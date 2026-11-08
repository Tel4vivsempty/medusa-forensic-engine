#!/bin/bash
# MEDUSA - Instalable en cualquier parte
set -e
echo "[1/4] Creando venv..."
python -m venv .venv
source .venv/bin/activate
echo "[2/4] Instalando deps..."
pip install -r scripts/requirements.txt
echo "[3/4] Compilando core C++..."
cd core && make && cd ..
echo "[4/4] Probando debate..."
python engine/debate.py
echo "Listo. Corre: python engine/variants/app_A_strict.py"
