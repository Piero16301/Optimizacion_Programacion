import pandas as pd


def cargarExcel(nombreExcel, nombreHoja, encabezado):
    # Lectura inicial archivo Excel
    excel = pd.read_excel(nombreExcel, sheet_name=nombreHoja, header=encabezado)
    dataFrame = pd.DataFrame(excel)

    return dataFrame


def organizarData(dataCOESTI):
    # Lectura inicial archivo Excel de COESTI
    dataFrameInicial = cargarExcel(dataCOESTI, 'CL', None)

    # Se eliminan filas y columnas no necesarias
    filtroFilas = dataFrameInicial.iloc[9:836, 1:37]
    nombresColumnas = ['Centro', 'JOP', 'GOP', 'Transportes', 'Zona', 'Departamento', 'Distrito', 'Estación',
                       'Material', 'Descripción', 'Producto', 'Concatenado', 'Capacidad DGH', 'Inventario Max Deseado',
                       'Muerto', 'Varilla', 'Descarga', 'Stock Operativo', 'VTA Promedio Emergencia', 'X 1', 'X 2',
                       'VTA Promedio %', 'VTA Día 04', 'VTA Día 05', 'Incremento VTA', 'Días Stock Emergencia',
                       'VTA Normal', 'Días Stock Normal', 'Pedido', 'Sugerido', 'Días Stock 1', 'Días Stock 2', 'Y 1',
                       'Cantidad Aproximada Carga', 'Observación', 'Z 1']

    # Asignación de encabezados de todas las columnas
    dataFrameEncabezado = pd.DataFrame(filtroFilas)
    dataFrameEncabezado.columns = nombresColumnas

    return dataFrameEncabezado


def aplicarFiltros(dataFrameEncabezado):
    # Filtro de filas de zona Lima
    dataFiltroZona = dataFrameEncabezado[dataFrameEncabezado['Zona'] == 'LIMA']

    # Filtro de filas con cantidad sugerida diferente de nulo
    dataFiltroSugerido = dataFiltroZona[dataFiltroZona['Sugerido'].notna()]

    # Reiniciar los índices de las filas
    indicesReiniciados = dataFiltroSugerido.reset_index(drop=True)

    return indicesReiniciados


def guardarExcel(indicesReiniciados, nombreExcel):
    # Guardar como Excel
    indicesReiniciados.to_excel(nombreExcel, index=False, header=True)
