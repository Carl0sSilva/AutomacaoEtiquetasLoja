import win32print

NOME = "MDK-006"

handle = win32print.OpenPrinter(NOME)

info = win32print.GetPrinter(handle, 2)

print("Impressora encontrada!")
print()
print("Nome:", info["pPrinterName"])
print("Driver:", info["pDriverName"])
print("Porta:", info["pPortName"])
print("Status:", info["Status"])
print("Trabalhos na fila:", info["cJobs"])

win32print.ClosePrinter(handle)