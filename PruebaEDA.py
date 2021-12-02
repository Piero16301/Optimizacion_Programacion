import pandas as pd

from pandas_profiling import ProfileReport

dataFrame = pd.read_excel('datos_salida/Recorrido_Estaciones_Unidades.xlsx')

designReport = ProfileReport(dataFrame)
designReport.to_file('datos_salida/Reporte_Recorrido_Estaciones_Unidades.html')
