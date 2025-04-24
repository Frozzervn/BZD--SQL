import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

def create_table(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS bzd (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            priority INTEGER
        )
    ''')

def connect_db():
    con = sqlite3.connect('bzd1.db')
    create_table(con)
    return con

conn = connect_db()

def recreate_table(conn):
    with conn:
        conn.execute('DROP TABLE IF EXISTS bzd')
        create_table(conn)

def fetch_records(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bzd')
    return cursor.fetchall()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_records(conn):
        tree.insert('', tk.END, values=row)

def add_record():
    content = simpledialog.askstring("Новая запись", "Введите текст для новой записи:")
    priority = simpledialog.askinteger("Приоритет", "Введите приоритет (число):", initialvalue=2)
    if content and priority is not None:
        with conn:
            conn.execute('INSERT INTO bzd (content, priority) VALUES (?, ?)', (content, priority))
        refresh_table()

def modify_record():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите запись для изменения")
        return
    item = tree.item(selected)
    record_id = item['values'][0]
    current_content = item['values'][1]
    current_priority = item['values'][2]

    newcontent = simpledialog.askstring("Изменение текста", "Введите новый текст:", initialvalue=current_content)
    newpriority = simpledialog.askinteger("Изменение приоритета", "Введите новый приоритет:", initialvalue=current_priority)

    if newcontent is not None and newpriority is not None:
        with conn:
            conn.execute('UPDATE bzd SET content = ?, priority = ? WHERE id = ?', (newcontent, newpriority, record_id))
        refresh_table()

def delete_record():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите запись для удаления")
        return
    record_id = tree.item(selected)['values'][0]
    with conn:
        conn.execute('DELETE FROM bzd WHERE id = ?', (record_id,))
    refresh_table()

conn = connect_db()
create_table(conn)

root = tk.Tk()
root.title("BZD->SQL")
root.geometry("700x400")

columns = ("ID", "Текст", "Приоритет")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True)

refresh_table()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Добавить", command=add_record).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Изменить", command=modify_record).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Удалить", command=delete_record).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Обновить", command=refresh_table).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Выход", command=root.quit).grid(row=0, column=4, padx=5)

root.mainloop()
conn.close()
