# 🖨️ Automação de Impressão de Etiquetas e Notas (Olist / E-commerce)

Script em Python desenvolvido para agilizar a operação de expedição e embalagem de pedidos. O sistema monitora uma pasta específica em tempo real e, assim que o download de um arquivo PDF (nota fiscal ou etiqueta de envio) é concluído, envia o documento diretamente para a impressora térmica/padrão de forma silenciosa e organiza os arquivos já impressos.

---

## 📁 Estrutura do Projeto

```text
📦 automacao-impressao-olist
 ┣ 📜 imprimir_etiquetas.py          # Script principal de monitoramento e impressão automática
 ┣ 📜 Iniciar_Impressao.bat # Atalho executável para iniciar o sistema com dois cliques
 ┣ 📜 teste_fila.py         # Utilitário interativo para checar status e fila da impressora
 ┗ 📜 teste_impressora.py   # Utilitário rápido de diagnóstico de conexão com a impressora
```

---

## 🚀 Funcionalidades

* **Monitoramento em Tempo Real:** Detecta instantaneamente novos arquivos `.pdf` criados ou movidos para a pasta de downloads configurada.
* **Verificação de Integridade do Download:** Aguarda o arquivo estabilizar de tamanho antes de iniciar a impressão, evitando erros com arquivos corrompidos ou pela metade.
* **Impressão Silenciosa:** Utiliza o **SumatraPDF** via linha de comando (`-silent` e `noscale`) para imprimir sem abrir janelas e sem redimensionar etiquetas térmicas.
* **Validação e Diagnóstico de Hardware:** Verifica se a impressora está instalada e acessível antes de iniciar, além de contar com scripts auxiliares para testes rápidos.
* **Organização Automática:** Após o envio bem-sucedido para a fila de impressão, move o PDF para a subpasta `Impressos`, renomeando automaticamente caso já exista um arquivo com o mesmo nome (evitando sobrescrita).

---

## 📋 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado no Windows:

1. **Python 3.8+**
2. **SumatraPDF** (usado para a impressão silenciosa em linha de comando).
3. Uma impressora devidamente configurada no Windows (ex: impressora térmica de etiquetas).

### Bibliotecas Python necessárias

Instale as dependências executando o comando abaixo no terminal:

```bash
pip install watchdog pywin32
```

---

## ⚙️ Configuração

No início do script principal (`impressao.py`), ajuste as constantes de acordo com o ambiente da sua máquina:

```python
# Caminho da pasta onde os PDFs são baixados
PASTA_DOWNLOAD = Path(r"C:\Users\Lenovo\Downloads\DownloadNotas")

# Subpasta para onde os arquivos irão após serem impressos
PASTA_IMPRESSOS = PASTA_DOWNLOAD / "Impressos"

# Nome exato da impressora instalada no Windows
NOME_IMPRESSORA = "MDK-006"

# Caminho do executável do SumatraPDF
SUMATRA = Path(r"C:\Users\Lenovo\AppData\Local\SumatraPDF\SumatraPDF.exe")
```

> **Dica:** Para descobrir o nome exato da sua impressora, acesse *Painel de Controle > Dispositivos e Impressoras* no Windows.

---

## ▶️ Como Usar

### Opção 1: Execução rápida com 2 cliques (Recomendado para operação)

Para facilitar o uso diário pela equipe de expedição sem precisar abrir o terminal, utilize o arquivo `Iniciar_Impressao.bat`:

```bat
@echo off
title Automacao de Impressao - Olist
color 0A

:: Entra na pasta onde o script esta salvo (ajuste o caminho conforme sua maquina)
cd /d "C:\Caminho\Para\A\Pasta\Do\Seu\Projeto"

:: Executa o script Python
python imprimir_etiquetas.py

echo.
echo O programa foi encerrado.
pause
```

1. Ajuste o caminho da pasta dentro do `Iniciar_Impressao.bat`.
2. Crie um atalho dele na **Área de Trabalho** (ou coloque na pasta `shell:startup` para iniciar junto com o Windows).
3. Dê dois cliques para iniciar.

### Opção 2: Via Terminal

1. Abra o terminal (CMD ou PowerShell) na pasta do projeto.
2. Execute o script principal:

```bash
python imprimir_etiquetas.py
```

3. O console exibirá o status da impressora e entrará em modo de espera (`STATUS: ATIVO`).
4. Para encerrar o programa a qualquer momento, pressione `CTRL + C` no terminal.

---

## 🔍 Scripts de Diagnóstico (Testes)

Caso a impressora não esteja respondendo ou você queira validar o nome do dispositivo configurado no Windows, utilize os scripts auxiliares inclusos na pasta:

* **`teste_fila.py`**: Verifica a conexão com a impressora, exibe informações detalhadas (Nome, Driver, Porta, Status e quantidade de trabalhos na fila) e mantém a janela aberta até que você pressione `ENTER`. Ideal para rodar com dois cliques.
* **`teste_impressora.py`**: Executa a mesma verificação de forma direta no terminal, encerrando imediatamente após imprimir os dados na tela.

Para rodar pelo terminal:
```bash
python teste_fila.py
```

---

## 🛠️ Fluxo de Funcionamento

1. **Detecção:** O `watchdog` identifica um novo arquivo `.pdf` na pasta monitorada.
2. **Estabilização:** O script verifica o tamanho do arquivo a cada 1,5 segundos até confirmar que o navegador terminou o download (limite de 60 segundos).
3. **Impressão:** Envia o comando de impressão sem escala (`noscale`) para o SumatraPDF.
4. **Arquivamento:** Se a impressão retornar sucesso (`returncode == 0`), o arquivo é movido para a pasta `/Impressos`. Caso ocorra algum erro, o arquivo permanece na pasta raiz para não ser perdido.

---

## 📄 Licença

Este projeto é de uso livre para otimização de processos logísticos e operacionais. Sinta-se à vontade para adaptar e melhorar conforme a necessidade da sua operação!
