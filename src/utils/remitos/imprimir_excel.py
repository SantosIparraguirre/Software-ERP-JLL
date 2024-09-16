import win32com.client

def imprimir_excel(ruta_archivo):
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False

    try:
        workbook = excel.Workbooks.Open(ruta_archivo)
        workbook.ActiveSheet.PrintOut()
    finally:
        workbook.Close(SaveChanges=False)
        excel.Quit()