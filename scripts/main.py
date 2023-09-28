import tkinter as tk
import pandas as pd
from configparser import ConfigParser
from tkinter import ttk
import sys
from tkinter import filedialog

sys.path.insert(0, 'C:/work')
from library import pd_funcs as func
from library import classes_GUI as app_inter


def create_frame():
    """
    Создание фрейма
    Малкин Д.А.
    :return: None
    """
    global frame, root, bg1

    config = ConfigParser()
    config.read('C:\work\scripts\config.ini')

    bg1 = config.get('Color', 'bg_color')

    frame = tk.Frame(
        root,
        width='1024',
        height='720',
        bg=bg1
    )
    frame.pack()
    frame.propagate(False)


def create_app():
    """
    Малкин Д.А.
    :return:
    """
    global root, frame

    root = tk.Tk()

    root.geometry('1024x720')
    root.resizable(width=False, height=False)

    frame = tk.Frame(root)
    frame.pack()


def main_page():
    """
    Малкин Д.А.
    :return:
    главная страница
    """
    global frame, root

    frame.destroy()
    create_frame()

    button1 = app_inter.button(frame, 'Справочники', open_dict_menu)
    button2 = app_inter.button(frame, 'Отчет', open_rep_menu)
    button3 = app_inter.button(frame, 'Графики', open_graph_menu)
    button4 = app_inter.button(frame, 'Интерфейс', open_config_menu)

    button1.place(x=200, y=200)
    button2.place(x=400, y=200)
    button3.place(x=600, y=200)
    button4.place(x=600, y=500)


def open_config_menu():
    """
    Малкин Д.А.
    меню конфигурации
    def save - функция сохрангения
    :return:
    """
    global frame, root, bg1

    frame.destroy()
    create_frame()

    def save():
        """
        Малкин Д.А.
        :return:
        """
        value = entry.get()

        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')
        config.set('Color', 'bg_color', value)
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
        open_config_menu()

    select_name = app_inter.label_title(frame, 'Введите желаемый цвет фона на английском')
    entry = app_inter.entry(frame)
    button1 = app_inter.button(frame, 'Сохранить', save)
    back_button = app_inter.button(frame, 'Назад', main_page)
    select_name.place(x=80, y=100)
    entry.place(x=80, y=200)
    button1.place(x=80, y=250)
    back_button.place(x=700, y=600)

    print(bg1)


def open_dict_menu():
    """
    Малкин Д.А.
    :return:
    меню добавления редактирования и удаления
    """
    global frame, root

    frame.destroy()
    create_frame()

    add_button = app_inter.button(frame, 'Добавить', add_menu)
    delete_button = app_inter.button(frame, 'Удалить', delete_menu)
    edit_button = app_inter.button(frame, 'Редактировать', change_menu)
    back_button = app_inter.button(frame, 'Назад', main_page)

    add_button.place(x=200, y=200)
    delete_button.place(x=400, y=200)
    edit_button.place(x=600, y=200)
    back_button.place(x=600, y=600)


