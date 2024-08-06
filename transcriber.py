#!/usr/bin/env python3

import whisper
import ffmpeg
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

# Função para selecionar arquivo via interface gráfica
def select_file():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    #file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("MOV files", "*.mov"),
            ("MKV files", "*.mkv"),
            ("Audio files", "*.mp3;*.wav"),
            ("Image files", "*.png;*.jpg;*.jpeg"),
            ("All files", "*.*")
        ]
    )
    return file_path

def clear_screen():
    # Identifica o sistema operacional e executa o comando apropriado
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para converter segundos em formato HH:MM:SS
def seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# Função para extrair o áudio de um arquivo de vídeo
#def extract_audio(video_path, output_audio_path):
#    ffmpeg.input(video_path).output(output_audio_path, acodec='aac', vn=None).overwrite_output().run()

def extract_audio(video_path, output_audio_path):
    # Usando subprocess para suprimir a saída do ffmpeg
    command = [
        'ffmpeg',
        '-y',  # Força a sobrescrição de arquivos de saída existentes
        '-i', video_path,
        '-acodec', 'aac',
        '-vn',  # Remove o vídeo da saída
        output_audio_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Função principal para transcrever o áudio com timestamps
def transcribe_with_timestamps(audio_path, model_name="small"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language="pt", verbose=False)

    output_txt = os.path.splitext(audio_path)[0] + "_transcription_with_timestamps.txt"
    with open(output_txt, "w") as f:
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            #f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
            start_time = seconds_to_hms(start)
            end_time = seconds_to_hms(end)
            #f.write(f"[{start_time} --> {end_time}] {text}\n")
            f.write(f"[{start_time}] {text}\n")


    print(f"Transcrição salva com sucesso em '{output_txt}'")

    # Excluir o arquivo de áudio após a transcrição
    #if os.path.isfile(audio_path):
    #    os.remove(audio_path)
        #print(f"Arquivo de áudio '{audio_path}' excluído.")

def show_completion_message():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    messagebox.showinfo("Concluído", "O processo foi concluído com sucesso!")
    root.destroy()  # Fecha a aplicação tkinter

# Fluxo principal
if __name__ == "__main__":
    clear_screen()
    print("Programa transcritor de áudio.")
    print("Desenvolvido por Elvis Cosentino.")
    print("")
    print("Por favor, selecione um arquivo de áudio ou vídeo na janela de seleção de arquivo.")
    video_path = select_file()
    if video_path:
        audio_path = os.path.splitext(video_path)[0] + ".aac"
        
        print("Extraindo áudio...")
        extract_audio(video_path, audio_path)
        
        print("Transcrevendo áudio...")
        transcribe_with_timestamps(audio_path)
        
        show_completion_message()  # Mostra a caixa de mensagem ao final

        print("Processo concluído.")
    else:
        print("Nenhum arquivo selecionado.")
