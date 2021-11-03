from timeit import default_timer as timer

from ProcesamientoCOESTI import ProcesamientoCOESTI
from ProcesamientoExterno import ProcesamientoExterno
from ProcesamientoRestricciones import ProcesamientoRestricciones
from ProcesamientoDirecciones import ProcesamientoDirecciones
from ProcesamientoUnidades import ProcesamientoUnidades
from ProcesamientoRutas import ProcesamientoRutas

from VisualizadorMapa import VisualizadorMapa

import dash
from dash import dcc
from dash import html


# Server para mostrar el mapa
app = dash.Dash()
server = app.server


if __name__ == "__main__":
    # Inicio de tiempo
    inicio = timer()

    # Archivos de Excel de entrada
    procesadorDirecciones = ProcesamientoDirecciones('datos_entrada/Direcciones_Estaciones.xlsx')
    procesadorCOESTI = ProcesamientoCOESTI('datos_entrada/Pedidos_COESTI.xlsx')
    procesadorExterno = ProcesamientoExterno('datos_entrada/Pedidos_Externos.xlsx')
    # procesadorRestricciones = ProcesamientoRestricciones('datos_entrada/Restricciones_Estaciones.xlsx')
    procesadorUnidades = ProcesamientoUnidades('datos_entrada/Detalle_Unidades.xlsx')

    # Procesamiento de data
    procesadorDirecciones.procesarData()
    procesadorCOESTI.procesarData()
    procesadorExterno.procesarData()
    # procesadorRestricciones.procesarData()
    procesadorUnidades.procesarData()

    # Se obtiene el data frame con toda la data necesaria
    dataFrameDirecciones = procesadorDirecciones.dataFrame
    dataFrameCOESTI = procesadorCOESTI.dataFrame
    dataFrameExterno = procesadorExterno.dataFrame
    # dataFrameRestricciones = procesadorRestricciones.dataFrame

    # Mostrar datos de Data Frames
    # print('\n\n================ Data Frame Direcciones ================\n')
    # print(dataFrameDirecciones.to_string())
    # print('\n\n================ Data Frame COESTI ================\n')
    # print(dataFrameCOESTI.to_string())
    # print('\n\n================ Data Frame Externo ================\n')
    # print(dataFrameExterno.to_string())
    # print('\n\n================ Data Frame Restricciones ================\n')
    # print(dataFrameRestricciones.to_string())

    # Calcular las rutas de las unidades
    procesadorRutas = ProcesamientoRutas(dataFrameCOESTI, dataFrameExterno)
    origenes, destinos, unidades = procesadorRutas.calcularRutas()

    # Se muestran las estaciones en el mapa
    print('Mostrando localización de estaciones...')
    visualizador = VisualizadorMapa(dataFrameDirecciones, origenes, destinos, unidades)
    visualizador.visualizarEstaciones('Cliente')

    # Fin de tiempo
    fin = timer()
    print('Tiempo total:', round(fin - inicio, 2), 'segundos')

    app.layout = html.Div(children=[
        # Alto y ancho seteado para Chrome 1080p
        dcc.Graph(style={'width': '98vw', 'height': '97.5vh'}, figure=visualizador.mapa)
    ])
    
    app.run_server(host='0.0.0.0', port='80')
