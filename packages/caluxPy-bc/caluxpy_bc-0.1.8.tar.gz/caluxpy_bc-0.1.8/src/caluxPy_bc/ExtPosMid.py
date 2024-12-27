import os, logging, pathlib, datetime, pandas as pd, errno
from Python.Packages.caluxPy_bc.src.caluxPy_bc.ExtraccionBGD import ExtraccionBGD as Extraccion
from CalculoPosicion import CalculoPosicion as PNME

class ExtPosMid():
    
    def __init__(self, 
                 cwd: str, 
                 type: str, 
                 listado_cuentas: list[str], 
                 fecha: str = '', 
                 años: list = [], 
                 line_thresh: int = 3350, 
                 estructura: dict = {}, 
                 ext: bool = True, 
                 pos: bool = True,
                 file: str = '') -> None:
        
        self.cwd = cwd
        self.n_ext = 'prueba_pnme.xlsx'
        self.n_pos = 'resultados_pnme.xlsx'
        self.type = type
        self.fecha = fecha
        self.file = file
        
        self.crear_logger()
        
        #Verificación de que se incluyó hasta dentro de los parámetros       
        if self.type in ['update', 'big_update']:
            if self.fecha == '':
                e_prompt = 'Parámetro "fecha" no especificado'
                self.errorHandler(e_prompt)
            else:
                fecha_inputs = fecha.split('-')
        else:
            self.fecha = ''  
          
        self.años = años if self.fecha == '' else [fecha_inputs[0]]
        #self.años = ['2022']
        self.meses = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'] if self.fecha == '' else [self.mes_select(fecha_inputs[1])]
        #self.meses = ['FEB']
        self.dias = ['DIA' + str(1 + i) for i in range(31)] if self.fecha == '' else ['DIA' + str(int(fecha_inputs[2]))]
        self.mensuales = [mes + año[-2:] for año in años for mes in self.meses]
        self.columnas = ['AC', 'AB']
        
        #Asignación de otras variables
        self.estructura, self.listado_cuentas, self.line_thresh = estructura, listado_cuentas, line_thresh
        self.ext, self.pos = ext, pos
        
        #Verificación de cual proceso se desea
        if self.ext:
            self.datos = self.extraccion()
            self.exportar(datos = self.datos, df_type = 'extraccion')
        if self.pos:
            self.pnme = self.posicion()
    
        self.cerrar_logger()
        
    def extraccion (self) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            e_prompt = ''
            datos = Extraccion(estructura = self.estructura,
                               meses = self.meses,
                               años = self.años,
                               listado_cuentas = self.listado_cuentas,
                               dias = self.dias,
                               mensuales = self.mensuales,
                               columnas = self.columnas,
                               line_thresh = self.line_thresh,
                               cwd = self.cwd)
            df = datos.generated_df
            rutas_trabajadas = datos.rutas_trabajadas
            rutas_no_trabajadas = datos.rutas_no_trabajadas
            #print(f'Ruta -> {datos._ruta} \n Validación -> {datos._validacion}')
            #self._logger.info(f'Ruta -> {datos._ruta} \n Validación -> {datos._validacion}')
            #if datos.errores > 0:
            #    for errores in datos.errores_prompt:
            #        self._logger.info(f'{errores} || Mes: {mes} || Subsector: {subsector}')
            #rutas_trabajadas.append(datos._ruta)
        #except KeyError as e:
        #    e_prompt = f'--Error! -> Falta columna {e} en {mes}'
        #    self._logger.error(e_prompt)
        #except OSError as e:
        #    print(e)
        #    self._logger.error(e)
        #except IndexError as e:
        #    e_prompt = f'--Error! -> Archivo no existe ({e})'
        #    self._logger.error(e_prompt)
        #finally:
        #    if e_prompt != '': raise Exception(e_prompt)
        except Exception as e:
            self._logger.error(f'ExtPosMid_extraccion => {e}')
            
        #Si falla aquí es porque el codigo esta tomando un valor que no debería, por ejemplo una entidad en blanco
        df['Codigos'] = df['Subsector'] + ' ' + df['Entidad']
        df['Codigos'] = df['Codigos'].apply(lambda x: x.strip())
        df['Fecha'] = pd.to_datetime(df['Fecha'])  
        df = df.assign(Periodicidad=lambda x: x.apply(lambda row: 'Diaria' if row['Dia'][0:3] == 'DIA' else ('Mensual' if row['Mes'] == 'Mensual' else 'Other'), axis=1))
        
        #Mejorar esto
        rutas_todas = datos.rutas
        self._logger.info(f'Cantidad de Rutas Trabajadas: {len(rutas_trabajadas)}\nRutas Totales: {len(rutas_todas)}')
        print(f'Cantidad de Rutas Trabajadas: {len(rutas_trabajadas)}\nRutas Totales: {len(rutas_todas)}')
        if len(rutas_trabajadas) == len(rutas_todas):
            print('SUCCESS! -> Todas las rutas fueron trabajadas con éxito..')
            self._logger.info('SUCCESS! -> Todas las rutas fueron trabajadas con éxito..')
        else:
            rutas_no_trabajadas = []
            for ruta in rutas_todas:
                if not ruta in rutas_trabajadas:
                    rutas_no_trabajadas.append(ruta)
                    #print(rutas_no_trabajadas)
                    self._logger.info(f'Rutas no trabajadas => {rutas_no_trabajadas}')
       
        return df

    def posicion(self) -> pd.DataFrame:
        e_prompt = ''
        try:
            df = self.datos if self.ext == True else pd.read_excel(self.file)
            pnme = PNME(df, include = 'none', type = self.type, cwd = self.cwd)
        except ValueError as e:
            e_prompt = f'Revisar tipos de cambio => {e}'
            self._logger.error(e_prompt)
        except Exception as e:
            e_prompt = f'Error calculando posición => {e}'
            self._logger.error(e_prompt)
        finally:
            if e_prompt != '':
                raise Exception(e_prompt)
            else:
                return pnme

    def exportar(self, datos: pd.DataFrame, df_type: str) -> None:
        e_prompt = ''
        try:
            nombre = self.n_ext if df_type == 'extraccion' else self.n_pos if df_type == 'posicion' else None
            df = self.datos if df_type == 'extraccion' else self.pnme if df_type == 'posicion' else None
            if nombre == '' or df.empty:
                self._logger.error('Error iniciando exportado')
                raise Exception('Error iniciando exportado')
            ruta = os.path.join(self.cwd, nombre)
            if self.type == 'update':
                df_read = pd.read_excel(ruta)
                df_export = pd.concat([df_read, df])
                df_export.to_excel(ruta)
            elif self.type == 'new':
                df.to_excel(ruta)       
        except Exception as e:
            e_prompt = f'Error en exportación => {e}'
            self._logger.error(e_prompt)
        finally:
            if e_prompt != '': raise Exception(e_prompt)
        
    def mes_select(self, mes: str) -> str:
        if mes in ['01', '1']:
            return 'ENE'
        if mes in ['02', '2']:
            return 'FEB'
        if mes in ['03', '3']:
            return 'MAR'
        if mes in ['04', '4']:
            return 'ABR'
        if mes in ['05', '5']:
            return 'MAY'
        if mes in ['06', '6']:
            return 'JUN'
        if mes in ['07', '7']:
            return 'JUL'
        if mes in ['08', '8']:
            return 'AGO'
        if mes in ['09', '9']:
            return 'SEP'
        if mes in ['10', '10']:
            return 'OCT'
        if mes in ['11', '11']:
            return 'NOV'
        if mes in ['12', '12']:
            return 'DIC'

    def get_folder_path(self) -> str:
        # Get the path to the user's home directory
        home = pathlib.Path.home()

        # Construct the path to the desktop
        desktop = home / "Desktop"

        # Check if the desktop path exists; this is useful for OS's with different desktop paths
        if not desktop.exists():
            # Alternative approach for systems where the desktop might have a different name
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        
        if not os.path.exists(desktop):
            folder_path = os.path.join(home, 'cxbcLogs')
        else:
            folder_path = os.path.join(desktop, 'cxbcLogs')
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
                
        return folder_path
    
    def crear_logger(self) -> None:
        #desktop = self.get_folder_path()
        _logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        self._fileHandler = logging.FileHandler("{0}/{1}.log".format(self.cwd, 'process_start'), mode = 'w', encoding = 'utf-8')
        self._fileHandler.setFormatter(_logFormatter)
        self._logger.addHandler(self._fileHandler)
        
    def cerrar_logger(self) -> None:
        self._logger.removeHandler(self._fileHandler)
        self._fileHandler.close()
    
    def errorHandler(self, prompt: str) -> None:
        self._logger.error(prompt)
        self.cerrar_logger()
        raise Exception(prompt)
    
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
            self._logger.error(f'{e} => {ruta}')
        
        return ruta