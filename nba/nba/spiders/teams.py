import scrapy
import csv

class TeamsSpider(scrapy.Spider):
    name = 'teams'
    allowed_domains = ['basketball-reference.com']
    teams_url = 'http://basketball-reference.com/teams/'

    def __init__(self, team, year):
        self.TEAMS_MAPPINGS = self.read_teams_mappings()
        self.team = team
        self.year = year
    
    def start_requests(self):
        team_abbr = self.TEAMS_MAPPINGS[self.team]
        start_url = self.teams_url + team_abbr + '/' + self.year + '_games.html'
        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        for data in self.parse_table(response, _id="games"):
            data['playoffs'] = 0
            yield data

        for data in self.parse_table(response, _id="games_playoffs"):
            data['playoffs'] = 1
            yield data
    
    def parse_table(self, response, _id):
        table = response.xpath(f'//table[@id="{_id}"]')
        if len(table) == 0:
            return

        thead = table.xpath('./thead/tr/th/text()').extract()

        trs = table.xpath('./tbody/tr')
        for row in trs:
            if row.xpath('./@class').extract_first() == 'thead':
                continue

            table_elems = row.xpath('./th|./td') 

            data = {}
            for elem in table_elems:
                metric = elem.xpath('./@data-stat').extract_first()
                value = elem.xpath('./text()|./a/text()').extract_first()
                data[metric] = value
            
            yield data
 
   
    @staticmethod
    def read_teams_mappings():
        teams = list()
        with open('teams.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                teams.append(row)
        
        teams_mappings = {row['team_name']: row['team_id'] for row in teams}

        return teams_mappings