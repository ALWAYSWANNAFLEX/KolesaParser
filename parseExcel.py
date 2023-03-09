import collections
import csv
import tkinter as tk
import openpyxl
import pathlib
from tkinter import filedialog
from sibirkoleso import ParseSibirKoleso

HEADERS = (
    'Марка', 'Модель', 'Цена у нас', 'Цена sibirkoleso', 'Ссылка'
)

ParseResult = collections.namedtuple('ParseResult', ('mark', 'model', 'our_price', 'sib_price', 'link'))

PATH = str(pathlib.Path(__file__).parent)

class ReadExcel:
    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename()
        self.result = []

    def save_result(self):
        with open(PATH + '/parser_test.xlsx', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
            for row in self.result:
                writer.writerow(row)

    def read_file(self):
        file = openpyxl.open(self.file_path, read_only=True)
        work_book = file.active
        for row in range(2, work_book.max_row):
            mark = work_book[row][5].value
            size = work_book[row][4].value
            model = work_book[row][8].value
            our_price = work_book[row][9].value
            parser = ParseSibirKoleso(mark, size, model)
            self.result.append(ParseResult(mark=mark, model=model, our_price=our_price, sib_price=parser.run(), link=parser.filter_full_url))
            print("Записано  " + str(row))

#if __name__ == '__main__':
#    parse_file = ReadExcel()
#    parse_file.read_file()
