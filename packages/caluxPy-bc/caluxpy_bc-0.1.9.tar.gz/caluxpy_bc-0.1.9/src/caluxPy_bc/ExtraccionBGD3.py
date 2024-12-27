import os
import pandas as pd
import datetime
import logging

class ExtraccionBGD:

    TERMINALS = ['.xlsm', '.xlsx']
    LOG_FILE = 'extraccion_log.txt'
    
    def __init__(self, estructura, division, mes, año, listado_cuentas, dias, mensuales, columnas, subsector, line_thresh, cwd):
        """
        Initialize the ExtraccionBGD instance with provided parameters.
        """
        self.estructura = estructura
        self.division = division
        self.mes = mes
        self.año = año
        self.listado_cuentas = listado_cuentas
        self.dias = dias
        self.mensuales = mensuales
        self.columnas = columnas
        self.subsector = subsector
        self.terminal = ['.xlsm', '.xlsx']
        self.errores = 0
        self.errores_prompt = []
        self.line_thresh = line_thresh
        self.cwd = cwd
        #self.Fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()  # Add the new class variable Fecha
        self.rutas = []

        log_path = os.path.join(self.cwd, self.LOG_FILE)
        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        self._ruta, self._validacion = self.crear_ruta()
        self.generated_df = self.recoleccion_de_datos()
        self.limpiar_data(self.generated_df)

    @staticmethod
    def validate_fecha(fecha):
        """
        Validate and convert the input date string to a datetime.date object.
        """
        try:
            return datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            logging.error("Invalid date format. Expected 'YYYY-MM-DD'.")
            raise
  
    def crear_ruta(self):
        """
        Create the file path based on the given parameters and verify its existence.
        """
        for terminal in self.TERMINALS:
            directorio = self.estructura['estructura_ruta'].format(
                division = self.division,
                año = self.año,
                subsector = getattr(self, 'subsector', '')
            )
            archivo = self.estructura['estructura_archivo'].format(
                subsector=self.subsector if self.division == 'Division_Banca_Fomento' else '',
                mes=self.mes,
                año=self.año[-2:],
                terminal=terminal
            )
            ruta = os.path.join(directorio, archivo)
            if self.verificar_ruta(ruta):
                self.rutas.append(ruta)
                return ruta, True
        '''
        while True:
            if self.division == 'Division_Banca_Fomento':
                directorio = self.estructura['estructura_ruta'].format(
                    division=self.division,
                    año=self.año,
                    subsector=self.subsector
                )
                archivo = self.estructura['estructura_archivo'].format(
                    subsector=self.subsector,
                    mes=self.mes,
                    año=self.año[-2:],
                    terminal=self.terminal[terminal_seeker]
                )
            else:
                directorio = self.estructura['estructura_ruta'].format(
                    division=self.division,
                    año=self.año
                )
                archivo = self.estructura['estructura_archivo'].format(
                    mes=self.mes,
                    año=self.año[-2:],
                    terminal=self.terminal[terminal_seeker]
                )

            ruta = os.path.join(directorio, archivo)
            validacion = self.verificar_ruta(ruta)
            if validacion:
                break
            else:
                terminal_seeker += 1
                if terminal_seeker >= len(self.terminal):
                    logging.error(f"No valid file found for {self.division}, {self.subsector}, {self.mes}, {self.año}.")
                    raise FileNotFoundError("No valid file found.")
                    
        ExtraccionBGD.rutas.append(ruta)
        return ruta, validacion
        '''
        logging.error("No valid file found for the specified parameters.")
        raise FileNotFoundError("No valid file found.")
  
    @staticmethod
    def verificar_ruta(ruta):
        """
        Verify if the given file path exists.
        """
        if os.path.exists(ruta):
            logging.info(f"File found: {ruta}")
            return True
        else:
            logging.warning(f"File not found: {ruta}")
            return False

    def recoleccion_de_datos(self):
        """
        Collect data from the specified Excel file.
        """
        '''
        excel = pd.ExcelFile(self._ruta)
        generated_df = self.generar_df(excel)
        del excel
        return generated_df
        '''
        
        with pd.ExcelFile(self.ruta) as excel:
            relevant_sheets = self.get_relevant_sheets(excel.sheet_names)
            return self.generar_df(excel, relevant_sheets)

    def get_relevant_sheets(self, sheet_names):
        """
        Filter and return relevant sheets based on `dias` and `mensuales`.
        """
        return [
            sheet for sheet in sheet_names
            if sheet in self.dias or (sheet in self.mensuales) #and self.check_fecha_match(sheet))
        ]

    def generar_df(self, excel, sheets):
        """
        Generate a DataFrame by concatenating data from the specified sheets.
        """
        generated_df = pd.DataFrame()

        '''
        for dia in excel.sheet_names:
            if dia in self.dias or (dia in self.mensuales and self.check_fecha_match(dia)):
                col = 0
                while True:
                    try:
                        data, tipo_cambio, fecha = self.extraer_data(
                            pd.read_excel(excel, sheet_name=dia, nrows=self.line_thresh, usecols=self.columnas[col])
                        )
                        if self.Fecha and fecha != self.Fecha:
                            break  # Exit if the extracted Fecha does not match the class variable Fecha

                        data = pd.DataFrame(data)
                        if not data.empty:
                            data['Dia'] = dia
                            data['Mes'] = self.mes
                            data['Subsector'] = self.subsector
                            data['Tipo Cambio'] = tipo_cambio
                            data['Fecha'] = fecha
                            # Create a unique identifier for each row
                            data['Unique_ID'] = data.apply(lambda row: f"{row['Dia']}_{row['Mes']}_{row['Subsector']}_{row['Entidad']}_{row['Cuenta']}_{row['Fecha']}", axis=1)
                            data = data[['Unique_ID', 'Dia', 'Mes', 'Fecha', 'Subsector', 'Entidad', 'Cuenta', 'Valor', 'Tipo Cambio']]
                        
                        generated_df = pd.concat([generated_df, data])
                        break
                    except pd.errors.ParserError:
                        col += 1
                        if col >= len(self.columnas):
                            logging.error(f"Parser error in sheet {dia} for {self.subsector}, {self.mes}, {self.año}.")
                            break
                    except KeyError as e:
                        message = f'--Error! -> Falta columna {e} || Día: {dia}'
                        self.errores += 1
                        self.errores_prompt.append(message)
                        logging.error(message)
                        break
        '''
        
        for sheet in sheets:
            try:
                for col in self.columnas:
                    try:
                        data, tipo_cambio, fecha = self.extraer_data(pd.read_excel(excel, sheet_name=sheet, nrows=self.line_thresh, usecols=col))
                        if not fecha:
                            logging.info(f"Skipping sheet {sheet} as fecha is not found.")
                            break
                        data = self.process_data(data, sheet, tipo_cambio, fecha)
                        generated_df = pd.concat([generated_df, data], ignore_index=True)
                        break
                    except pd.errors.ParserError:
                        logging.warning(f"Parser error in sheet {sheet}, column {col}.")
            except Exception as e:
                logging.exception(f"Error processing sheet {sheet}: {e}")
        
        return generated_df

    def process_data(self, data, sheet, tipo_cambio, fecha):
        """
        Process raw data into a structured DataFrame with metadata columns.
        """
        data['Dia'] = sheet
        data['Mes'] = self.mes
        data['Subsector'] = self.subsector
        data['Tipo Cambio'] = tipo_cambio
        data['Fecha'] = fecha
        data['Unique_ID'] = data.apply(
            lambda row: f"{row['Dia']}_{row['Mes']}_{row['Subsector']}_{row['Entidad']}_{row['Cuenta']}_{row['Fecha']}",
            axis=1
        )
        return data[['Unique_ID', 'Dia', 'Mes', 'Fecha', 'Subsector', 'Entidad', 'Cuenta', 'Valor', 'Tipo Cambio']]
        
    def check_fecha_match(self, dia):
        """
        Check if the fecha extracted matches the class variable Fecha.
        """
        excel = pd.ExcelFile(self._ruta)
        for col in self.columnas:
            try:
                _, _, fecha = self.extraer_data(
                    pd.read_excel(excel, sheet_name=dia, nrows=self.line_thresh, usecols=col)
                )
                if fecha == self.Fecha:
                    return True
            except pd.errors.ParserError:
                continue
            except KeyError:
                continue
        return False

    def extraer_data(self, data):
        """
        Extract data from a DataFrame and return the processed values.
        """
        try:
            tipo_cambio = data.iloc[0, 1] #tipo_cambio = data.iloc[0].iloc[1]
            fecha = data.columns[0] #fecha = data.iloc[0].index[0]
            hoy = datetime.datetime.now().date()
            entidades = data.iloc[2].to_list()
            entidades[0] = 'ENTIDADES'
            data.rename(columns=data.iloc[2], inplace=True)

            valores_data = []
            entidades_data = []
            cuentas_data = []
            datos = {}

            if isinstance(fecha, datetime.datetime):
                fecha = fecha.date()
                if fecha <= hoy:
                    for codigo in self.listado_cuentas:
                        try:
                            linea = data[data['CODIGOS'] == codigo].values[0].tolist()
                            cuenta = linea[0]
                            for item in linea:
                                if item != codigo and item != cuenta:
                                    valores_data.append(item)
                                    cuentas_data.append(f'{cuenta.strip().title()} ({codigo})')

                            for entidad in entidades:
                                if entidad != 'ENTIDADES' and entidad != 'CODIGOS':
                                    entidades_data.append(entidad)

                            if len(entidades_data) == len(valores_data):
                                datos = {
                                    'Entidad': entidades_data,
                                    'Cuenta': cuentas_data,
                                    'Valor': valores_data
                                }
                            else:
                                logging.error(f"Length mismatch between entidades and valores for {codigo} on {fecha}.")
                                logging.error(f"Entidades: {entidades_data}")
                                logging.error(f"Valores: {valores_data}")
                        except Exception as e:
                            logging.error(f"ERROR! --> Cuenta {cuenta} no encontrada: {e}")

            return datos, tipo_cambio, fecha
        except Exception as e:
            logging.exception(f"Error extracting data: {e}")
            return pd.DataFrame(), None, None

    @staticmethod
    def limpiar_data(df):
        """
        Clean the DataFrame by dropping NaN values and removing duplicates.
        """
        df.dropna(inplace=True)
        initial_len = len(df)
        df.drop_duplicates(subset=['Unique_ID'], inplace=True)
        final_len = len(df)
        
        logging.info(f"Removed {initial_len - final_len} duplicate rows based on Unique_ID.")
        
        # Drop the 'Unique_ID' column
        df.drop(columns=['Unique_ID'], inplace=True)
        logging.info("Dropped 'Unique_ID' column after removing duplicates.")




