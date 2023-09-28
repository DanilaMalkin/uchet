"""
Финальный Проект
Библиотека функций для работы с базами данных
Беседин И.Д. ; Крутиков М.А. ; Малкин Д.А.
Библиотека написана Крутиковым М.А.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Функции обработки датасетов
def delete_func(path, key, format_id):
    """
    Функия удаления элемента из датасета
    :param path: Путь к Файлу
    :param key: Ключ удаления
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :return: None
    """
    data_frame = pd.read_csv(path, index_col=0)
    data_frame.drop(labels=key, axis=0, inplace=True)
    if format_id:
        data_frame.to_csv(path)
    else:
        data_frame_to_excel(path, data_frame)


def add_func(path, param, format_id):
    """
    Функция добавления в датасет
    :param path: Путь к Файлу
    :param param: Строка, которую требуется добавить. Разделитель - запятая
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :return: None
    """
    data_frame = pd.read_csv(path)
    param = [param.split(',')]
    col_names = []
    for col in data_frame.columns:
        col_names.append(col)
    data_frame2 = pd.DataFrame(param, columns=col_names)
    data_frame = pd.concat([data_frame, data_frame2], ignore_index=True)
    if format_id:
        data_frame_to_csv(path, data_frame, ',')
    else:
        data_frame_to_excel(path, data_frame)


def inplace_function(path, param, format_id):
    """
    Функция реактирования элементов датасета
    :param path: Путь к Файлу
    :param param: Строка с ключем и новыми значениями. Разделитель - запятая
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :return: None
    """
    data_frame = pd.read_csv(path)
    param = [param.split(',')]

    col_list = []
    for col in data_frame.columns:
        col_list.append(col)

    if param[0][0].isdigit():
        param[0][0] = int(param[0][0])

    data_frame = pd.read_csv(path, index_col=0)
    data_frame2 = pd.DataFrame(param, columns=col_list, index=[param[0][0]])
    col_list = col_list[1:len(col_list)]
    data_frame.loc[param[0][0], col_list] = data_frame2.loc[param[0][0], col_list]

    if format_id:
        data_frame.to_csv(path)
    else:
        data_frame_to_excel(path, data_frame)


# Функции сохранения
def data_frame_to_csv(path, data_frame, sep):
    """
    Функция сохранения датафрейма в csv
    :param path: Путь сохранения/обновления файла
    :param data_frame: Датафрейм
    :param sep: Разделитель
    :return: None
    """
    data_frame.to_csv(path, sep, index=False)


def data_frame_to_excel(path, data_frame):
    """
    Функция сохранения датафрейма в excel
    :param path: Путь сохранения/обновления файла
    :param data_frame: Датафрейм
    :return: None
    """
    data_frame.to_excel(path)


def plt_to_png(path, fig):
    """
    Функция сохранения графика в png
    :param path: Путь сохранения/обновления файла
    :param fig: График plt
    :return: None
    """
    fig.savefig(path + '\\' + 'Figure.png', bbox_inches='tight')
    plt.close(fig)


def plt_to_pdf_frame(path, fig):
    """
    Функция сохранения графика в pdata_frame
    :param path: Путь сохранения/обновления файла
    :param fig: График plt
    :return: None
    """
    fig.savefig(path + '\\' + 'Figure.pdata_frame', bbox_inches='tight')
    plt.close(fig)


# File combining algorithms
def clothes_by_class(cat, path_brand, path_id, format_id, path):
    """
    Функция создания таблицы брендов по категориям
    :param cat: категория
    :param path_brand: Путь к датасету брендов
    :param path_id: Путь к датасету
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :param path: Путь сохранения
    :return: None
    """
    data_frame_brand = pd.read_csv(path_brand, index_col=0)
    data_frame_id = pd.read_csv(path_id, index_col=0)

    data_frame_brand.drop(["Location", "Phone"], axis=1, inplace=True)
    data_frame_brand = data_frame_brand[data_frame_brand.Category == cat]

    data_frame_id_cpy = data_frame_id.drop(["MODEL_ID", "Quanity"], axis=1)
    data_frame_out = data_frame_id_cpy[data_frame_id_cpy["Brand"].isin(data_frame_brand["Brand"])]
    if data_frame_out.empty:
        print("No such category")
    else:
        if format_id:
            path = path + '\\' + 'Basic_report.csv'
            data_frame_to_csv(path, data_frame_out, ',')
        else:
            path = path + '\\' + 'Basic_report.xlsx'
            data_frame_to_excel(path, data_frame_out)


def basic_rep(path_id, path_disc, path_brand, format_id, path):
    """
    Создание базового объединенного датасета
    :param path_id: Путь к MODEL_ID.csv
    :param path_disc: Путь к Discount.csv
    :param path_brand: Путь к Brand.csv
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :param path: Путь вывода
    :return: None
    """
    data_frame_id = pd.read_csv(path_id)
    data_frame_discount = pd.read_csv(path_disc)
    data_frame_brand = pd.read_csv(path_brand)
    data_frame_merged = data_frame_id.merge(data_frame_brand, on="Brand", how='left')
    data_frame_merged = data_frame_merged.merge(data_frame_discount, on="Season", how='left')
    data_frame_merged.drop('Phone', axis=1, inplace=True)
    if format_id:
        path = path + '\\' + 'Basic_report.csv'
        data_frame_merged.to_csv(path, index=False)
    else:
        path = path + '\\' + 'Basic_report.xlsx'
        data_frame_to_excel(path, data_frame_merged)


def pivot_table(basic_rep_path, format_id, path):
    """
    Создание базовой сводной таблицы по параметрам Брэнд, Тип, Количество
    :param basic_rep_path: Путь к Basic_report.csv
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :param path: Путь вывода
    :return: None
    """
    data_frame = pd.read_csv(basic_rep_path, index_col=0)
    data_frame_pt = pd.pivot_table(
        data=data_frame,
        index='Brand',
        columns='Type',
        values='Quantity',
        aggfunc=np.sum
    )

    if format_id:
        path = path + '\\' + 'Pivot_table.csv'
        data_frame_pt.to_csv(path, index=True)
    else:
        path = path + '\\' + 'Pivot_table.xlsx'
        data_frame_to_excel(path, data_frame_pt)


def pivot_table_season_price(basic_rep_path, format_id, path):
    """
    Создание сводной таблицы по бренду с ценами по сезонам
    :param basic_rep_path: Путь к Basic_report.csv
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :param path: Путь вывода
    :return: None
    """
    data_frame = pd.read_csv(basic_rep_path, index_col=0)
    data_frame_pt = pd.pivot_table(
        data=data_frame,
        index='Brand',
        columns='Season',
        values='Price (USD)',
        aggfunc='mean'
    )
    if format_id:
        path = path + '\\' + 'Pivot_table_season_price.csv'
        data_frame_pt.to_csv(path, index=True)
    else:
        path = path + '\\' + 'Pivot_table_season_price.xlsx'
        data_frame_to_excel(path, data_frame_pt)


def bar_chart(path_ds, format_id, path):
    """
    Создание столбчатой диаграммы
    :param path_ds: Путь к датасету
    :param format_id: True - сохранение в png, False - сохранение в pdf
    :param path: Путь вывода
    :return: None
    """
    data_frame = pd.read_csv(path_ds, index_col=0)
    data_frame.plot(kind='bar', stacked=True)

    plt.xlabel('Brands')
    plt.ylabel('Quantity')
    plt.title('Quantity of an apparel type by brand')
    if format_id:
        path = path + '\\' + 'bar_chart.png'
        plt.savefig(path)
        plt.show()
    else:
        path = path + '\\' + 'bar_chart.pdf'
        plt.savefig(path)
        plt.show()


def hist_chart(path_basic, format_id, path):
    """
    Создание гистограммы
    :param path_basic: Путь к Basic_report.csv
    :param format_id: True - сохранение в png, False - сохранение в pdf
    :param path: Путь вывода
    :return: None
    """
    data_frame = pd.read_csv(path_basic, index_col=0)
    data_frame = data_frame.groupby('Brand')['Price (USD)'].agg(['sum'])
    plt.hist(data_frame)

    plt.xlabel('')
    plt.ylabel('')
    plt.title('Basic Hist')
    if format_id:
        path = path + '\\' + 'hist.png'
        plt.savefig(path)
        plt.show()
    else:
        path = path + '\\' + 'hist.pdf'
        plt.savefig(path)
        plt.show()


def custom_pivot(basic_rep_path, format_id, path, custom_settings):
    """
    Создание кастомной сводной таблицы
    :param basic_rep_path: Путь к Basic_report.csv
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :param path: Путь вывода
    :param custom_settings: Список из 4х элементов, параменты сводной таблицы
    :return: None
    """
    data_frame = pd.read_csv(basic_rep_path, index_col=0)
    data_frame_pt = pd.pivot_table(
        data=data_frame,
        index=custom_settings[0],
        columns=custom_settings[1],
        values=custom_settings[2],
        aggfunc=custom_settings[3]
    )
    if format_id:
        path = path + '\\' + 'Pivot_table_custom.csv'
        data_frame_pt.to_csv(path, index=True)
    else:
        path = path + '\\' + 'Pivot_table_custom_.xlsx'
        data_frame_to_excel(path, data_frame_pt)


def describe_func(path_original, format_id, path):
    """
    Функция описания датасета по количественному параметру
    :param path_original: Путь к Basic_report.csv
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :param path: Путь вывода
    :return: None
    """
    data_frame = pd.read_csv(path_original, index_col=0)

    data_frame_new = data_frame.groupby('Brand')['Price (USD)'].agg([
        'count', 'mean', 'std', 'min', 'max'])

    if format_id:
        path = path + '\\' + 'Stat_describe.csv'
        data_frame_new.to_csv(path, index=True)
    else:
        path = path + '\\' + 'Stat_describe.xlsx'
        data_frame_to_excel(path, data_frame_new)


def stat_box(path_original, format_id, path):
    """
    Создание Бокс - диаграммы
    :param path_original: путь к статистическому отчету
    :param format_id: True - сохранение в png, False - сохранение в pdf
    :param path: Путь вывода
    :return: None
    """
    data_frame = pd.read_csv(path_original)
    array = data_frame['Brand'].to_numpy()

    data_frame = pd.read_csv(path_original, index_col=0)
    data_frame = data_frame.T  # Транспонирование датафрейма
    plt.boxplot(data_frame, labels=array)
    plt.xlabel('Brands')
    plt.ylabel('Average Price')
    plt.title('Average price per brand')
    if format_id:
        path = path + '\\' + 'scatter_plot.png'
        plt.savefig(path)
        plt.show()
    else:
        path = path + '\\' + 'scatter_plot.pdf'
        plt.savefig(path)
        plt.show()


def scatter_plot(path_original, format_id, path):
    """
    Создание диаграммы рассеивания по цене и количеству в зависимости от бренда
    :param path_original: Путь к Basic_report.csv
    :param format_id: True - сохранение в png, False - сохранение в pdf
    :param path: Путь вывода
    :return: None
    """
    data_frame = pd.read_csv(path_original, index_col=0)
    data_frame.drop(['Season', 'Type', 'Discount', 'Location', 'Category'], axis=1)
    plt.scatter(data_frame['Price (USD)'], data_frame['Quantity'])
    plt.xlabel('Brands')
    plt.ylabel('Average Price')
    plt.title('Average price per brand')
    if format_id:
        path = path + '\\' + 'scatter_plot.png'
        plt.savefig(path)
        plt.show()
    else:
        path = path + '\\' + 'scatter_plot.pdf'
        plt.savefig(path)
        plt.show()


def describe_func_qual(path_original, format_id, path):
    """
    Функция описания датасета по качественному параметру
    :param path_original: Путь к Basic_report.csv
    :param format_id: True - сохранение в csv, False - сохранение в excel
    :param path: Путь вывода
    :return: None
    """
    data_frame = pd.read_csv(path_original, index_col=0)
    data_frame_new = data_frame.groupby('Brand')['Type'].agg([
        'count', 'first', 'last'])

    if format_id:
        path = path + '\\' + 'Stat_describe.csv'
        data_frame_new.to_csv(path, index=True)
    else:
        path = path + '\\' + 'Stat_describe.xlsx'
        data_frame_to_excel(path, data_frame_new)


# Вызовы функций для подгрузки датасетов, используемых в графиках
basic_rep('C:\work\data\MODEL_ID.csv', 'C:\work\data\Discount.csv',
          'C:\work\data\Brand.csv', True, 'C:\work\output')
pivot_table('C:\work\output\Basic_report.csv', True, 'C:\work\output')
describe_func('C:\work\output\Basic_report.csv', True, 'C:\work\output')
