import dash
from dash import dcc
from dash import html
from timeit import default_timer as timer
import time

from ProcesamientoCOESTI import ProcesamientoCOESTI
from ProcesamientoExterno import ProcesamientoExterno
from ProcesamientoRestricciones import ProcesamientoRestricciones
from ProcesamientoDirecciones import ProcesamientoDirecciones
from ProcesamientoUnidades import ProcesamientoUnidades
from ProcesamientoRutas import ProcesamientoRutas
from VisualizadorMapa import VisualizadorMapa

separador = '='

if __name__ == "__main__":
    # Inicio de tiempo
    inicio = timer()

    horaInicio = time.localtime()
    print(separador * 45, 'INICIANDO EL PROGRAMA', separador * 45)
    print(' ' * 50, time.strftime('%I:%M:%S %p', horaInicio), '\n')

    # Archivos de Excel de entrada
    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print('{0: <60}'.format('1. Lectura de datos'),
          separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
          )

    procesadorDirecciones = ProcesamientoDirecciones('datos_entrada/Direcciones_Estaciones.xlsx')
    procesadorCOESTI = ProcesamientoCOESTI('datos_entrada/Pedidos_COESTI.xlsx')
    procesadorExterno = ProcesamientoExterno('datos_entrada/Pedidos_Externos.xlsx')
    procesadorUnidades = ProcesamientoUnidades('datos_entrada/Detalle_Unidades.xlsx')
    procesadorRestricciones = ProcesamientoRestricciones('datos_entrada/Restricciones_Estaciones.xlsx')

    # Procesamiento de data
    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print(
        '{0: <60}'.format('   1.1. Leyendo direcciones'),
        separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
    )
    procesadorDirecciones.procesarData()

    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print(
        '{0: <60}'.format('   1.2. Leyendo pedidos de COESTI'),
        separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
    )
    procesadorCOESTI.procesarData()

    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print(
        '{0: <60}'.format('   1.3. Leyendo pedidos externos'),
        separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
    )
    procesadorExterno.procesarData()

    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print(
        '{0: <60}'.format('   1.4. Leyendo detalles de unidades'),
        separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
    )
    procesadorUnidades.procesarData()

    print(
        '{0: <60}'.format('   1.5. Leyendo restricciones de estaciones'),
        separador * 30, '    ', '{0: >7}'.format(str(round(timer() - inicio, 3))), 'segundos'
    )
    procesadorRestricciones.procesarData()

    # Se obtiene el data frame con toda la data necesaria
    dataFrameDirecciones = procesadorDirecciones.dataFrame
    dataFrameCOESTI = procesadorCOESTI.dataFrame
    dataFrameExterno = procesadorExterno.dataFrame
    dataFrameRestricciones = procesadorRestricciones.dataFrame

    # Calcular las rutas de las unidades
    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print('{0: <61}'.format('\n2. Procesamiento de rutas'),
          separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
          )

    procesadorRutas = ProcesamientoRutas(dataFrameCOESTI, dataFrameExterno)
    procesadorRutas.calcularRutas(separador, inicio, maximosIntentosRecorrido=False)

    # Se muestran las estaciones en el mapa
    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print('{0: <61}'.format('\n3. Graficación de rutas'),
          separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
          )

    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print('{0: <60}'.format('   3.1. Cargando grafo de la ciudad'),
          separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
          )
    visualizador = VisualizadorMapa(caminosPrecisos=True, rutasDirectas=True)

    visualizador.visualizarEstaciones(separador, inicio)

    # Fin de tiempo
    tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
    print('{0: <61}'.format('\n4. Término de todos los cálculos'),
          separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
          )

    horaFin = time.localtime()
    print('\n' + separador * 44, 'FINALIZANDO EL PROGRAMA', separador * 44)
    print(' ' * 50, time.strftime('%I:%M:%S %p', horaFin))

    # # Server para mostrar el mapa
    # app = dash.Dash()
    #
    # app.layout = html.Div(children=[
    #     # Alto y ancho seteado para Chrome 1080p
    #     dcc.Graph(style={'width': '98vw', 'height': '97.5vh'}, figure=visualizador.mapa)
    # ])
    #
    # app.run_server(host='0.0.0.0', port=80)
