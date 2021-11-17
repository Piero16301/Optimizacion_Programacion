import pandas as pd


def cargarExcel(nombreExcel, nombreHoja, encabezado):
    # Lectura inicial archivo Excel
    excel = pd.read_excel(nombreExcel, sheet_name=nombreHoja, header=encabezado)
    dataFrame = pd.DataFrame(excel)

    return dataFrame


class ProcesamientoRestricciones:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel
        self.dataFrame = pd.DataFrame()

    def organizarData(self, hoja):
        dataFrameInicial = cargarExcel(self.rutaExcel, hoja, 0)

        return dataFrameInicial

    def procesarData(self):
        # Organizar data del Excel inicial
        self.dataFrame = self.organizarData('Lima')
