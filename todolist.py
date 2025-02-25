import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog, Toplevel
from tkcalendar import Calendar

def conectar_db(nome_db):
    conn = sqlite3.connect(nome_db)
    return conn

def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarefa TEXT NOT NULL,
        descricao TEXT,
        concluida INTEGER NOT NULL DEFAULT 0,
        prazo TEXT
    )
    ''')
    conn.commit()

def adicionar_tarefa(conn, tarefa, descricao, prazo):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tarefas (tarefa, descricao, prazo) VALUES (?, ?, ?)', (tarefa, descricao, prazo))
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

def marcar_pendente(conn, id_tarefa):
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET concluida = 0 WHERE id = ?', (id_tarefa,))
    conn.commit()

def atualizar_lista():
    for widget in frame_tarefas.winfo_children():
        widget.destroy()
    
    tarefas = listar_tarefas(conn)
    for tarefa in tarefas:
        status = "Concluída" if tarefa[3] == 1 else "Pendente"
        
        tarefa_frame = Frame(frame_tarefas)
        tarefa_frame.pack(pady=5)

        tarefa_label = Label(tarefa_frame, text=f"{tarefa[0]}. {tarefa[1]} - Prazo: {tarefa[4]} - Status: {status}")
        tarefa_label.pack(side=LEFT)

        btn_visualizar = Button(tarefa_frame, text="Visualizar", command=lambda id=tarefa[0]: visualizar_tarefa(id))
        btn_visualizar.pack(side=LEFT, padx=5)

        if tarefa[3] == 0:  # Se a tarefa não está concluída
            btn_alternar = Button(tarefa_frame, text="Marcar como Concluída", command=lambda id=tarefa[0]: marcar_concluida_interface(id))
        else:  # Se a tarefa está concluída
            btn_alternar = Button(tarefa_frame, text="Marcar como Pendente", command=lambda id=tarefa[0]: marcar_pendente_interface(id))

        btn_alternar.pack(side=LEFT, padx=5)

        btn_remover = Button(tarefa_frame, text="Remover", command=lambda id=tarefa[0]: remover_tarefa_interface(id))
        btn_remover.pack(side=LEFT, padx=5)

def adicionar_tarefa_interface():
    tarefa = entrada_tarefa.get()
    descricao = entrada_descricao.get("1.0", END).strip()
    prazo = cal.get_date()
    if tarefa and descricao:
        adicionar_tarefa(conn, tarefa, descricao, prazo)
        entrada_tarefa.delete(0, END)
        entrada_descricao.delete("1.0", END)
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")

def remover_tarefa_interface(id_tarefa):
    remover_tarefa(conn, id_tarefa)
    atualizar_lista()

def marcar_concluida_interface(id_tarefa):
    marcar_concluida(conn, id_tarefa)
    atualizar_lista()

def marcar_pendente_interface(id_tarefa):
    marcar_pendente(conn, id_tarefa)
    atualizar_lista()

def visualizar_tarefa(id_tarefa):
    cursor = conn.cursor()
    cursor.execute('SELECT tarefa, descricao, prazo FROM tarefas WHERE id = ?', (id_tarefa,))
    tarefa = cursor.fetchone()

    if tarefa:
        visualizacao = Toplevel(root)
        visualizacao.title("Visualizar Tarefa")

        Label(visualizacao, text="Título:").pack(pady=5)
        Label(visualizacao, text=tarefa[0]).pack(pady=5)

        Label(visualizacao, text="Descrição:").pack(pady=5)
        Label(visualizacao, text=tarefa[1]).pack(pady=5)

        Label(visualizacao, text="Prazo:").pack(pady=5)
        Label(visualizacao, text=tarefa[2]).pack(pady=5)

        Button(visualizacao, text="Fechar", command=visualizacao.destroy).pack(pady=10)

root = Tk()
root.title("To-Do List")

nome_db = simpledialog.askstring("Nome do Banco de Dados", "Digite o nome do banco de dados (ex: todo_list.db):")
if not nome_db:
    nome_db = 'todo_list.db'

conn = conectar_db(nome_db)
criar_tabela(conn)

frame_adicionar = Frame(root)
frame_adicionar.pack(pady=10)

Label(frame_adicionar, text="Tarefa:").grid(row=0, column=0)
entrada_tarefa = Entry(frame_adicionar, width=30)
entrada_tarefa.grid(row=0, column=1)

Label(frame_adicionar, text="Descrição:").grid(row=1, column=0)
entrada_descricao = Text(frame_adicionar, width=30, height=5)
entrada_descricao.grid(row=1, column=1)

Label(frame_adicionar, text="Prazo:").grid(row=2, column=0)
cal = Calendar(frame_adicionar, selectmode='day')
cal.grid(row=2, column=1)

Button(frame_adicionar, text="Adicionar Tarefa", command=adicionar_tarefa_interface).grid(row=3, columnspan=2)

frame_tarefas = Frame(root)
frame_tarefas.pack(pady=10)

atualizar_lista()

root.mainloop()
conn.close()