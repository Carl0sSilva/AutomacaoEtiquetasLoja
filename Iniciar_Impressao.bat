@echo off
title Automacao de Impressao - Olist
color 0A

:: Entra na pasta onde o script esta salvo
cd /d "C:\OlistAutomacao"

:: Executa o script Python
python imprimir_etiquetas.py

:: Se o programa fechar por algum erro, pausa a tela para conseguir ler o motivo
echo.
echo O programa foi encerrado.
pause
