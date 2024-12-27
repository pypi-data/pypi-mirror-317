import os, pandas as pd, datetime, errno, logging, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

class ExtraccionBGD():
   
    def __init__(self, estructura, meses, años, listado_cuentas, dias, mensuales, columnas, line_thresh, cwd) -> None:
        
        #Definición de las Variables de la Instancia
        self.estructura = estructura
        self.meses = meses
        self.años = años
        self.listado_cuentas = listado_cuentas
        self.dias = dias
        self.mensuales = mensuales
        self.columnas = columnas
        self.errores = 0
        self.errores_prompt = ''
        self.line_thresh = line_thresh
        self.cwd = cwd
        self.rutas_trabajadas = []
        self.rutas_no_trabajadas = []
        
        self.crear_logger()
        hoy = datetime.datetime.now().date()
        
        #Ejecución de las Funcione
        self.rutas = []
        for año in self.años:
            conteo_mes = 0
            for mes in meses:
                conteo_mes += 1
                if int(año) >= hoy.year and conteo_mes > hoy.month:
                    break
                for key, value in estructura.items():
                    for subsector in value['subsectores']:
                        self.rutas.append(self.crear_ruta(estructura = estructura, division = key, subsector = subsector, año = año, mes = mes))

        self.generated_df = self.recoleccion_de_datos_concurrent(rutas = self.rutas, 
                                                                 listado_cuentas = self.listado_cuentas, 
                                                                 dias = self.dias, 
                                                                 mensuales = self.mensuales, 
                                                                 columnas = self.columnas, 
                                                                 line_thresh = self.line_thresh)
        self.cerrar_logger()
        
    def crear_ruta(self, division, estructura, subsector, año, mes):
        terminal = ['.xlsm', '.xlsx']
        terminal_seeker = 0
        try:
            while True:
                if division == 'Division_Banca_Fomento':
                    directorio = estructura[division]['estructura_ruta'].format(division = division, año = año, subsector = subsector)
                    archivo = estructura[division]['estructura_archivo'].format(subsector = subsector, mes = mes, año = año[-2:], terminal = terminal[terminal_seeker])
                elif division == 'Division_Banca_Comercial':
                    directorio = estructura[division]['estructura_ruta'].format(division = division, año = año)
                    archivo = estructura[division]['estructura_archivo'].format(mes = mes, año = año[-2:], terminal = terminal[terminal_seeker])
                ruta = os.path.join(directorio, archivo)
                if os.path.exists(ruta):
                    break
                else:
                    terminal_seeker += 1
                    if terminal_seeker >= len(terminal): raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ruta) 
        except Exception as e:
            self._logger.error(f'crear_ruta => {e} => {ruta}')
        
        return ruta

    def recoleccion_de_datos_concurrent(self, rutas, listado_cuentas, dias, mensuales, columnas, line_thresh):
        # Initialize DataFrame to collect all results
        data_frames = []
        all_data = pd.DataFrame()
        # Use ThreadPoolExecutor to process multiple files in parallel
        
        max_workers = min(10, os.cpu_count() + 4) 
        with ThreadPoolExecutor(max_workers = max_workers) as executor:
            # Map each file to a future
            futures = {executor.submit(self.process_file, ruta, listado_cuentas, dias, mensuales, columnas, line_thresh): ruta for ruta in rutas}
            for future in as_completed(futures):
                try:
                    file_data = future.result()
                    data_frames.append(file_data)
                except Exception as e:
                    self._logger.error(f"recoleccion_de_datos_concurrent => Error processing file {futures[future]}: {e}")
                    print(f"recoleccion_de_datos_concurrent => Error processing file {futures[future]}: {e}")
        all_data = pd.concat(data_frames, ignore_index = True)
        if all_data.empty:
            raise ValueError('recoleccion_de_datos_concurrent => No data collected.')
        else:
            self.limpiar_data(all_data)
        return all_data

    def process_file(self, file_path, listado_cuentas, dias, mensuales, columnas, line_thresh):
        # Initialize a container for DataFrames generated from each sheet
        data_frames = []
        processed_data = pd.DataFrame()
        # Use pandas.ExcelFile for efficient access to sheets
        with pd.ExcelFile(file_path) as excel:
            print(f'Trabajando => {file_path}')
            try:
                for sheet_name in excel.sheet_names:
                    if sheet_name in dias + mensuales:
                        col = 0
                        while True:
                            try:
                                df = excel.parse(sheet_name = sheet_name, usecols = f'A:{columnas[col]}', nrows = line_thresh)
                                processed_df, status, error = self.generar_df_concurrent(df, file_path, sheet_name, listado_cuentas)
                                data_frames.append(processed_df)
                                break
                            except pd.errors.ParserError as e:
                                col += 1
                                if col >= len(columnas): raise pd.errors.ParserError('Column could not be properly parsed')
                            except Exception as e:
                                error_info = traceback.format_exc()
                                raise Exception(f'{e}\n{error_info}')
                        if processed_df.empty:
                            if status == 'no trabajado':
                                print(f'\tprocess_file => from {file_path}: {sheet_name} status: {status}')
                            else:
                                print(f'\tprocess_file => from {file_path}: {sheet_name} => empty')
                                
            except Exception as e:
                error_info = traceback.format_exc()
                raise Exception(f'process_file => {e}\n{error_info}')
            processed_data = pd.concat(data_frames, ignore_index=True)
            if processed_data.empty:
                print(f'process_file => file {file_path} did not return data')
                self._logger.info(f'process_file => file {file_path} did not return data')
                self.rutas_no_trabajadas.append(file_path)
            else:
                print(f'Trabajada => {file_path}')
                self.rutas_trabajadas.append(file_path)
        # Concatenate all DataFrames from this file
        return processed_data

    def generar_df_concurrent(self, df, file_path, sheet_name, listado_cuentas) -> list[pd.DataFrame, str]:
        processed_data_df = pd.DataFrame()
        # Load the specific sheet into a DataFrame
        try:
            # Assuming `extraer_data` can process data from a single DataFrame
            processed_data, tipo_cambio, fecha, status, error = self.extraer_data(data = df, listado_cuentas = listado_cuentas, file_name = os.path.basename(file_path))
            if error != '':
                if len(processed_data) > 0:
                    # Additional processing, e.g., adding columns for Dia, Mes, etc.
                    processed_data['Dia'] = sheet_name  # Assuming sheet names are dates or similar
                    processed_data['Mes'], processed_data['Subsector'] = self.get_splitted(file_path)
                    processed_data['Tipo Cambio'] = tipo_cambio
                    processed_data['Fecha'] = fecha
                    #processed_data['Periodicidad'] = 'Diaria' if sheet_name[0:3] == 'DIA' else 'Mensual'
                    
                    # Reorder or modify DataFrame as needed
                    processed_data_df = pd.DataFrame(processed_data)
                    processed_data_df = processed_data_df[['Dia', 'Mes', 'Fecha', 'Subsector', 'Entidad', 'Cuenta', 'Valor', 'Tipo Cambio']]
                    if processed_data_df.empty:
                        print(f'generar_df_concurrent => {file_path}: {sheet_name} (empty)')
        except KeyError as e:
            error_info = traceback.format_exc()
            self._logger.error(f'generar_df_concurrent => Error Falta columna {e} || Día: {sheet_name}\n{error_info}')
        except Exception as e:
            error_info = traceback.format_exc()
            self._logger.error(f"generar_df_concurrent => Error processing sheet {sheet_name}: {file_path} => {e}\n{error_info}")
            
        return processed_data_df, status, error  # Return an empty DataFrame in case of error

    def extraer_data(self, data, listado_cuentas, file_name) -> list[dict, float, datetime.date, str]:
        valores_data = []
        entidades_data = []
        cuentas_data = []
        datos = {}
        tipo_cambio = 0
        fecha = None
        error = 0
        status = 'ok'
        
        try:
            fecha = data.iloc[0].index[0]
            if fecha in [None, '', 'Unnamed: 0']:
                status = 'no trabajado'
                raise ValueError(f'No trabajado')
            tipo_cambio = float(data.iloc[0].iloc[1]) #Extracción del tipo de cambio
            hoy = datetime.datetime.now().date()
            entidades = data.iloc[2].to_list() #Extracción del nombre de las entidades
            entidades[0] = 'ENTIDADES' #reemplaza el primer valor por esto
            data.rename(columns = data.iloc[2], inplace = True) #Cambia la primera linea del DataFrame para que los índices por columna sean adecuados
            #data.columns = entidades

            #Definición de Variables
            cuenta = ''
            if isinstance(fecha, datetime.datetime):
                fecha = fecha.date()
                if fecha <= hoy:
                    #Proceso de creado de listas
                    for codigo in listado_cuentas:
                        try:
                            linea = data[data['CODIGOS'] == codigo].values[0].tolist()
                            cuenta = linea[0]
                            for item in linea: #itera sobre las cuentas seleccionadas
                                #if type(item) == int or type(item) == float and not pd.isna(item): #itera por cada componente de la línea y si cumple con las condiciones se agrega
                                if item != codigo and item != cuenta:
                                    valores_data.append(item) #Se agrega el valor a los datos
                                    cuentas_data.append(f'{cuenta.lstrip(' ').rstrip(' ').title()} ({codigo})') #Se agrega la cuenta por cada dato agregado
                                    
                            for entidad in entidades:
                                if entidad != 'ENTIDADES' and entidad != 'CODIGOS': #and not pd.isna(entidad) and entidad != 0:
                                    entidades_data.append(entidad)

                            #Verifica que las longitudes cuadren y si no devuelve un error
                            if len(entidades_data) == len(valores_data):
                                datos = {
                                        'Entidad': entidades_data,
                                        'Cuenta': cuentas_data,
                                        'Valor': valores_data
                                        }
                        except Exception as e: #Si no encuentra la cuenta
                            error_info = traceback.format_exc()
                            self._logger.error(f'extraer_data => ERROR Cuenta {cuenta}: {codigo} no encontrada en fecha {fecha} => {file_name} \n{error_info}')
        
        except ValueError as e:
            pass
        except Exception as e:
            error_info = traceback.format_exc()
            error = f'extraer_data => {e}\n {error_info}'
        finally:
            return datos, tipo_cambio, fecha, status, error

    def limpiar_data(self, df):
        df.dropna(inplace = True)

    def get_splitted(self, ruta: str) -> str:
            splitted = ruta.split('\\')
            mes = splitted[-1].split('.')[0].split('_')[-1][0:3]
            if splitted[5] == 'Division_Banca_Fomento':
                subsector = splitted[8]
            elif splitted[5] == 'Division_Banca_Comercial':
                subsector = 'BM'
            return mes, subsector
        
    def crear_logger(self) -> None:
        #desktop = self.get_folder_path()
        _logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        self._fileHandler = logging.FileHandler("{0}/{1}.log".format(self.cwd, 'extraccion_log'), mode = 'w', encoding = 'utf-8')
        self._fileHandler.setFormatter(_logFormatter)
        self._logger.addHandler(self._fileHandler)
        
    def cerrar_logger(self) -> None:
        self._logger.removeHandler(self._fileHandler)
        self._fileHandler.close()
  
    #region => Backup
    '''
    def recoleccion_de_datos(self, excel, listado_cuentas, dias, mensuales, columnas, subsector, mes, line_thresh):      
        #Llama la función y como se manda el DataFrame entonces se concatena la información al usado
        generated_df = self.generar_df(
                                        excel = excel, 
                                        listado_cuentas = listado_cuentas, 
                                        dias = dias, 
                                        mensuales = mensuales,
                                        columnas = columnas,
                                        subsector = subsector,
                                        mes = mes,
                                        line_thresh = line_thresh
                                        )
        del excel
        return generated_df
    
    def generar_df(self, excel, listado_cuentas, dias, mensuales, columnas, subsector, mes, line_thresh):
        #Genera una base concatenada de los dias y ese DF generado lo devuelve a recolección de datos
        generated_df = pd.DataFrame()
        self.errores_prompt = []
        
        for dia in excel.sheet_names:
            if dia in dias or dia in mensuales:
                col = 0
                while True:
                    try:
                        data, tipo_cambio, fecha = self.extraer_data(
                                                                     data = pd.read_excel(excel, sheet_name = dia, nrows = line_thresh, usecols = columnas[col]), 
                                                                     listado_cuentas = listado_cuentas
                                                                    )
                        data = pd.DataFrame(data)
                        #Agrega columnas de constantes
                        if not data.empty:
                            data['Dia'] = dia
                            data['Mes'] = mes
                            data['Subsector'] = subsector
                            data['Tipo Cambio'] = tipo_cambio
                            data['Fecha'] = fecha
                            data = data[['Dia', 'Mes', 'Fecha', 'Subsector', 'Entidad', 'Cuenta', 'Valor', 'Tipo Cambio']]
                            
                        #Concatena las tablas que se van creando
                        generated_df = pd.concat([generated_df, data])
                        break
                    except pd.errors.ParserError as e:
                        col += 1
                    except KeyError as e:
                        message = f'--Error! -> Falta columna {e} || Día: {dia}'
                        self._logger.error(message)
                        self.errores += 1
                        self.errores_prompt.append(f' {message}')
                        raise KeyError(self.errores_prompt)
                        
        return generated_df
    
    def verificar_ruta(self, ruta):
        if os.path.exists(ruta):
            return True
        else: 
            return False
    
    def crear_ruta(self, division, estructura, subsector, año, mes):
        terminal_seeker = 0
        ruta = ''
        try:
            while True:
                if division == 'Division_Banca_Fomento':
                    directorio = estructura['estructura_ruta'].format(division = division, año = año, subsector = subsector)
                    #Se usa terminal seeker para iterar en opciones
                    archivo = estructura['estructura_archivo'].format(subsector = subsector, mes = mes, año = año[-2:], terminal = terminal[terminal_seeker])
                else: 
                    directorio = estructura['estructura_ruta'].format(division = division, año = año)
                    archivo = estructura['estructura_archivo'].format(mes = mes, año = año[-2:], terminal = terminal[terminal_seeker])
                ruta = os.path.join(directorio, archivo)
                validacion = self.verificar_ruta(ruta = ruta)
                if validacion == True:
                    break
                else:
                    terminal_seeker += 1
                    if terminal_seeker > 1: raise Exception('Ruta no encontrada')
            ExtraccionBGD.rutas.append(ruta)
        except Exception as e:
            self._logger.error(f'{e} => {ruta}')
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ruta) 
            
        return ruta, validacion'''
    #endregion => Backup

