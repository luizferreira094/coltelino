@echo off
setlocal enabledelayedexpansion

:: Nome do modelo
set MODEL_NAME=mobsearch

:: Caminho da pasta de arquivos
set DATA_PATH=curated_files

echo ======================================
echo 1. Criando UNICHARSET...
echo ======================================
for %%F in (%DATA_PATH%\*.box) do (
    unicharset_extractor %%F
    if !errorlevel! neq 0 (
        echo Erro ao processar %%F
        exit /b !errorlevel!
    )
)

echo ======================================
echo 2. Treinando modelo...
echo ======================================
for %%F in (%DATA_PATH%\*.tr) do (
    shapeclustering -F %DATA_PATH%\font_properties -U unicharset %%F
    mftraining -F %DATA_PATH%\font_properties -U unicharset %%F
    cntraining %%F

    if !errorlevel! neq 0 (
        echo Erro no treinamento de %%F
        exit /b !errorlevel!
    )
)

:: Renomeando arquivos de saída
move inttemp %MODEL_NAME%.inttemp
move normproto %MODEL_NAME%.normproto
move pffmtable %MODEL_NAME%.pffmtable
move shapetable %MODEL_NAME%.shapetable

echo ======================================
echo 3. Gerando TRAINEDDATA...
echo ======================================
combine_tessdata %DATA_PATH%\%MODEL_NAME%.

if !errorlevel! neq 0 (
    echo Erro ao gerar traineddata!
    exit /b !errorlevel!
)

:: Move o modelo para a pasta do Tesseract
move %DATA_PATH%\%MODEL_NAME%.traineddata %TESSDATA_PREFIX%\%MODEL_NAME%.traineddata

echo ======================================
echo TREINAMENTO FINALIZADO!
echo O arquivo %MODEL_NAME%.traineddata está pronto para uso.
echo ======================================
pause