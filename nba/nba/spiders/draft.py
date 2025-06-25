import scrapy
import time


class DraftSpider(scrapy.Spider):
    name = 'draft'
    allowed_domains = ['basketball-reference.com']
    URL_TEMPLATE = 'https://www.basketball-reference.com/draft/NBA_{year}.html'

    def __init__(self, years=None, **kwargs):
        self.current_year = None
        super(DraftSpider, self).__init__(**kwargs)
        if years is not None:
            self.years = (int(year) for year in years.split(','))
        else:
            self.years = range(1977, 2022)

    def start_requests(self):
        for year in self.years:
            print(f'Scraping draft year: {year}')
            time.sleep(1)
            url = self.URL_TEMPLATE.format(year=year)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for table_data in self.parse_table(response, 'stats'):
            yield table_data

    def parse_table(self, response, _id):
        draft_round = 1

        table = response.xpath(f'//table[@id="{_id}"]')
        if len(table) == 0:
            return

        head = table.xpath('./thead/tr/th/text()').extract()

        trs = table.xpath('./tbody/tr')
        for row in trs:
            if row.xpath('./@class').extract_first() == 'over_header thead':
                xpath = './th[@data-stat="header_draft"]/text()'
                draft_round = (row.xpath(xpath)
                    .extract_first()
                    .replace('Round ', '')
                )
                continue

            elif row.xpath('./@class').extract_first() == 'thead':
                continue

            table_elems = row.xpath('./th|./td') 

            data = {}
            for elem in table_elems:
                metric = elem.xpath('./@data-stat').extract_first()
                value = elem.xpath('./text()|./a/text()').extract_first()
                data[metric] = value
            
            data['draft_year'] = (response.xpath('//h1[@itemprop="name"]')
                                  .xpath('span/text()')[0].extract()
                                 )
            data['url'] = draft_round
            yield data