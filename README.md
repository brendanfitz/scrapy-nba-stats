# scrapy-nba-stats

## About

This is a scrapy program to crawl the [Basketball Reference](https://www.basketball-reference.com/) site for NBA statistics.

## Usage

Use the following to pull per-game by season stats for [Kevin Durant](https://www.basketball-reference.com/players/d/duranke01.html):

`scrapy crawl players -o kevin_durant_stats.csv -a player_name="Kevin Durant"`

Use the following to pull game results for the [1995-1996 Chicago Bulls](https://www.basketball-reference.com/teams/CHI/1996_games.html):

`scrapy crawl teams -o chicago_bulls_96.csv -a team="Chicago Bulls" -a year=1996`
