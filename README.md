# Web Scraper Bot with IP Blocking Avoidance

This GitHub repository contains a Python bot that uses the Selenium framework to perform web scraping tasks. The bot is designed to avoid IP blocking by utilizing a user agent to disguise its identity. 

## Getting Started

To get started with this bot, you will need to have Python and Selenium installed on your machine. You can install Selenium using pip:

```pip install selenium```


You will also need to have a web driver installed for the browser you want to use. This bot has been tested with the Chrome driver, which you can download [here](https://chromedriver.chromium.org/downloads).

Once you have Python, Selenium, and the Chrome driver installed, you can clone this repository to your local machine:

```git clone https://github.com/moonnstarr/cex_exe.git```


## Configuration

Before running the bot, you will need to configure it with the appropriate settings.

### User Agent

To avoid IP blocking, the bot uses a user agent to disguise its identity. You can set the user agent in the `app.py` file. You can find a list of user agents [here](https://developers.whatismybrowser.com/useragents/explore/).

### URLs

The URLs to be scraped should be added to the `URLS` list in the `main.py` file.

### XPaths

The bot uses XPaths to locate the elements to be scraped on each page. You will need to set the appropriate XPaths for your particular use case in the `XPATHS` dictionary in the `app.py` file.

### Output

The scraped data will be saved to a CSV file named `output.csv` in the same directory as the bot script. You can change the name and location of this file in the `OUTPUT_FILE` variable in the `app.py` file.

## Running the Bot

To run the bot, simply execute the `app.py` script:

```python web_scraper_bot.py```


The bot will open a headless Chrome browser window and navigate to each URL in the `URLS` list. It will then scrape the data specified by the XPaths in the `XPATHS` dictionary and save it to the `output.csv` file. 

## Disclaimer

Please use this bot responsibly and in accordance with the terms of service of the websites you are scraping. The use of web scraping bots can sometimes violate the terms of service of websites, and may even be illegal in some jurisdictions.

