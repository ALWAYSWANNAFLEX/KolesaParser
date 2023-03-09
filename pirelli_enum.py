import openpyxl


class PirelliReplace:
    def __init__(self, compare_item):
        self.file = openpyxl.open('Pirelli.xlsx', read_only=True)
        self.compare_item = compare_item.replace('-', '')

    def run(self):
        work_book = self.file.active
        replaced_string = self.compare_item
        for row in range(1, work_book.max_row):
            pirelli_brand = work_book[row][0].value.lower().replace('-', '')
            if(pirelli_brand == self.compare_item):
                replaced_string = work_book[row][1].value.lower().replace('-', '').replace(' ', '')
        return replaced_string