def add_menu():
    """
    Малкин Д.А.
    меню добавления
    :return:
    """
    global frame, root
    frame.destroy()
    create_frame()

    config = ConfigParser()
    config.read('C:\work\scripts\config.ini')

    path_model = config.get('Path', 'model_id_path')
    path_brand = config.get('Path', 'brand_path')
    path_discount = config.get('Path', 'discount_path')

    def update_table(*args):
        """
        Малкин Д.А.
        обновление таблицы
        :return:
        """
        dropdown_value = dropdown_var.get()
        if dropdown_value == '':
            return  # Выход из функции, если значение выпадающего меню пустое

        if dropdown_value == 'Models':
            columns = columns_MODELid
        elif dropdown_value == 'Brands':
            columns = columns_Brand
        else:
            columns = columns_Discount

        # Очистка существующих столбцов и данных из виджета ttk.Treeview
        tree["columns"] = columns
        tree.delete(*tree.get_children())

        # Чтение выбранного CSV-файла и вставка данных в виджет ttk.Treeview
        data = pd.read_csv(csv_dict[dropdown_value], delimiter=',', encoding='UTF-8')
        tree["columns"] = data.columns.tolist()  # Установка столбцов на основе столбцов данных

        for col in tree["columns"]:
            tree.heading(col, text=col)  # Установка заголовков столбцов

        for i, row in data.iterrows():
            tree.insert('', 'end', values=list(row))

    csv_dict = {'Models': path_model, 'Brands': path_brand,
                'Discounts': path_discount}

    columns_MODELid = ["ID", "Brand", "Season", "Type", "Quantity", "Price (USD)"]
    columns_Brand = ["Brand", "Location", "Category", "Phone"]
    columns_Discount = ["Season", "Discount"]

    dropdown_var = tk.StringVar()
    dropdown_var.trace('w', update_table)  # Call update_table function whenever dropdown value changes
    dropdown = tk.OptionMenu(frame, dropdown_var, "Models", "Brands", "Discounts")

    tree = ttk.Treeview(frame, columns=[], show="headings")
    select_name = app_inter.label_title(frame, 'Добавление')
    select_frame = app_inter.label_subtitle(frame, 'Выберите справочник')
    add_label = app_inter.label_subtitle(frame, 'Добавьте новую запись:')

    dropdown.config(width=14, font=('Helvetica', 18))

    entry = tk.Entry(frame, font=('Helvetica', 18, "bold"), highlightbackground='black', highlightthickness=1,
                     bg='white', width=18)

    def add_record():
        """
        Малкин Д.А.
        :return:
        """
        param = entry.get()
        func.add_func(csv_dict[dropdown_var.get()], param, True)
        update_table()

    add_button = app_inter.button(frame, 'Добавить', add_record)
    back_button = app_inter.button(frame, 'Назад', open_dict_menu)

    # Configure Treeview style and headings
    style = ttk.Style()
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=15,
                    fieldbackground="#D3D3D3"
                    )
    style.map("Treeview",
              background=[('selected', '#347083')])

    select_name.place(x=400, y=10)
    select_frame.place(x=150, y=100)
    dropdown.place(x=150, y=150)
    add_label.place(x=550, y=100)
    entry.place(x=550, y=150)
    add_button.place(x=550, y=200)
    back_button.place(x=700, y=600)
    tree.place(x=160, y=300, width=700)


def delete_menu():
    """
    Малкин Д.А.
    меню удаления
    :return:
    """
    global frame, root

    frame.destroy()
    create_frame()

    config = ConfigParser()
    config.read('C:\work\scripts\config.ini')

    path_model = config.get('Path', 'model_id_path')
    path_brand = config.get('Path', 'brand_path')
    path_discount = config.get('Path', 'discount_path')

    csv_dict = {'Models': path_model, 'Brands': path_brand,
                'Discounts': path_discount}

    def update_table(*args):
        """
        Малкин Д.А.
        обновление
        :return:
        """
        dropdown_value = dropdown_var.get()
        if dropdown_value == '':
            return  # Выход из функции, если значение выпадающего меню пустое

        if dropdown_value == 'Models':
            columns = columns_MODELid
        elif dropdown_value == 'Brands':
            columns = columns_Brand
        else:
            columns = columns_Discount

        # Очистка существующих столбцов и данных из виджета ttk.Treeview
        tree["columns"] = columns
        tree.delete(*tree.get_children())

        # Чтение выбранного CSV-файла и вставка данных в виджет ttk.Treeview
        data = pd.read_csv(csv_dict[dropdown_value], delimiter=',', encoding='UTF-8')
        tree["columns"] = data.columns.tolist()  # Установка столбцов на основе столбцов данных

        for col in tree["columns"]:
            tree.heading(col, text=col)  # Установка заголовков столбцов

        for i, row in data.iterrows():
            tree.insert('', 'end', values=list(row))

    columns_MODELid = ["ID", "Brand", "Season", "Type", "Quantity", "Price (USD)"]
    columns_Brand = ["Brand", "Location", "Category", "Phone"]
    columns_Discount = ["Season", "Discount"]

    dropdown_var = tk.StringVar()
    dropdown_var.trace('w', update_table)  # Call update_table function whenever dropdown value changes
    dropdown = tk.OptionMenu(frame, dropdown_var, "Models", "Brands", "Discounts")

    tree = ttk.Treeview(frame, columns=[], show="headings")
    select_name = app_inter.label_title(frame, 'Удаление')
    select_frame = app_inter.label_subtitle(frame, 'Выберите справочник')
    add_label = app_inter.label_subtitle(frame, 'Выберете окно \n для удаления')

    dropdown.config(width=14, font=('Helvetica', 18))

    entry = tk.Entry(frame, font=('Helvetica', 18, "bold"), highlightbackground='black', highlightthickness=1,
                     bg='white', width=18)

    # data = pd.read_csv('/Users/imac/Desktop/work/data/MODEL_ID.csv', delimiter=',', encoding='UTF-8')

    def delete_func():
        """
        Малкин Д.А.
        функция удаления
        :return:
        """
        param = entry.get()
        if param.isdigit():
            param = int(param)
        func.delete_func(csv_dict[dropdown_var.get()], param, True)
        update_table()

    # add_button = tk.Button(frame, text='Удалить', font=('Arial', 20), command=delete_func)

    # back_button = tk.Button(frame, text='Назад', font=('Arial', 26), command=open_dict_menu)

    add_button = app_inter.button(frame, 'Удалить', delete_func)
    back_button = app_inter.button(frame, 'Назад', open_dict_menu)

    style = ttk.Style()
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=15,
                    fieldbackground="#D3D3D3")
    style.map("Treeview",
              background=[('selected', '#347083')])

    select_name.place(x=420, y=10)
    select_frame.place(x=150, y=100)
    add_label.place(x=550, y=100)
    dropdown.place(x=150, y=200)
    entry.place(x=550, y=200)
    add_button.place(x=550, y=250)
    back_button.place(x=700, y=600)
    tree.place(x=160, y=350, width=700)

    update_table()

    tree.yview_moveto(0.0)


