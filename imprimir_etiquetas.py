import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

import win32print
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

PASTA_DOWNLOAD = Path(
    r"C:\Users\Lenovo\Downloads\DownloadNotas"
)

PASTA_IMPRESSOS = PASTA_DOWNLOAD / "Impressos"

NOME_IMPRESSORA = "MDK-006"

SUMATRA = Path(
    r"C:\Users\Lenovo\AppData\Local\SumatraPDF\SumatraPDF.exe"
)

# Tempo que o arquivo precisa permanecer com o mesmo tamanho
# para considerarmos que o download terminou.
TEMPO_ESTABILIDADE = 1.5

# Tempo máximo esperando o download terminar
TIMEOUT_DOWNLOAD = 60


# ==========================================================
# FUNÇÕES
# ==========================================================

def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def log(mensagem):
    print(f"[{agora()}] {mensagem}", flush=True)


def verificar_impressora():

    try:
        impressora = win32print.OpenPrinter(NOME_IMPRESSORA)

        info = win32print.GetPrinter(impressora, 2)

        win32print.ClosePrinter(impressora)

        log("Impressora encontrada.")
        log(f"  Nome   : {info['pPrinterName']}")
        log(f"  Driver : {info['pDriverName']}")
        log(f"  Porta  : {info['pPortName']}")
        log(f"  Status : {info['Status']}")
        log(f"  Fila   : {info['cJobs']}")

        return True

    except Exception as erro:

        log("ERRO ao acessar a impressora.")
        log(f"Detalhes: {erro}")

        return False


def arquivo_estavel(caminho):

    try:

        tamanho1 = caminho.stat().st_size

        time.sleep(TEMPO_ESTABILIDADE)

        tamanho2 = caminho.stat().st_size

        return (
            tamanho1 == tamanho2
            and tamanho2 > 0
        )

    except (FileNotFoundError, PermissionError):

        return False


def aguardar_download(caminho):

    inicio = time.time()

    while time.time() - inicio < TIMEOUT_DOWNLOAD:

        if not caminho.exists():
            return False

        if arquivo_estavel(caminho):
            return True

        time.sleep(0.4)

    return False


def imprimir_pdf(caminho_pdf):

    log(f"Enviando para impressão: {caminho_pdf.name}")

    comando = [
        str(SUMATRA),
        "-silent",
        "-print-to",
        NOME_IMPRESSORA,
        "-print-settings",
        "noscale",
        str(caminho_pdf),
    ]

    try:

        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
        )

        if resultado.returncode == 0:

            log("Impressão enviada com sucesso.")

            return True

        else:

            log("ERRO na impressão.")

            if resultado.stderr:
                log(resultado.stderr.strip())

            return False

    except subprocess.TimeoutExpired:

        log("ERRO: tempo limite da impressão excedido.")

        return False

    except Exception as erro:

        log(f"ERRO inesperado: {erro}")

        return False


def mover_para_impressos(caminho_pdf):

    PASTA_IMPRESSOS.mkdir(
        parents=True,
        exist_ok=True
    )

    destino = PASTA_IMPRESSOS / caminho_pdf.name

    # Se já existir um arquivo com o mesmo nome,
    # cria outro nome para não sobrescrever.
    contador = 1

    while destino.exists():

        destino = (
            PASTA_IMPRESSOS
            / f"{caminho_pdf.stem}_{contador}{caminho_pdf.suffix}"
        )

        contador += 1

    shutil.move(
        str(caminho_pdf),
        str(destino)
    )

    log(f"PDF movido para Impressos.")


# ==========================================================
# MONITORAMENTO
# ==========================================================

class MonitorPDF(FileSystemEventHandler):

    def processar_pdf(self, caminho):

        caminho = Path(caminho)

        # Só interessa PDF
        if caminho.suffix.lower() != ".pdf":
            return

        # Ignora arquivos dentro de Impressos
        if PASTA_IMPRESSOS in caminho.parents:
            return

        log("")
        log("=" * 60)

        log(f"Novo PDF detectado:")
        log(f"  {caminho.name}")

        log("Aguardando o download terminar...")

        if not aguardar_download(caminho):

            log("ERRO: o download não terminou corretamente.")
            log("O arquivo não será impresso.")

            return

        log("Download concluído.")

        # Pequena margem de segurança
        time.sleep(0.5)

        # Imprime
        sucesso = imprimir_pdf(caminho)

        if sucesso:

            # Dá um pequeno tempo para o Windows
            # receber o trabalho na fila.
            time.sleep(0.5)

            try:

                mover_para_impressos(caminho)

            except Exception as erro:

                log(
                    f"AVISO: impressão feita, "
                    f"mas não foi possível mover o PDF: {erro}"
                )

        else:

            log("PDF NÃO foi movido para Impressos.")
            log("Ele permanece na pasta para nova tentativa.")

        log("=" * 60)
        log("")


    def on_created(self, event):

        if event.is_directory:
            return

        self.processar_pdf(event.src_path)


    def on_moved(self, event):

        if event.is_directory:
            return

        self.processar_pdf(event.dest_path)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    print("")
    print("=" * 60)
    print("       AUTOMAÇÃO DE ETIQUETAS - OLIST")
    print("=" * 60)
    print("")

    log(f"Pasta monitorada:")
    log(f"  {PASTA_DOWNLOAD}")

    log("")

    log(f"Impressora:")
    log(f"  {NOME_IMPRESSORA}")

    log("")

    # Verifica pasta
    if not PASTA_DOWNLOAD.exists():

        log("ERRO: pasta de download não existe.")

        sys.exit(1)

    # Verifica Sumatra
    if not SUMATRA.exists():

        log("ERRO: SumatraPDF não encontrado.")
        log(f"Caminho esperado: {SUMATRA}")

        sys.exit(1)

    log("SumatraPDF encontrado.")

    log("")

    # Verifica impressora
    if not verificar_impressora():

        sys.exit(1)

    # Cria pasta Impressos
    PASTA_IMPRESSOS.mkdir(
        parents=True,
        exist_ok=True
    )

    log("")
    log("=" * 60)
    log("STATUS: ATIVO")
    log("Aguardando novos PDFs...")
    log("Pressione CTRL+C para parar.")
    log("=" * 60)
    log("")

    # Configura monitor
    evento = MonitorPDF()

    observador = Observer()

    observador.schedule(
        evento,
        str(PASTA_DOWNLOAD),
        recursive=False
    )

    observador.start()

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        log("")
        log("Encerrando automação...")

        observador.stop()

    observador.join()

    log("Automação encerrada.")


if __name__ == "__main__":
    main()