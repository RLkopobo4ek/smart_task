from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QTextEdit, QApplication, QLineEdit, QListWidget, QLabel, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QWidget
import json
app = QApplication([])

notes = {
    'Добро пожаловать!':{
        "текст": "Это приложение для заметок",
        "теги":['добро', 'инструкция']
    }
}


with open('notes_data.json', 'w') as file:
    json.dump(notes, file)

notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки') # - Создание окна
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

button_create = QPushButton('Создать заметку')
button_del = QPushButton('Удалить заметку')
button_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('ВВедите тег')
field_text = QTextEdit()

button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_find = QPushButton('Искать заметки по тегу')

list_tags = QListWidget()
List_Tags_label = QLabel('Список тегов')

layouts_note = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_create)
row_1.addWidget(button_del)

row_2 = QHBoxLayout()
row_2.addWidget(button_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(List_Tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_4 = QHBoxLayout()

row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4.addWidget(button_tag_find)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layouts_note.addLayout(col_1, stretch=2)
layouts_note.addLayout(col_2, stretch=1)
notes_win.setLayout(layouts_note)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'название заметки:')
    if ok and note_name != '':
        notes[note_name] = {'текст': '', 'теги': []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])
        print(notes)



def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для удаления не выбрана!')

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('заметка для сохранения не выбрана!')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('заметка для тега не выбрана!')

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Тег для удаления не выбран!')


def search_tag():
    print(button_tag_find.text())
    tag = field_tag.text()
    if button_tag_find.text() == 'Искать заметки по тегу' and tag:
        print(tag)
        notes_filter = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filter[note] = notes[note]
        button_tag_find.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filter)
        print(button_tag_find.text())
    elif button_tag_find.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_find.setText('Искать заметки по тегу')
        print(button_tag_find.text())
    else:
        pass



def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])


list_notes.itemClicked.connect(show_note)
button_save.clicked.connect(save_note)
button_create.clicked.connect(add_note)
button_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_find.clicked.connect(search_tag)

notes_win.show()
with open('notes_data.json', 'r') as file:
    notes = json.load(file)



list_notes.addItems(notes)

notes_win.show()
app.exec_()