def change_menu():
    """
    меню редактирования
    Малкин Д.А.
    :return:
    """
    global frame, root

    frame.destroy()
    create_frame()

    config = ConfigParser()
    config.read('C:\work\scripts\config.ini')

    path_model = config.get('Path', 'model_id_path')
    path_brand = config.get('Path', 'brand_path')
    path_discount = config.get('Path', 'discount_path')

    csv_dict = {'Models': path_model, 'Brands': path_brand,
                'Discounts': path_discount}

    def update_table(*args):
        """
        Малкин Д.А.
        :return:
        """
        dropdown_value = dropdown_var.get()
        if dropdown_value == '':
            return  # Выход из функции, если значение выпадающего меню пустое

        if dropdown_value == 'Models':
            columns = columns_MODELid
        elif dropdown_value == 'Brands':
            columns = columns_Brand
        else:
            columns = columns_Discount

        # Очистка существующих столбцов и данных из виджета ttk.Treeview
        tree["columns"] = columns
        tree.delete(*tree.get_children())

        # Чтение выбранного CSV-файла и вставка данных в виджет ttk.Treeview
        data = pd.read_csv(csv_dict[dropdown_value], delimiter=',', encoding='UTF-8')
        tree["columns"] = data.columns.tolist()  # Установка столбцов на основе столбцов данных

        for col in tree["columns"]:
            tree.heading(col, text=col)  # Установка заголовков столбцов

        for i, row in data.iterrows():
            tree.insert('', 'end', values=list(row))

    columns_MODELid = ["ID", "Brand", "Season", "Type", "Quantity", "Price (USD)"]
    columns_Brand = ["Brand", "Location", "Category", "Phone"]
    columns_Discount = ["Season", "Discount"]

    dropdown_var = tk.StringVar()
    dropdown_var.trace('w', update_table)  # Call update_table function whenever dropdown value changes
    dropdown = tk.OptionMenu(frame, dropdown_var, "Models", "Brands", "Discounts")

    tree = ttk.Treeview(frame, columns=[], show="headings")
    entry = tk.Entry(frame, font=('Helvetica', 18, "bold"), highlightbackground='black', highlightthickness=1,
                     bg='white', width=18)

    def change_record():
        """
        Малкин Д.А.
        замена записи
        :return:
        """
        param = entry.get()
        func.inplace_function(csv_dict[dropdown_var.get()], param, True)
        update_table()

    select_name = app_inter.label_title(frame, 'Редактирование')
    select_frame = app_inter.label_subtitle(frame, 'Выберите справочник')
    add_label1 = app_inter.label_subtitle(frame, 'Выберите поле')
    add_label2 = app_inter.label_subtitle(frame, 'для редактирования')

    dropdown.config(width=14, font=('Helvetica', 18))

    add_button = app_inter.button(frame, 'Редактировать', change_record)
    back_button = app_inter.button(frame, 'Назад', open_dict_menu)

    # Configure Treeview style and headings
    style = ttk.Style()
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=15,
                    fieldbackground="#D3D3D3")
    style.map("Treeview",
              background=[('selected', '#347083')])

    # Set initial columns based on default dropdown value
    update_table()

    # Перемещение полосы прокрутки в начало
    tree.yview_moveto(0.0)

    select_name.place(x=350, y=10)
    select_frame.place(x=150, y=100)
    add_label1.place(x=550, y=100)
    add_label2.place(x=550, y=140)
    dropdown.place(x=150, y=200)
    entry.place(x=550, y=200)
    add_button.place(x=550, y=250)
    back_button.place(x=700, y=600)
    tree.place(x=160, y=350, width=700)


