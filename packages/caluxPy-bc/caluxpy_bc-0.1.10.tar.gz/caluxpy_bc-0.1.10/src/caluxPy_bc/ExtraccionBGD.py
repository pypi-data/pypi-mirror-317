import os
import pandas as pd
import datetime
import logging

class ExtraccionBGD:

    rutas = []

    def __init__(self, estructura, division, mes, año, listado_cuentas, dias, mensuales, columnas, subsector, line_thresh, cwd, fecha=None):
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
        self.Fecha = None  # Default value if no fecha is provided
        if fecha:
            self.Fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()

        logging.basicConfig(filename=os.path.join(self.cwd, 'extraccion_log.txt'), level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        self._ruta, self._validacion = self.crear_ruta()
        self.generated_df = self.recoleccion_de_datos()
        self.limpiar_data(self.generated_df)

    # I - Se crea la ruta a acceder por el código
    def crear_ruta(self):
        """
        Create the file path based on the given parameters and verify its existence.
        """
        terminal_seeker = 0
        ruta = ''

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

    # II - Se verifica si la ruta existe
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

    # III - Se crea una instancia de excel para pasar a generar el DataFrame
    def recoleccion_de_datos(self):
        """
        Collect data from the specified Excel file.
        """
        excel = pd.ExcelFile(self._ruta)
        generated_df = self.generar_df(excel)
        del excel
        return generated_df

    # IV - Se manda a extraer los datos mediante V y se concatenan en este
    def generar_df(self, excel):
        """
        Generate a DataFrame by concatenating data from the specified sheets.
        """
        generated_df = pd.DataFrame()

        for dia in excel.sheet_names:
            # Skip days not in `dias` or `mensuales`
            if dia not in self.dias and dia not in self.mensuales:
                continue
            
            col = 0
            while True:
                try:
                    # Extract data, tipo_cambio, and fecha
                    data, tipo_cambio, fecha = self.extraer_data(
                        pd.read_excel(excel, sheet_name=dia, nrows=self.line_thresh, usecols=self.columnas[col])
                    )
                    
                    # If Fecha is defined and does not match, skip this sheet
                    if self.Fecha and fecha != self.Fecha:
                        break
                    
                    # Convert to DataFrame and process
                    data = pd.DataFrame(data)
                    if not data.empty:
                        data['Dia'] = dia
                        data['Mes'] = self.mes
                        data['Subsector'] = self.subsector
                        data['Tipo Cambio'] = tipo_cambio
                        data['Fecha'] = fecha
                        # Create a unique identifier for each row
                        data['Unique_ID'] = data.apply(
                            lambda row: f"{row['Dia']}_{row['Mes']}_{row['Subsector']}_{row['Entidad']}_{row['Cuenta']}_{row['Fecha']}", 
                            axis=1
                        )
                        data = data[['Unique_ID', 'Dia', 'Mes', 'Fecha', 'Subsector', 'Entidad', 'Cuenta', 'Valor', 'Tipo Cambio']]
                    
                    # Concatenate with the result DataFrame
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

        return generated_df

    def extraer_data(self, data):
        """
        Extract data from a DataFrame and return the processed values.
        """
        tipo_cambio = data.iloc[0].iloc[1]
        fecha = data.iloc[0].index[0]
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

