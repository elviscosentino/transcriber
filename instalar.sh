#!/bin/bash

clear
echo
echo "============================================================"
echo
echo "Instalador do sistema de transcrição de áudio."
echo "Criado por Elvis Cosentino"
echo
echo "============================================================"
echo

sudo apt install python3
sudo apt install python3-tk
sudo apt install python3-pip
pip install ffmpeg-python
pip install openai-whisper

#curl -O https://raw.githubusercontent.com/elviscosentino/transcriber/main/transcriber.py
wget https://raw.githubusercontent.com/elviscosentino/transcriber/main/transcriber.py
chmod +x transcriber.py

echo
echo "============================================================"
echo
echo "Instalação concluída!"
echo
echo "============================================================"
echo
