import win32print

NOME_IMPRESSORA = "MDK-006"

try:
    impressora = win32print.OpenPrinter(NOME_IMPRESSORA)

    info = win32print.GetPrinter(impressora, 2)

    print("=" * 50)
    print("IMPRESSORA ENCONTRADA")
    print("=" * 50)
    print(f"Nome   : {info['pPrinterName']}")
    print(f"Driver : {info['pDriverName']}")
    print(f"Porta  : {info['pPortName']}")
    print(f"Status : {info['Status']}")
    print(f"Fila   : {info['cJobs']}")

    win32print.ClosePrinter(impressora)

except Exception as e:
    print("ERRO:")
    print(e)

input("\nPressione ENTER para fechar...")