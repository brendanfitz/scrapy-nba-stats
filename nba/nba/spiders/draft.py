import scrapy


class DraftSpider(scrapy.Spider):
    name = 'draft'
    allowed_domains = ['basketball-reference.com']

    def __init__(self, year):
        self.year = year
    
    def start_requests(self):
        start_url = f'https://www.basketball-reference.com/draft/NBA_{self.year}.html'
        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        for table_data in self.parse_table(response, 'stats'):
            yield table_data

    def parse_table(self, response, _id):
        draft_round = 1

        table = response.xpath(f'//table[@id="{_id}"]')
        if len(table) == 0:
            return

        thead = table.xpath('./thead/tr/th/text()').extract()

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
            
            data['draft_year'] = self.year
            data['draft_round'] = draft_round
            yield data