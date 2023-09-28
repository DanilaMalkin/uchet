"""
Финальный Проект
Функции создания элементов интерфейса
Беседин И.Д. ; Крутиков М.А. ; Малкин Д.А.
Библиотека написана Бесединым И.Д.
"""
import tkinter as tk


def button(container, text, func_name):
    """
    Функция создания объекта кнопка
    :param container: Фрейм, в котором располагается кнопка
    :param text: Лейбл кнопки
    :param func_name: Функция, выполняемая кнопкой
    :return: Объект кнопки
    """
    button_obj = tk.Button(
        container,
        text=text,
        width=13,
        height=2,
        bg="white",
        fg="black",
        activebackground='grey',
        font=('Helvetica', 18),
        command=func_name
    )
    return button_obj


def label_title(container, text):
    """
    Функция создания объекта лейбл основной
    :param container: Фрейм, в котором располагается кнопка
    :param text: Лейбл
    :return: Объект кнопки
    """
    label_obj_t = tk.Label(
        container,
        text=text,
        font=('Helvetica', 30)
    )
    return label_obj_t


def label_subtitle(container, text):
    """
        Функция создания объекта лейбл побочный
        :param container: Фрейм, в котором располагается кнопка
        :param text: Лейбл
        :return: Объект кнопки
        """
    label_obj_st = tk.Label(
        container,
        text=text,
        width=20,
        font=('Helvetica', 18)
    )
    return label_obj_st


def entry(container):
    """
        Функция создания объекта поле ввода данных
        :param container: Фрейм, в котором располагается поле ввода данных
        :return: Объект поля ввода данных
        """
    entry_obj = tk.Entry(
        container,
        highlightbackground='black',
        highlightthickness=1,
        bg='white',
        font=('Helvetica', 18, "bold"),
        width=20,
    )
    return entry_obj