def otchet1():
    """
    Беседин И.Д.
    Формирование структуры первого отчета
    :return:
    """
    global frame, root

    frame.destroy()
    create_frame()

    config = ConfigParser()
    config.read('C:\work\scripts\config.ini')
    path_model = config.get('Path', 'model_id_path')
    path_brand = config.get('Path', 'brand_path')
    path_discount = config.get('Path', 'discount_path')
    path = config.get('Path', 'output_path')

    csv_dict = {'Models': path_model, 'Brands': path_brand,
                'Discounts': path_discount}

    def save_in():
        """
        сохранение
        Малкин Д.А.
        :return:
        """
        # Открытие диалогового окна для выбора файла и пути сохранения
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV Files", "*.csv"),
                                                           ("xlsx Files", "*.xlsx"),
                                                           ("All Files", "*.*")])
        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        original_path = config.get('Path', 'basic_report_path')
        data_frame = pd.read_csv(original_path, index_col=0)

        if filename:
            # Сохранение таблицы в выбранный файл
            try:
                if '.csv' in filename:
                    data_frame.to_csv(filename)
                else:
                    data_frame.to_excel(filename)
            except:
                print("Ошибка", "Невозможно сохранить файл!")

    def addotchhet():
        """
        Беседин И.Д.
        Добавление первого отчета
        :return:
        """
        func.basic_rep(csv_dict['Models'], csv_dict['Discounts'], csv_dict['Brands'], True, path)

        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        original_path = config.get('Path', 'basic_report_path')

        columns = ["MODEL_ID", "Brand", "Season", "Type", "Quantity", "Price (USD)", "Discount", "Location", "Category"]
        data = pd.read_csv(original_path, delimiter=',', encoding='UTF-8')

        # Создание таблицы Treeview для отображения данных
        style = ttk.Style()
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=15,
                        fieldbackground="#D3D3D3")
        style.map("Treeview",
                  background=[('selected', '#347083')])

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)  # Установка ширины столбца
        save_button = app_inter.button(frame, 'Сохранить', save_in)
        save_button.place(x=200, y=600)

        tree.place(x=70, y=300)  # Размещение таблицы с использованием place

        # Отображение всех строк в Treeview
        for i, row in data.iterrows():
            tree.insert('', 'end', values=list(row))

    title = app_inter.label_title(frame, 'Объединённая таблица')
    title.place(x=300, y=10)

    otchet_button = app_inter.button(frame, 'Открыть отчет', addotchhet)
    otchet_button.place(x=200, y=200)
    back_button = app_inter.button(frame, 'Назад', open_rep_menu)
    back_button.place(x=700, y=600)


