from ProcesamientoCOESTI import ProcesamientoCOESTI
from VisualizadorMapa import VisualizadorMapa

if __name__ == "__main__":
    # Entrada de Excel de COESTI
    procesador = ProcesamientoCOESTI('datos_entrada/Data_COESTI.xlsx')

    # Procesamiento de data de COESTI
    procesador.preProcesarData()

    # Se obtiene el data frame con toda la data necesaria
    dataFrame = procesador.dataFrame
    print(dataFrame.to_string())

    print('Mostrando localización de estaciones...')
    visualizador = VisualizadorMapa(dataFrame)
    visualizador.visualizarEstaciones()
