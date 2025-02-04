import fitz  # PyMuPDF
import os
import pytesseract
from PIL import Image as PilImage
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox

caminho_tesseract = r"C:\Program Files\Tesseract-OCR" #o "r" antes (raw string), serve pra dizer pro python que não quer que leia nada como um char especial, quer que leia do jeito que está
pytesseract.pytesseract.tesseract_cmd = caminho_tesseract + r"\tesseract.exe"
caminho_arquivo_txt = r"F:\pdfada\arquivo.txt"

caminho_final_arquivos = ""
caminho_arquivo_pdf = ""

def pdf_para_imagem():
    if not os.path.exists(caminho_final_arquivos):    
        os.makedirs(caminho_final_arquivos, exist_ok=True)
    else:
        pass
   
    arquivo_pdf = fitz.open(caminho_arquivo_pdf)

    for numero_pagina in range(len(arquivo_pdf)):
        pagina = arquivo_pdf[numero_pagina]
        imagem = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))
        caminho_imagem = os.path.join(caminho_final_arquivos, f"pagina_{numero_pagina + 1}.jpg")
        imagem.save(caminho_imagem)
        print(f"Página {numero_pagina + 1} salva como {caminho_imagem}")
    arquivo_pdf.close()
    print("Conversão concluída com sucesso")

def imagem_para_texto():
    global caminho_arquivo_txt
    caminho_arquivo_txt = os.path.join(caminho_final_arquivos, "arquivo.txt")
    if not os.path.exists(caminho_final_arquivos):
        os.makedirs(caminho_final_arquivos, exist_ok=True)
    else:
        arquivos_ordenados = sorted(
        (arquivo for arquivo in os.listdir(caminho_final_arquivos) if arquivo.startswith("pagina_") and arquivo.endswith(".jpg")),
        key=lambda x: int(''.join(filter(str.isdigit, x))))
        for arquivo in arquivos_ordenados:
            caminho_imagem = os.path.join(caminho_final_arquivos, arquivo)
            if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
                print(f"Imagem encontrada: {caminho_imagem}")
                imagens = PilImage.open(caminho_imagem)
                texto = pytesseract.image_to_string(imagens, lang="por")
                with open(caminho_arquivo_txt, "a", encoding="utf-8") as arquivo:
                    arquivo.write(texto)
                print(("Texto adicionado com sucesso"))

def selecionar_caminho_final_arquivos():
    global caminho_final_arquivos
    caminho_final_arquivos = fd.askdirectory()
    if caminho_final_arquivos:
       label_saida_arquivos.config(text=f"{caminho_final_arquivos}")

def selecionar_caminho_arquivo_pdf():
    global caminho_arquivo_pdf
    caminho_arquivo_pdf = fd.askopenfilename()
    if caminho_arquivo_pdf:
       label_pdf.config(text=f"{caminho_arquivo_pdf}")       

def converter():
    if not caminho_final_arquivos:
        messagebox.showerror("Erro", "Nenhum diretório selecionado!")
        return #return serve para parar a função caso a condição não seja satisfeita, sem return, tentaria rodar e daria erro
    if not caminho_arquivo_pdf:
        messagebox.showerror("Erro", "Nenhum arquivo PDF selecionado!")
        return 
    messagebox.showinfo("Conversão", "Iniciando conversão")
    pdf_para_imagem()
    imagem_para_texto()
    messagebox.showinfo("Sucesso", "Conversão concluída com sucesso!")

window = tk.Tk()
window.title("Imagem para PDF")
window.geometry("400x200")
window.resizable(False, False)

title = tk.Label(window, text="PDF to IMAGE to TXT", font=("Calibri 20 bold"))
title.pack()

label_frame = tk.LabelFrame(window, borderwidth=2)
label_frame.pack()
label_local_saida_arquivos = tk.Label(label_frame, text="Diretório de saída: ")
label_local_saida_arquivos.grid(row=0, column=0, sticky="w")
label_saida_arquivos = tk.Label(label_frame, text="Nenhuma pasta selecionada", wraplength=300)
label_saida_arquivos.grid(row=1, column=1, sticky="w")
botao_saida_arquivos = ttk.Button(label_frame, text="Selecionar diretório", command=selecionar_caminho_final_arquivos, width=18)
botao_saida_arquivos.grid(row=1, column=0, sticky="w", pady=1, padx=2)
label_local_arquivo_pdf = tk.Label(label_frame, text="Arquivo PDF:")
label_local_arquivo_pdf.grid(row=2, column=0, sticky="w")
botao_arquivo_pdf = ttk.Button(label_frame, text="Selecionar arquivo", command=selecionar_caminho_arquivo_pdf, width=18)
botao_arquivo_pdf.grid(row=3, column=0, sticky="w", pady=(0, 4), padx=2)
label_pdf = tk.Label(label_frame, text="Nenhum arquivo selecionado", wraplength=300)
label_pdf.grid(row=3, column=1, sticky="w")
botao_converter_pdf_para_imagem = ttk.Button(window, text="Converter", width=22, command=converter)
botao_converter_pdf_para_imagem.pack(pady=2)

window.mainloop()

#Uso de Pillow - básico
#Uso de cv2 - avançado