from timeit import default_timer as timer

from ProcesamientoCOESTI import ProcesamientoCOESTI
from VisualizadorMapa import VisualizadorMapa

if __name__ == "__main__":
    # Inicio de tiempo
    inicio = timer()

    # Entrada de Excel de COESTI
    procesador = ProcesamientoCOESTI('datos_entrada/Pedidos_COESTI.xlsx')

    # Procesamiento de data de COESTI
    procesador.preProcesarData()

    # Se obtiene el data frame con toda la data necesaria
    dataFrame = procesador.dataFrame
    print(dataFrame.to_string())

    print('Mostrando localización de estaciones...')
    visualizador = VisualizadorMapa(dataFrame)
    visualizador.visualizarEstaciones()

    # Fin de tiempo
    fin = timer()
    print('Tiempo total:', round(fin - inicio, 2), 'segundos')
