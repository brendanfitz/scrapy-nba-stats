# scrapy-nba-stats

## About

This is a scrapy program to crawl the [Basketball Reference](https://www.basketball-reference.com/) site for NBA statistics.

## Usage

Use the following to pull Per-Game Season stats for [Kevin Durant](https://www.basketball-reference.com/players/d/duranke01.html)

`scrapy crawl players -o items.csv -a player_name="Kevin Durant"`
