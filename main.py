import pandas as pd

if __name__ == "__main__":
    data = pd.read_excel('REPORTE_COESTI.XLSX', sheet_name='SUGERIDO COESTI')
    print(data)
