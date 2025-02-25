import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog

def conectar_db(nome_db):
    conn = sqlite3.connect(nome_db)
    return conn

def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarefa TEXT NOT NULL,
        concluida INTEGER NOT NULL DEFAULT 0,
        prazo TEXT
    )
    ''')
    conn.commit()

def adicionar_tarefa(conn, tarefa, prazo):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tarefas (tarefa, prazo) VALUES (?, ?)', (tarefa, prazo))
    conn.commit()

def remover_tarefa(conn, id_tarefa):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
    conn.commit()

def listar_tarefas(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas')
    return cursor.fetchall()

def marcar_concluida(conn, id_tarefa):
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET concluida = 1 WHERE id = ?', (id_tarefa,))
    conn.commit()

def atualizar_lista():
    for widget in frame_tarefas.winfo_children():
        widget.destroy()
    
    tarefas = listar_tarefas(conn)
    for tarefa in tarefas:
        status = "Concluída" if tarefa[2] == 1 else "Pendente"
        tarefa_label = Label(frame_tarefas, text=f"{tarefa[0]}. {tarefa[1]} - Prazo: {tarefa[3]} - Status: {status}")
        tarefa_label.pack()

def adicionar_tarefa_interface():
    tarefa = entrada_tarefa.get()
    prazo = entrada_prazo.get()
    if tarefa and prazo:
        adicionar_tarefa(conn, tarefa, prazo)
        entrada_tarefa.delete(0, END)
        entrada_prazo.delete(0, END)
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")

def remover_tarefa_interface():
    try:
        id_tarefa = int(entrada_id.get())
        remover_tarefa(conn, id_tarefa)
        entrada_id.delete(0, END)
        atualizar_lista()
    except ValueError:
        messagebox.showwarning("Aviso", "Por favor, insira um ID válido.")

def marcar_concluida_interface():
    try:
        id_tarefa = int(entrada_id.get())
        marcar_concluida(conn, id_tarefa)
        entrada_id.delete(0, END)
        atualizar_lista()
    except ValueError:
        messagebox.showwarning("Aviso", "Por favor, insira um ID válido.")

root = Tk()
root.title("To-Do List")

# Solicitar o nome do banco de dados
nome_db = simpledialog.askstring("Nome do Banco de Dados", "Digite o nome do banco de dados (ex: todo_list.db):")
if not nome_db:
    nome_db = 'todo_list.db'  # Nome padrão se o usuário não fornecer

conn = conectar_db(nome_db)
criar_tabela(conn)

frame_tarefas = Frame(root)
frame_tarefas.pack(pady=10)

frame_adicionar = Frame(root)
frame_adicionar.pack(pady=10)

Label(frame_adicionar, text="Tarefa:").grid(row=0, column=0)
entrada_tarefa = Entry(frame_adicionar, width=30)
entrada_tarefa.grid(row=0, column=1)

Label(frame_adicionar, text="Prazo (YYYY-MM-DD HH:MM):").grid(row=1, column=0)
entrada_prazo = Entry(frame_adicionar, width=30)
entrada_prazo.grid(row=1, column=1)

Button(frame_adicionar, text="Adicionar Tarefa", command=adicionar_tarefa_interface).grid(row=2, columnspan=2)

frame_remover = Frame(root)
frame_remover.pack(pady=10)

Label(frame_remover, text="ID da Tarefa:").grid(row=0, column=0)
entrada_id = Entry(frame_remover, width=30)
entrada_id.grid(row=0, column=1)

Button(frame_remover, text="Remover Tarefa", command=remover_tarefa_interface).grid(row=1, column=0)
Button(frame_remover, text="Marcar como Concluída", command=marcar_concluida_interface).grid(row=1, column=1)

frame_tarefas = Frame(root)
frame_tarefas.pack(pady=10)

atualizar_lista()

root.mainloop()