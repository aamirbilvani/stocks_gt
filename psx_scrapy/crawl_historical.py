import requests
import os
import csv
import time
from datetime import datetime


def main():
    year_dict = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    symbols_path = dir_path + "/../data/symbols.txt"
    with open(symbols_path, 'r') as symbols_file:
        symbols_list = list(csv.reader(symbols_file))
        for index, line in enumerate(symbols_list, 1):
            try:
                symbol = line[0]
                request_path = "https://dps.psx.com.pk/timeseries/eod/" + line[0]
                data_retrieved = False
                while not data_retrieved:
                    time.sleep(1)
                    r = requests.get(request_path, timeout=5)
                    print('{:03d} - {} returned {}'.format(index, request_path, r.status_code))
                    if r.status_code == requests.codes.OK:
                        json = r.json()
                        data = json['data']
                        if data is not None:
                            data_retrieved = True
                            for item in data:
                                epoch = item[0]
                                epoch_date = datetime.utcfromtimestamp(int(epoch))
                                year = epoch_date.year
                                date_string = epoch_date.strftime('%Y-%m-%d')
                                price = item[1]
                                volume = item[2]
                                
                                if year not in year_dict:
                                    year_dict[year] = {}

                                if date_string not in year_dict[year]:
                                    year_dict[year][date_string] = {}
                                    
                                year_dict[year][date_string][symbol] = price

                # if index % 10 == 0:
                #     break
            
            except requests.exceptions.RequestException as e:
                print(e)

    print('Data acquired\n\n')
        
    for year in sorted(year_dict, reverse=True):
        file_path = dir_path + '/../data/historical/' + str(year) + '.csv'

        symbol_column = {}
        for index, row in enumerate(symbols_list, 1):
            symbol_column[row[0]] = index

        if not os.path.isfile(file_path):
            with open(file_path, 'w', newline='') as output_file:
                header_row = ['symbol']
                for row in symbols_list:
                    header_row.append(row[0])
                data_writer = csv.writer(output_file)
                data_writer.writerow(header_row)

        with open(file_path, 'r+', newline='') as output_file:
            data_list = list(csv.reader(output_file))
            output_writer = csv.writer(output_file)

            for date in sorted(year_dict[year]):
                output_row = [date]
                output_row.extend([''] * (len(data_list[0]) - 1))
                for symbol in year_dict[year][date]:
                    output_row[symbol_column[str(symbol)]] = year_dict[year][date][str(symbol)]
                output_writer.writerow(output_row)

if __name__ == '__main__':
    main()