def otchet2():
    """
    отчет 2
    Создание второго отчета
    Беседин И.Д.
    :return:
    """
    global frame, root

    frame.destroy()
    create_frame()

    def save_in():
        """
        Беседин И.Д.
        :return:
        """
        # Открытие диалогового окна для выбора файла и пути сохранения
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV Files", "*.csv"),
                                                           ("xlsx Files", "*.xlsx")])

        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        original_path = config.get('Path', 'pivot_table_custommean')
        data_frame = pd.read_csv(original_path, index_col=0)

        if filename:
            # Сохранение таблицы в выбранный файл
            try:
                if '.csv' in filename:
                    data_frame.to_csv(filename)
                else:
                    data_frame.to_excel(filename)
            except:
                print("Ошибка", "Невозможно сохранить файл!")

    def custom_otchet():
        """
        Кастомизация отчета, формирование окна
        Беседин И.Д.
        :return:
        """
        global frame, root

        frame.destroy()
        create_frame()

        def generation():
            """
            Беседин И.Д.
            Генерация кастомизированного отчета
            :return:
            """
            config = ConfigParser()
            config.read('C:\work\scripts\config.ini')

            path = config.get('Path', 'output_path')

            basic_rep = config.get('Path', 'basic_report_path')

            basic_rep_custom_path = config.get('Path', 'pivot_table_custom')

            custom_kist = []
            param1 = entry1.get()
            custom_kist.append(param1)
            param2 = entry2.get()
            custom_kist.append(param2)
            param3 = entry3.get()
            custom_kist.append(param3)
            param4 = entry4.get()
            custom_kist.append(param4)

            func.custom_pivot(basic_rep, True, path, custom_kist)
            columns = ["", "", "", ""]
            data = pd.read_csv(basic_rep_custom_path, delimiter=',', encoding='UTF-8')

            # Создание таблицы Treeview для отображения данных
            style = ttk.Style()
            style.configure("Treeview",
                            background="white",
                            foreground="black",
                            rowheight=15,
                            fieldbackground="#D3D3D3")
            style.map("Treeview",
                      background=[('selected', '#347083')])

            tree = ttk.Treeview(frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
                # Установка ширины столбца
            save_button = app_inter.button(frame, 'Сохранить', save_in)
            save_button.place(x=400, y=200)

            tree.place(x=100, y=500)  # Размещение таблицы с использованием grid

            # Отображение всех строк в Treeview
            for i, row in data.iterrows():
                tree.insert('', 'end', values=list(row))

        # select_frame = app_inter.label_subtitle(frame, 'Выберите справочник')
        # add_label = app_inter.label_subtitle(frame, 'Выберете окно \n для удаления')

        add_label = app_inter.label_subtitle(frame, 'Ввод данных')

        # entry1_label = app_inter.label_subtitle(frame, "Введите в каждую ячейку значение для кастомизированного отчёта")
        entry1_label = tk.Label(frame, text="Введите в каждую ячейку значение \n для кастомизированного отчёта",
                                font=('Helvetica', 28))

        entry1 = app_inter.entry(frame)

        entry2 = app_inter.entry(frame)
        entry3 = app_inter.entry(frame)

        entry4 = app_inter.entry(frame)

        generate_button = app_inter.button(frame, 'Сгенерировать', generation)
        back_button = app_inter.button(frame, 'Назад', open_rep_menu)

        add_label.place(x=350, y=10)
        entry1_label.place(x=100, y=100)
        entry1.place(x=100, y=200)
        entry2.place(x=100, y=250)
        entry3.place(x=100, y=300)
        entry4.place(x=100, y=350)
        generate_button.place(x=100, y=400)
        back_button.place(x=700, y=400)

    title = app_inter.label_title(frame, 'Сводная таблица')
    title.place(x=330, y=10)
    otchet_button = app_inter.button(frame, 'Ввести данные', custom_otchet)
    otchet_button.place(x=200, y=200)
    back_button = app_inter.button(frame, 'Назад', open_rep_menu)
    back_button.place(x=700, y=600)


def otchet3():
    """
    Создание 3 отчета
    Беседин И.Д.
    :return:
    """
    global frame, root

    frame.destroy()
    create_frame()

    def save_in1():
        """
        Малкин Д.А.
        Сохранение первого отчета
        :return:
        """
        # Открытие диалогового окна для выбора файла и пути сохранения
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV Files", "*.csv"),
                                                           ("xlsx Files", "*.xlsx")])

        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        original_path = config.get('Path', 'stat_path')
        data_frame = pd.read_csv(original_path, index_col=0)

        if filename:
            # Сохранение таблицы в выбранный файл
            try:
                if '.csv' in filename:
                    data_frame.to_csv(filename)
                else:
                    data_frame.to_excel(filename)
            except:
                print("Ошибка", "Невозможно сохранить файл!")

    def save_in2():
        """
        Малкин Д.А.
        Сохранение второго отчета
        :return:
        """
        # Открытие диалогового окна для выбора файла и пути сохранения
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV Files", "*.csv"),
                                                           ("xlsx Files", "*.xlsx")])

        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        original_path = config.get('Path', 'stat_path')
        data_frame = pd.read_csv(original_path, index_col=0)

        if filename:
            # Сохранение таблицы в выбранный файл
            try:
                if '.csv' in filename:
                    data_frame.to_csv(filename)
                else:
                    data_frame.to_excel(filename)
            except:
                print("Ошибка", "Невозможно сохранить файл!")

    def describe_otchet1():
        """
        Беседин И.Д.
        :return:
        """
        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        path = config.get('Path', 'output_path')
        original_path = config.get('Path', 'basic_report_path')

        stat_path = config.get('Path', 'stat_path')

        func.describe_func(original_path, True, path)

        columns = ["Brand", "cout", "mean", "std", "min", "max"]
        data = pd.read_csv(stat_path, delimiter=',', encoding='UTF-8')

        # Создание таблицы Treeview для отображения данных
        style = ttk.Style()
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=15,
                        fieldbackground="#D3D3D3")
        style.map("Treeview",
                  background=[('selected', '#347083')])

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)  # Установка ширины столбца

        save_button1 = app_inter.button(frame, 'Сохранить1', save_in1)
        save_button1.place(x=200, y=600)
        tree.place(x=350, y=120)  # Размещение таблицы с использованием place

        # Отображение всех строк в Treeview
        for i, row in data.iterrows():
            tree.insert('', 'end', values=list(row))

    def describe_otchet2():
        """
        Беседин И.Д.
        :return:
        """

        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        path = config.get('Path', 'output_path')
        original_path = config.get('Path', 'basic_report_path')

        func.describe_func_qual(original_path, True, path)
        stat_path = config.get('Path', 'stat_path')
        columns = ["Brand", "cout", "first", "last"]
        data = pd.read_csv(stat_path, delimiter=',', encoding='UTF-8')

        # Создание таблицы Treeview для отображения данных
        style = ttk.Style()
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=15,
                        fieldbackground="#D3D3D3")
        style.map("Treeview",
                  background=[('selected', '#347083')])

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)  # Установка ширины столбца

        save_button2 = app_inter.button(frame, 'Сохранить2', save_in2)
        save_button2.place(x=400, y=600)

        tree.place(x=350, y=320)  # Размещение таблицы с использованием place

        # Отображение всех строк в Treeview
        for i, row in data.iterrows():
            tree.insert('', 'end', values=list(row))

    config = ConfigParser()
    config.read('C:\work\scripts\config.ini')

    output_path = config.get('Path', 'output_path')
    basic_report_path = config.get('Path', 'basic_report_path')

    title = app_inter.label_title(frame, 'Статистическая таблица')
    title.place(x=270, y=10)
    otchet_button = app_inter.button(frame, 'Открыть отчет 3.1', describe_otchet1)

    otchet_button.place(x=100, y=120)
    otchet_button = app_inter.button(frame, 'Открыть отчет 3.2',
                                     describe_otchet2)
    otchet_button.place(x=100, y=350)

    back_button = app_inter.button(frame, 'Назад', open_rep_menu)
    back_button.place(x=700, y=600)


