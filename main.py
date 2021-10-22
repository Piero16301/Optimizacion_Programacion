from timeit import default_timer as timer

from ProcesamientoCOESTI import ProcesamientoCOESTI
from ProcesamientoExterno import ProcesamientoExterno
from ProcesamientoRestricciones import ProcesamientoRestricciones
from ProcesamientoDirecciones import ProcesamientoDirecciones

from VisualizadorMapa import VisualizadorMapa

if __name__ == "__main__":
    # Inicio de tiempo
    inicio = timer()

    # Archivos de Excel de entrada
    # procesadorDirecciones = ProcesamientoDirecciones('datos_entrada/Direcciones_Estaciones.xlsx')
    procesadorCOESTI = ProcesamientoCOESTI('datos_entrada/Pedidos_COESTI.xlsx')
    procesadorExterno = ProcesamientoExterno('datos_entrada/Pedidos_Externos.xlsx')
    procesadorRestricciones = ProcesamientoRestricciones('datos_entrada/Restricciones_Estaciones.xlsx')

    # Procesamiento de data
    # procesadorDirecciones.procesarData()
    procesadorCOESTI.procesarData()
    procesadorExterno.procesarData()
    procesadorRestricciones.procesarData()

    # Se obtiene el data frame con toda la data necesaria
    dataFrameCOESTI = procesadorCOESTI.dataFrame
    dataFrameExterno = procesadorExterno.dataFrame
    dataFrameRestricciones = procesadorRestricciones.dataFrame

    # Mostrar datos de Data Frames
    # print('\n================ Data Frame Direcciones ================\n')
    # print(dataFrameDirecciones.to_string())
    print('\n================ Data Frame COESTI ================\n')
    print(dataFrameCOESTI.to_string())
    print('\n================ Data Frame Externo ================\n')
    print(dataFrameExterno.to_string())
    print('\n================ Data Frame Restricciones ================\n')
    print(dataFrameRestricciones.to_string())

    # print('Mostrando localización de estaciones...')
    visualizador = VisualizadorMapa(dataFrameCOESTI)
    visualizador.visualizarEstaciones()

    # Fin de tiempo
    fin = timer()
    print('Tiempo total:', round(fin - inicio, 2), 'segundos')
