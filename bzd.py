import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

def connect_db():
    return sqlite3.connect('bzd.db')

def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bzd (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL
            )
        ''')

def read_records(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bzd')
    rows = cursor.fetchall()
    if rows:
        records = "\n".join([f"ID: {row[0]}, Текст: {row[1]}" for row in rows])
        messagebox.showinfo("Записи в базе данных", records)
    else:
        messagebox.showinfo("Записи в базе данных", "Нет записей в базе данных.")

def insert_record(conn):
    content = simpledialog.askstring("Новая запись", "Введите текст для новой записи:")
    if content:
        with conn:
            conn.execute('INSERT INTO bzd (content) VALUES (?)', (content,))
        messagebox.showinfo("Успех", "Запись успешно добавлена.")

def modify_record(conn):
    record_id = simpledialog.askinteger("Изменение записи", "Введите ID записи для изменения:")
    new_content = simpledialog.askstring("Изменение записи", "Введите новый текст для записи:")
    if record_id is not None and new_content:
        with conn:
            conn.execute('UPDATE bzd SET content = ? WHERE id = ?', (new_content, record_id))
        messagebox.showinfo("Успех", "Запись успешно изменена.")
    else:
        messagebox.showwarning("Ошибка", "Введите корректные данные.")

def delete_record(conn):
    record_id = simpledialog.askinteger("Удаление записи", "Введите ID записи для удаления:")
    if record_id is not None:
        with conn:
            conn.execute('DELETE FROM bzd WHERE id = ?', (record_id,))
        messagebox.showinfo("Успех", "Запись успешно удалена.")
    else:
        messagebox.showwarning("Ошибка", "Введите корректный ID.")

def main():
    conn = connect_db()
    create_table(conn)

    root = tk.Tk()
    root.title("BZD->SQL")
    root.geometry("1000x1000")  # Размер окна установлен на 800х800

    btn_insert = tk.Button(root, text="Добавить запись", command=lambda: insert_record(conn))
    btn_insert.pack(pady=10)

    btn_read = tk.Button(root, text="Прочитать записи", command=lambda: read_records(conn))
    btn_read.pack(pady=10)

    btn_modify = tk.Button(root, text="Изменить запись", command=lambda: modify_record(conn))
    btn_modify.pack(pady=10)

    btn_delete = tk.Button(root, text="Удалить запись", command=lambda: delete_record(conn))
    btn_delete.pack(pady=10)

    btn_exit = tk.Button(root, text="Выход", command=root.quit)
    btn_exit.pack(pady=10)

    root.mainloop()
    conn.close()


if __name__ == "__main__":
    main()