def open_rep_menu():
    """
    Формирование меню с кнопками разных отчетов
    Беседин И.Д.
    :return:
    """
    global frame, root

    frame.destroy()
    create_frame()

    config = ConfigParser()
    config.read('C:\work\scripts\config.ini')
    path_model = config.get('Path', 'model_id_path')
    path_brand = config.get('Path', 'brand_path')
    path_discount = config.get('Path', 'discount_path')
    path = config.get('Path', 'output_path')

    csv_dict = {'Models': path_model, 'Brands': path_brand,
                'Discounts': path_discount}

    otchet_button = app_inter.button(frame, 'ОТЧЁТ 1', otchet1)
    otchet_button.place(x=200, y=200)

    otchet_button2 = app_inter.button(frame, 'ОТЧЁТ 2', otchet2)
    otchet_button2.place(x=400, y=200)

    otchet_button3 = app_inter.button(frame, 'ОТЧЁТ 3', otchet3)
    otchet_button3.place(x=600, y=200)

    back_button = app_inter.button(frame, 'Назад', main_page)
    back_button.place(x=700, y=600)


def open_graph_menu():
    """
    Создание меню графических отчетов
    Беседин И.Д.
    :return:
    """
    global frame, root
    frame.destroy()
    create_frame()

    otchet_button = app_inter.button(frame, 'График 1', open_graph_menu1)
    otchet_button.place(x=100, y=200)

    otchet_button2 = app_inter.button(frame, 'График 2', open_graph_menu2)
    otchet_button2.place(x=300, y=200)

    otchet_button3 = app_inter.button(frame, 'График 3', open_graph_menu3)
    otchet_button3.place(x=500, y=200)

    otchet_button4 = app_inter.button(frame, 'График 4', open_graph_menu4)
    otchet_button4.place(x=700, y=200)

    back_button = app_inter.button(frame, 'Назад', main_page)
    back_button.place(x=700, y=600)


