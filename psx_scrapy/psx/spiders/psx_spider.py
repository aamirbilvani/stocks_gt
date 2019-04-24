import scrapy
from datetime import datetime
import os
import csv

class PSXSpider(scrapy.Spider):
    name = "psx"

    def start_requests(self):
        current_date = datetime.now()
        today854 = current_date.replace(hour=8,minute=54,second=0,microsecond=0)
        today1706 = current_date.replace(hour=17,minute=6,second=0,microsecond=0)

        # weekday: 0 = Monday
        # only update between 9.30 and 15.30 on weekdays
        if (current_date.weekday() < 5 and current_date > today854 and current_date < today1706):

            path = '../data/{:04d}_{:02d}_{:02d}.csv'.format(current_date.year, current_date.month, current_date.day)

            if not os.path.isfile(path):
                with open(path, 'w', newline='') as data_file, \
                     open('../data/symbols.txt', 'r') as symbols_file:
                    symbols_list = list(csv.reader(symbols_file))
                    header_row = ['symbol']
                    for row in symbols_list:
                        header_row.append(row[0])
                    data_writer = csv.writer(data_file)
                    data_writer.writerow(header_row)

            urls = []
            with open('../data/symbols.txt', 'r') as symbols_file:
                symbols_list = list(csv.reader(symbols_file))
                for row in symbols_list:
                    urls.append(row[1])

            with open(path, 'r+', newline='') as data_file:
                data_list = list(csv.reader(data_file))
                data_writer = csv.writer(data_file)

                timestamp = '{:02d}:{:02d}'.format(current_date.hour, current_date.minute)
                new_row = [timestamp]
                new_row.extend([''] * (len(data_list[0]) - 1))
                data_writer.writerow(new_row)

            for url in urls:
                request = scrapy.Request(url=url, callback=self.parse)
                request.meta['path'] = path
                yield request

    def parse(self, response):
        path = response.meta['path']
        with open(path, 'r') as data_file:
            data_list = list(csv.reader(data_file))

        symbol = response.css('div.pageHeader__title::text').extract_first()
        stock_value = response.css('div.quote__close::text').extract_first()[3:]

        header_row = data_list[0]
        data_row = data_list[-1]
        for i in range(0, len(header_row)):
            col_symbol = str(header_row[i]).strip()
            if col_symbol == symbol:
                data_row[i] = float(stock_value.replace(',',''))
                break    

        with open(path, 'r+', newline='') as data_file:
            data_writer = csv.writer(data_file)
            data_writer.writerows(data_list)