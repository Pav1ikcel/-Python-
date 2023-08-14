import json
import datetime
import os

NOTES_FILE = "notes.json"

class Note:
    def __init__(self, id, title, body, created_at, updated_at):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at

class NoteApp:
    def __init__(self):
        self.notes = []
        self.next_id = 1
        self.load_notes()

    def add_note(self, title, body):
        note = Note(
            id=self.next_id,
            title=title,
            body=body,
            created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self.next_id += 1
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, id, title, body):
        for note in self.notes:
            if note.id == id:
                note.title = title
                note.body = body
                note.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return
        print(f"Заметка с ID {id} не найдена.")

    def delete_note(self, id):
        to_remove = None
        for note in self.notes:
            if note.id == id:
                to_remove = note
                break
        if to_remove:
            self.notes.remove(to_remove)
            self.save_notes()
        else:
            print(f"Заметка с ID {id} не найдена.")

    def list_notes(self):
        for note in self.notes:
            print(f"{note.id}: {note.title}")

    def view_note_details(self, id):
        for note in self.notes:
            if note.id == id:
                print(f"Заголовок: {note.title}")
                print(f"Тело: {note.body}")
                print(f"Дата создания: {note.created_at}")
                print(f"Дата обновления: {note.updated_at}")
                return
        print(f"Заметка с ID {id} не найдена.")

    def load_notes(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as file:
                data = json.load(file)
                self.notes = [Note(**note_data) for note_data in data]
                self.next_id = max(note.id for note in self.notes) + 1

    def save_notes(self):
        with open(NOTES_FILE, "w") as file:
            data = [{'id': note.id, 'title': note.title, 'body': note.body,
                     'created_at': note.created_at, 'updated_at': note.updated_at}
                    for note in self.notes]
            json.dump(data, file, default=str)

if __name__ == "__main__":
    note_app = NoteApp()
    while True:
        print("1. Добавить заметку")
        print("2. Редактировать заметку")
        print("3. Удалить заметку")
        print("4. Список заметок")
        print("5. Просмотр заметки")
        print("0. Выход")
        
        choice = input("Введите номер команды: ")
        
        if choice == "1":
            title = input("Введите заголовок заметки: ")
            body = input("Введите тело заметки: ")
            note_app.add_note(title, body)
            print("Заметка успешно сохранена")
        elif choice == "2":
            id = int(input("Введите ID заметки для редактирования: "))
            title = input("Введите новый заголовок заметки: ")
            body = input("Введите новое тело заметки: ")
            note_app.edit_note(id, title, body)
        elif choice == "3":
            id = int(input("Введите ID заметки для удаления: "))
            note_app.delete_note(id)
        elif choice == "4":
            note_app.list_notes()
        elif choice == "5":
            id = int(input("Введите ID заметки для просмотра: "))
            note_app.view_note_details(id)
        elif choice == "0":
            break
        else:
            print("Некорректная команда. Пожалуйста, выберите правильный номер команды.")
