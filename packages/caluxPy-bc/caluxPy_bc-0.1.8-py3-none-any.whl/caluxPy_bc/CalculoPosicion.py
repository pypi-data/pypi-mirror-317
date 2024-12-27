import os, pandas as pd, datetime, logging
class CalculoPosicion:

    def __init__(self, df, include, type, cwd) -> None:
        self.cwd = cwd
        logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid adding multiple handlers if this class is instantiated multiple times
        if not self.logger.handlers:
            fileHandler = logging.FileHandler(os.path.join(self.cwd, 'posicion.log'), mode='w', encoding='utf-8')
            fileHandler.setFormatter(logFormatter)
            self.logger.addHandler(fileHandler)
        
        self.include = include
        self.type = type
        self._df = df
        
        # Initial processing to prepare the data
        df2 = self._df.copy()
        df2['Fecha'] = pd.to_datetime(df2['Fecha'], format='%Y-%m-%d')
        grouped = df2.groupby('Codigos')
        df_entidades = {key: group for key, group in grouped}
        entidades = list(df_entidades.keys())
        cantidad_entidades = len(entidades)

        self.datos_entidades = pd.DataFrame()
        self.capital_subsectores = pd.DataFrame()
        i = 0
        
        for entidad in entidades:
            if entidad not in ['BM_SUBSECTOR', 'AP_SUBSECTOR', 'BAC_SUBSECTOR', 'CC_SUBSECTOR', 'SP_SUBSECTOR']:
                i += 1
                self.logger.info(f'Trabajando entidad {i} de {cantidad_entidades} -> {entidad}..')
                df_entidad = df_entidades[entidad]
                datos_entidad, capital_subsector = self.crear_df(df_entidad, entidad)
                self.datos_entidades = pd.concat([self.datos_entidades, datos_entidad]).reset_index(drop=True)
                self.capital_subsectores = pd.concat([self.capital_subsectores, capital_subsector]) if not self.capital_subsectores.empty else capital_subsector
                self.capital_subsectores.reset_index(drop=True, inplace=True)

        self.datos = self.calculo_subsector_sistema(self.datos_entidades)
        
        if self.include == 'var': self.datos = self.calcular_variacion(self.datos)

        self.logger.handlers[0].close()
        self.logger.removeHandler(self.logger.handlers[0])

    def exportar_datos(self, datos_entidades, cwd):
        if self.type == 'update':
            df_read = pd.read_excel(os.path.join(cwd, 'resultados_pnme.xlsx'))
            df_export = pd.concat([df_read, datos_entidades])
            df_export.to_excel(os.path.join(cwd, 'resultados_pnme.xlsx'), index=False)
        elif self.type == 'new':
            datos_entidades.to_excel(os.path.join(cwd, 'resultados_pnme.xlsx'), index=False)
        self.logger.info(f'Tabla de Resultados exportada con exito en ruta: {cwd}')

    def forma_calculo_posicion(self, datos, fecha, entidad):
        fecha_cambio_citi = datetime.datetime.strptime('2023-08-18', '%Y-%m-%d') #Cambio del cálculo fue el 25 de agosto del 2023 pero se usan los 5 días anteriores
        fecha_cambio = datetime.datetime.strptime('2023-04-10', '%Y-%m-%d') #Cambio del cálculo fue el 17 de abril del 2023 pero se usan los 5 días anteriores
        fecha_cambio_posicion = datetime.datetime.strptime('2024-01-01', '%Y-%m-%d')

        #region --> Pasar Valor a Variables y Verificar que un Valor pase
        # Fetch and verify values
        activos = datos.get('Total De Activos (ME-1)', 0)
        compra_forwards = datos.get('Contratos De Compra A Plazo Forward Y A Futuro De Divisas (ME-4-7)', 0)
        a_cont_sin_cont = datos.get('Cuentas Contingentes Deudoras Sin Contratos (ME-4-16)', 0)
        provisiones = datos.get('Provisión Para Diferencias En Cambios De Créditos D Y E (ME-4-5)', 0) + datos.get('Provisión Por Diferencias De Cambios De Los Créditos D Y E (ME-4-5)', 0)
        a_cont = datos.get('Cuentas Contingentes Deudoras (ME-4-2)', 0)
        pasivos = datos.get('Total De Pasivos (ME-2)', 0)
        venta_forwards = datos.get('Contratos De Venta A Plazo Forward Y A Futuro De Divisas (ME-4-8)', 0)


        if entidad == 'BM CITIBANK' and (fecha_cambio_citi <= fecha < fecha_cambio_posicion):
            derechos_derivados = datos.get('Derechos En Derivados (IF-1)', 0)
            obligaciones_derivados = datos.get('Obligaciones De Derivados (IF-2)', 0)
        else:
            derechos_derivados = datos.get('Derechos En Derivados (ME-4-7)', 0) + (datos.get('Contratos De Compra/Venta Al Contado (Spot) (ME-4-19)', 0) if fecha >= fecha_cambio_posicion else 0)
            obligaciones_derivados = datos.get('Obligaciones En Derivados (ME-4-8)', 0) + datos.get('Obligaciones De Derivados (ME-4-8)', 0)
        
        p_cont_sin_cont = datos.get('Cuentas Contingentes Acreedoras Sin Contratos (ME-4-17)', 0)
        p_cont = datos.get('Cuentas Contingentes Acreedoras (ME-4-3)', 0)
        capital_pagado = datos.get('Capital Pagado (BG-3-1)', 0)
        adicional_pagado = datos.get('Capital Adicional Pagado (BG-3-2)', 0)
        reservas = datos.get('Reservas Obligatoria\\ (ME-4-6)', 0)
        tipo_cambio = datos.get('tipo_cambio', 0)
        
        #Capital
        capital = capital_pagado + reservas
        capital_mas_adicional = capital + adicional_pagado
        
        #Calculo Actual
        parte_activa_actual = activos + derechos_derivados + a_cont_sin_cont - provisiones #Se suman las provisiones porque son negativas
        parte_pasiva_actual = pasivos + obligaciones_derivados + p_cont_sin_cont

        #Calculo Anterior
        parte_activa_antes = activos + (a_cont - compra_forwards - venta_forwards) + compra_forwards - provisiones
        parte_pasiva_antes = pasivos + (p_cont - compra_forwards - venta_forwards) + venta_forwards

        parte_activa = parte_activa_antes if fecha < fecha_cambio else parte_activa_actual
        parte_pasiva = parte_pasiva_antes if fecha < fecha_cambio else parte_pasiva_actual

        #np.seterr(divide = 'raise')
        try:
            parte_activa = parte_activa / tipo_cambio
            parte_pasiva = parte_pasiva / tipo_cambio
            posicion = parte_activa - parte_pasiva
        except Exception as e:
            self.logger.error(f'Error! Calculando Posición -> {fecha}')
            posicion = 0
        
        try:
            if tipo_cambio == 0 or capital == 0:
                self.logger.error(f'Error! Calculando Posición entre Capital -> {fecha} {'|| Tipo Cambio en 0' if tipo_cambio == 0 else '|| Capital en 0' if capital == 0 else ""}')
                posicion_capital = 0
            else:
                posicion_capital = posicion / (capital / tipo_cambio)
        except Exception as e:
            self.logger.error(f'Error! Calculando Posición entre Capital -> {fecha}')
            posicion_capital = 0
            
        try:     
            if tipo_cambio == 0 or capital_mas_adicional == 0:
                self.logger.error(f'Error! Calculando Posición entre Capital más Adicional -> {fecha} {'|| Tipo Cambio en 0' if tipo_cambio == 0 else '|| Capital más Adicional en 0' if capital_mas_adicional == 0 else ""}')
                posicion_capital_adicional = 0
            else:
                posicion_capital_adicional = posicion / (capital_mas_adicional / tipo_cambio)
        except Exception as e:
            self.logger.error(f'Error! Calculando Posición entre Capital más Adicional -> {fecha}')
            posicion_capital_adicional = 0
        
        capital_list = []
        capitaladd_list = []
        fecha_list = []
        df_capital = {}
        
        if entidad in ['BM SUBSECTOR', 'AP SUBSECTOR', 'BAC SUBSECTOR', 'CC SUBSECTOR', 'SP SUBSECTOR']:
            capital_list.append(capital)
            capitaladd_list.append(capital_mas_adicional)
            fecha_list.append(fecha)
        df_capital['Fecha'] = fecha_list  
        df_capital['Capital'] = capital_list
        df_capital['Capital Mas Add'] = capitaladd_list
        df_capital = pd.DataFrame.from_dict(df_capital)

        return posicion, posicion_capital, posicion_capital_adicional, tipo_cambio, df_capital, capital, capital_mas_adicional, parte_activa, parte_pasiva

    def sacar_valores(self, datos, cuentas, parametros, **kwargs):
        valores = {}
        par1 = kwargs['par1']
        #par2 = kwargs['par2']
        for cuenta in cuentas:
            try:
                valores[cuenta] = datos[(datos[parametros[0]] == cuenta) & (datos[parametros[1]] == par1)]['Valor'].values[0] # & (df[parametros[2]] == par2) #no se necesita entidad porque se esta dividiendo ya por entidades
            except IndexError:
                self.logger.warning(f'WARNING! -> Cuenta {cuenta} no encontrada!')

        i = 0
        while True:
            if i <= len(cuentas):
                try:
                    valores['tipo_cambio'] = datos[(datos[parametros[1]] == par1)]['Tipo Cambio'].values[i] #& (df[parametros[2]] == par2)
                    if valores['tipo_cambio'] == 0:
                        i += 1
                    else:
                        break
                except Exception as e:
                    i += 1
            else:
                valores['tipo_cambio'] = 0
                break
            
        return valores

    def calculador_posicion_fecha(self, datos, fechas_sacadas, cuentas_sacadas, parametros, entidad):
        dat, pos, pos_cap, pos_cap_add, tasa_cambio, capital, capital_mas_ad, parte_activa, parte_pasiva = [], [], [], [], [], [], [], [], []
        dict_posicion = {}
        capital_df = pd.DataFrame()
        for fecha in fechas_sacadas:
            dat.append(fecha.date())
            self.logger.info(f'Fecha: {fecha.date()}')
            posicion = self.forma_calculo_posicion(
                datos=self.sacar_valores(datos=datos, cuentas=cuentas_sacadas, parametros=parametros, par1=fecha),
                fecha=fecha,
                entidad=entidad
            )
            pos.append(posicion[0])
            pos_cap.append(posicion[1])
            pos_cap_add.append(posicion[2])
            tasa_cambio.append(posicion[3])
            capital.append(posicion[5])
            capital_mas_ad.append(posicion[6])
            parte_activa.append(posicion[7])
            parte_pasiva.append(posicion[8])
            
            capital_df = pd.concat([capital_df, posicion[4]])

        self.logger.info(f'{dat} - {entidad} - {tasa_cambio}')
        dict_posicion = {'Fecha': dat,
                         'AyC': parte_activa,
                         'PyC': parte_pasiva,
                         'Posicion': pos,
                         'Capital': capital,
                         'Capital + Add': capital_mas_ad,
                         '%Capital': pos_cap,
                         '%Capital + Add': pos_cap_add,
                         'Tipo Cambio': tasa_cambio
                         }

        return dict_posicion, capital_df

    def generar_diccionario_posicion_entidad(self, datos, entidad):
        cuentas_sacadas = datos['Cuenta'].unique()
        fechas_sacadas = datos['Fecha'].unique()
        parametros = ['Cuenta', 'Fecha', 'Codigos', 'Valor']
        dic_resultados_posicion_fecha, capital = self.calculador_posicion_fecha(
            datos=datos,
            fechas_sacadas=fechas_sacadas,
            cuentas_sacadas=cuentas_sacadas,
            parametros=parametros,
            entidad=entidad
        )
        return dic_resultados_posicion_fecha, capital

    def crear_df(self, datos, entidad):

        #Definir las informaciones por Periodicidad
        diarias = datos[datos['Dia'].str.startswith('DIA')] #Informaciones Diarias
        mensuales = datos[~datos['Dia'].astype(str).str.startswith('DIA')] #Informaciones Mensuales

        #Sacar las informaciones por periodicidad y luego juntarlas y retornar df compilado
        informaciones_diarias_entidad, capital_diario = self.generar_diccionario_posicion_entidad(datos = diarias, entidad = entidad)
        informaciones_diarias_entidad = pd.DataFrame(informaciones_diarias_entidad)
        informaciones_diarias_entidad['Periodicidad'] = 'Diaria'
        informaciones_diarias_entidad.sort_values(by = ['Fecha'], inplace = True)
        #informaciones_diarias_entidad['Variacion'] = informaciones_diarias_entidad['Posicion'] - informaciones_diarias_entidad['Posicion'].shift(1)
        
        capital_diario = pd.DataFrame(capital_diario)
        capital_diario['Periodicidad'] = 'Diaria'
        capital_diario['Entidad'] = entidad

        informaciones_mensuales_entidad, capital_mensual = self.generar_diccionario_posicion_entidad(datos = mensuales, entidad = entidad)
        informaciones_mensuales_entidad = pd.DataFrame(informaciones_mensuales_entidad)
        informaciones_mensuales_entidad['Periodicidad'] = 'Mensual'
        informaciones_mensuales_entidad.sort_values(by = ['Fecha'], inplace = True)
        #informaciones_mensuales_entidad['Variacion'] = informaciones_mensuales_entidad['Posicion'] - informaciones_mensuales_entidad['Posicion'].shift(1)
        
        capital_mensual = pd.DataFrame(capital_mensual)
        capital_mensual['Periodicidad'] = 'Mensual'
        capital_mensual['Entidad'] = entidad

        informaciones_entidad = pd.concat([informaciones_diarias_entidad, informaciones_mensuales_entidad])
        capital_subsector = pd.concat([capital_diario, capital_mensual])
        informaciones_entidad['Entidad'] = entidad
        informaciones_entidad[['Subsector', 'Entidad']] = informaciones_entidad['Entidad'].str.split('_', n = 1, expand = True)
        informaciones_entidad = informaciones_entidad[[
            'Fecha', 'Periodicidad', 'Entidad', 'Subsector', 'Posicion', 'Capital', 'Capital + Add',
            '%Capital', '%Capital + Add', 'Tipo Cambio', 'AyC', 'PyC'
        ]]#, 'Variacion']]

        return informaciones_entidad, capital_subsector

    def calculo_subsector_sistema(self, df_entidades):
        df_total = pd.DataFrame()

        def calculo(df: pd.DataFrame, type: str):
            #Crea un df vacio
            df_results = pd.DataFrame()
            
            #toma porcion del df parametro y saca la suma 
            dfs = df[['AyC', 'PyC', 'Posicion', 'Capital', 'Capital + Add']]
            suma = dfs.sum()

            #Se llena el df vacio con las nuevas informaciones
            fecha = df['Fecha'].unique()
            df_results['Fecha'] = fecha
            df_results['Periodicidad'] = df['Periodicidad'].unique()
            df_results['Entidad'] = 'SUBSECTOR' if type == 'sub' else 'SISTEMA'
            df_results['Subsector'] = df['Subsector'].unique() if type == 'sub' else 'SIS'
            df_results['AyC'] = suma['AyC']
            df_results['PyC'] = suma['PyC']
            df_results['Posicion'] = suma['Posicion']
            df_results['Capital'] = suma['Capital']
            df_results['Capital + Add'] = suma['Capital + Add']

            #Informaciones que requieren el ripo de cambio
            tipo_cambio = df['Tipo Cambio'].unique()
            self.logger.info(f'Fecha {fecha} | Tipo Cambio -> {tipo_cambio}')
            df_results['%Capital'] = (suma['Posicion'] * tipo_cambio) / suma['Capital']
            df_results['%Capital + Add'] = (suma['Posicion'] * tipo_cambio) / suma['Capital + Add']
            df_results['Tipo Cambio'] = tipo_cambio
            return df_results
        
        #Para determinar los valores de los subsectores
        grouped = df_entidades.groupby(['Periodicidad', 'Subsector', 'Fecha'])
        for key, df in grouped:
            df_results = calculo(df, 'sub')
            df_total = df_results if df_total.empty else pd.concat([df_total, df_results])

        #Para determinar los valores del sistema
        grouped = df_total.groupby(['Periodicidad', 'Fecha'])
        for key, df in grouped:
            df_results = calculo(df, 'sis')
            df_total = df_results if df_total.empty else pd.concat([df_total, df_results])

        #Para sacar las variaciones del df que contiene las infos de subsectores y sistema
        #subsector_df = pd.DataFrame()
        #grouped = df_total.groupby(['Periodicidad', 'Subsector'])
        #for key, df in grouped:
        #    df.sort_values(by = ['Fecha'], inplace = True)
        #    df['Variacion'] = df['Posicion'] - df['Posicion'].shift(1)
        #    subsector_df = df if df.empty else pd.concat([subsector_df, df])
        #df_total = subsector_df

        #Se junta el df original con el que resulta de este proceso
        df_final = pd.concat([df_entidades, df_total])

        return df_final
    
    def calcular_variacion(self, df):
        # Implement this method if needed
        return df