def open_graph_menu1():
    """
    Открытие графического меню 1
    Беседин И.Д.
    :return:
    """
    global frame, root
    frame.destroy()
    create_frame()

    def add_grafic1():
        """
        Добавление графического меню 1
        Беседин И.Д.
        :return:
        """
        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        path = config.get('Path', 'graphics_output')

        path_func = config.get('Path', 'pivot_path')

        func.bar_chart(path_func, False, path)

    title = app_inter.label_title(frame, 'Столбчатая диаграмма')
    title.place(x=300, y=10)

    otchet_button = app_inter.button(frame, 'Сделать отчёт', add_grafic1)
    otchet_button.place(x=200, y=200)

    back_button = app_inter.button(frame, 'Назад', open_graph_menu)
    back_button.place(x=700, y=600)


def open_graph_menu2():
    """
    Открытие графического меню 2
    Беседин И.Д.
    :return:
    """
    global frame, root
    frame.destroy()
    create_frame()

    def add_grafic2():
        """
        Добавление графического меню 2
        Беседин И.Д.
        :return:
        """
        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        path = config.get('Path', 'graphics_output')

        path_func = config.get('Path', 'stat_path')

        func.stat_box(path_func, True, path)

    title = app_inter.label_title(frame, 'Диаграмма Бокса-Вискера')
    title.place(x=250, y=10)

    otchet_button = app_inter.button(frame, 'Сделать отчёт', add_grafic2)
    otchet_button.place(x=200, y=200)

    back_button = app_inter.button(frame, 'Назад', open_graph_menu)
    back_button.place(x=700, y=600)


def open_graph_menu3():
    """
    Открытие графического меню 3
    Беседин И.Д.
    :return:
    """
    global frame, root
    frame.destroy()
    create_frame()
    frame.destroy()
    create_frame()

    config = ConfigParser()
    config.read('C:\work\scripts\config.ini')

    path = config.get('Path', 'output_path')

    def add_grafic3():
        """
        Добавление графического меню 3
        Беседин И.Д.
        :return:
        """
        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        path = config.get('Path', 'graphics_output')

        path_func = config.get('Path', 'basic_report_path')

        func.scatter_plot(path_func, True, path)

    title = app_inter.label_title(frame, 'Диаграмма рассеяния')
    title.place(x=300, y=10)

    otchet_button = app_inter.button(frame, 'Сделать отчёт', add_grafic3)
    otchet_button.place(x=200, y=200)

    back_button = app_inter.button(frame, 'Назад', open_graph_menu)
    back_button.place(x=700, y=600)


def open_graph_menu4():
    """
    Открытие графического меню 4
    Беседин И.Д.
    :return:
    """
    global frame, root
    frame.destroy()
    create_frame()

    def add_grafic4():
        """
        Добавление графического меню 4
        Беседин И.Д.
        :return:
        """
        config = ConfigParser()
        config.read('C:\work\scripts\config.ini')

        path = config.get('Path', 'graphics_output')

        path_func = config.get('Path', 'basic_report_path')

        func.hist_chart(path_func, False, path)

    title = app_inter.label_title(frame, 'Гистограмма')
    title.place(x=300, y=10)

    otchet_button = app_inter.button(frame, 'Сделать отчёт', add_grafic4)
    otchet_button.place(x=200, y=200)

    back_button = app_inter.button(frame, 'Назад', open_graph_menu)
    back_button.place(x=700, y=600)


def main():
    """
    Мейн функция запуска
    Беседин И.Д.
    :return:
    """
    create_app()
    main_page()

    root.mainloop()


if __name__ == '__main__':
    main()
