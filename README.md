# Linkedin Webscraper
 Created a webscraper that takes in Linkedin URLs scraped from Google Chrome Search and then scrapes every Linkedin profile information.

# Demo
<img src = "scraping_snippet/snippet.gif">

# Setting up account information

We require the user to log in to their Linkedin Account.

Please create a `config.ini` file with the following content

```ini
[DRIVER]
path = path/to/chromdriver

[ACCOUNT]
username = email@email.com
password = password123
```

Please refer to [Selenium](#Selenium) for instructions on chrome driver path

# Setting up URLs

We expect the Linkedin URLs to be placed under [URLs folder](scraped%20URLs)

# Note
 The webscrapers that are readily available on other repositories do not seem to work on my work station for some reason. Thus, my personal webscraper may also not work for you but do feel free to try it out!

# Discretion
 Although the legal terms of webscraping on Linkedin public data is rather blurry, scraping data from Linkedin is nonethless still a difficult task due to its security features. I recommend creating multiple dummy accounts for this task to avoid your personal account from being suspended!
 
# Dependencies

Python==3.8

## Selenium:

Web driver is required before using Selenium.

we used `ChromeDriver` for this project.

Please follow the links [here](https://chromedriver.chromium.org/downloads) to download the correct driver.

To check Chrome version
```bash
google-chrom --version
```

driver must be placed in PATH, please follow the instructions
[here](https://www.browserstack.com/guide/run-selenium-tests-using-selenium-chromedriver)

# Developer

Install dependencies with
```bash
pip install -r requirements.txt
```
