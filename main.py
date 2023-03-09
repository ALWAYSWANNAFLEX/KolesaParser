from parseExcel import ReadExcel

if __name__ == '__main__':
    parse_file = ReadExcel()
    parse_file.read_file()
    parse_file.save_result()