# Synergy Stats

Created by: Michael Altschuler

Last Updated: 09/20/2021

## Purpose

The purpose of this application is to gather all the public offensive and defensive sysnergy stats for every player since 2017-18.  Stats include:
* Player
* Team
* Age
* Height (in inches)
* Weight (in pounds)
* Games Played
* Minutes Played
* Possessions for Each Play Type
* Points for Each Play Type
* Points per Possession for Each Play Type
* Frequency for Each Play Type
* Percentile for Each Play Type

Play Types include:
* transition
* isolation
* PnR Ball Handler
* PnR Screener
* post-ups
* spot-ups
* cuts
* hand-offs
* off-screen
* putbacks

The final file will be located in final_data/{season} and will be called offense.csv if they are offensive possessions and defense.csv if they are defensive possessions.

## How to Run

```
python offense_scraper.py {season}
python defense_scraper.py {season}
```

For example:
```
python offense_scraper.py 2017-18
```

## Potential Issues

This application uses chromedriver selenium to scrape the javascript table from stats.nba.com.  Make sure you have Chrome installed and make sure you have have the correct version of chromedriver that matches your version of chrome (https://chromedriver.chromium.org/downloads) and have it located in the same directory as scraper.py

It is possible that due to taking too long to load the webpage, not all of the rows will be read.  This application built in a protection to re-run it it didn't collect at least 50 rows. If you do not intend for this behavior, comment out that infinite loop at the bottom of scraper.py or hit CTL + C  after final.csv is saved the first time.
