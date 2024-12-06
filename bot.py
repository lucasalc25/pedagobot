import time
import keyboard
import pyautogui
from tkinter import filedialog, messagebox
import tkinter as tk
import os
from automacao.planilhas import filtrar_faltosos
from automacao.ocr import esperar_elemento, localizar_elemento
from pathlib import Path

def criar_pastas():
    # Obtém o caminho da pasta Documentos do usuário
    caminho_documentos = Path.home() / "Documents"
    
    # Define o caminho completo da nova pasta
    caminho_pasta_easylog = os.path.join(caminho_documentos, 'EasyLog')
    caminho_pasta_planilhas = os.path.join(caminho_pasta_easylog, 'Planilhas')
    
    pasta_easylog = 'EasyLog'
    pasta_planilhas = 'Planilhas'
    
    # Cria a pasta, se ela não existir
    if not os.path.exists(caminho_pasta_easylog):
        os.makedirs(caminho_pasta_easylog)
        print(f"Pasta '{pasta_easylog}' criada em {caminho_documentos}")
    else:
        print(f"A pasta '{pasta_easylog}' já existe em {caminho_documentos}")
        
    # Cria a pasta, se ela não existir
    if not os.path.exists(caminho_pasta_planilhas):
        os.makedirs(caminho_pasta_planilhas)
        print(f"Pasta '{pasta_planilhas}' criada em {caminho_pasta_easylog}")
    else:
        print(f"A pasta '{pasta_planilhas}' já existe em {caminho_pasta_easylog}")

def repetir_tecla(*teclas, total_repeticoes):
    """
    Pressiona uma ou mais teclas repetidamente.
    
    :param teclas: Teclas a serem pressionadas (pode ser uma ou mais).
    :param total_repeticoes: Número de vezes que as teclas serão pressionadas.
    """
    for _ in range(total_repeticoes):
        if len(teclas) == 1:  # Apenas uma tecla
            pyautogui.press(teclas[0])
        else:  # Mais de uma tecla
            pyautogui.hotkey(*teclas)
        time.sleep(0.2)
    
# Função para anexar arquivo
def anexar_planilha(campo_planilha):
    caminho_planilha = filedialog.askopenfilename(title="Selecione uma planilha", filetypes=[("Arquivos do Excel", "*.xlsx")])
    if caminho_planilha:
        campo_planilha.delete(0, tk.END)
        campo_planilha.insert(0, caminho_planilha)

# Função para anexar imagem
def anexar_imagem(imagem):
    caminho = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg")]
    )
    if caminho:
        imagem.delete(0, tk.END)  # Limpa o conteúdo atual
        imagem.insert(0, caminho)  # Exibe o caminho do arquivo
                
def preparar_data_faltosos(campo_data_inicial, campo_data_final):
    data_inicial = campo_data_inicial.get("1.0", tk.END)
    data_final = campo_data_final.get("1.0", tk.END)
    
    messagebox.showinfo("Atenção!", "Certifique-se de ter feito o login no HUB!")
    
    pyautogui.hotkey('alt','tab')
    time.sleep(1)
    
    esperar_elemento("./imagens/hub_aberto.png")
    
    gerar_faltosos_e_educadores(data_inicial, data_final) 

       
def gerar_faltosos_e_educadores(data_inicial, data_final):
    messagebox.showinfo("Atenção!", "Certifique-se de ter feito o login no HUB!")
    
    repeticoes = 0
    while not localizar_elemento("./imagens/hub_aberto.png"):
        if repeticoes > 1:
            # Pressiona 'Alt' e 'Tab' duas vezes mantendo 'Alt' pressionado
            pyautogui.keyDown('alt')  # Mantém a tecla 'Alt' pressionada
            repetir_tecla('tab', total_repeticoes=repeticoes)
            pyautogui.keyUp('alt')  # Mantém a tecla 'Alt' pressionada
        else:
            pyautogui.hotkey('alt','tab')

        repeticoes += 1
        time.sleep(2) 

    pyautogui.press('alt')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    repetir_tecla('tab', total_repeticoes=3)
    pyautogui.press('enter')
    time.sleep(1)

    esperar_elemento('./imagens/faltas_por_periodo.png')
    keyboard.write(str(data_inicial))
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    keyboard.write(str(data_final))

    pesquisar_faltosos = localizar_elemento('./imagens/pesquisar.png')
    pyautogui.click(pesquisar_faltosos)

    esperar_elemento('./imagens/lista_faltosos.png')
    exportar_faltosos = localizar_elemento('./imagens/exportar.png')
    pyautogui.click(exportar_faltosos)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    caminho_planilhas = Path.home() / "Documents" / "EasyLog" / "Planilhas" / "alunos_e_educadores.png"
    caminho_planilhas = os.path.normpath(caminho_planilhas)
    campo_nome_planilha = localizar_elemento('./imagens/campo_nome_planilha.png')
    pyautogui.click(campo_nome_planilha)
    time.sleep(1)
    pyautogui.write(caminho_planilhas)
    time.sleep(1)
    salvar = localizar_elemento('./imagens/salvar.png')
    pyautogui.click(salvar)
    time.sleep(2)
    
    if localizar_elemento('./imagens/substituir_arquivo.png'):
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
    
    messagebox.showinfo("Atenção!", "Planilha de alunos e educadores gerada!")
        
def gerar_faltosos(data_inicial, data_final):  
    gerar_faltosos_e_educadores(data_inicial, data_final)
        
    pyautogui.press('alt')
    time.sleep(1)
    repetir_tecla('tab', total_repeticoes=7)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    
    esperar_elemento('./imagens/presencas_e_faltas.png')
    pyautogui.write(data_inicial)
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.write(data_final)
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('space')
    time.sleep(1)
    visualizar = localizar_elemento('./imagens/visualizar.png')
    pyautogui.click(visualizar)
    
    esperar_elemento('./imagens/visu_presencas_e_faltas.png')
    pyautogui.press('alt')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    repetir_tecla('tab', total_repeticoes=3)
    pyautogui.press('right')
    time.sleep(1)
    repetir_tecla('tab', total_repeticoes=5)
    pyautogui.press('enter')
    time.sleep(1)
    
    esperar_elemento('./imagens/opcoes_exportacao.png')
    pyautogui.press('enter')
    time.sleep(1)
    
    caminho_planilha = Path.home() / "Documents" / "EasyLog" / "Planilhas" / "faltosos.xls"
    caminho_planilha = os.path.normpath(caminho_planilha)
    campo_nome_planilha = localizar_elemento('./imagens/campo_nome_planilha.png')
    pyautogui.click(campo_nome_planilha)
    time.sleep(1)
    pyautogui.write(caminho_planilha)
    time.sleep(1)
    salvar = localizar_elemento('./imagens/salvar.png')
    pyautogui.click(salvar)
    time.sleep(2)
    
    if localizar_elemento('./imagens/substituir_arquivo.png'):
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        
    esperar_elemento('./imagens/abrir_planilha.png')
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    messagebox.showinfo("Atenção!", "Planilha de faltosos gerada!")
    
    filtrar_faltosos(caminho_planilha)

     
        
        
    
    