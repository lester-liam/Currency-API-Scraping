# Currency-API-Scraping
A webscraper that scrapes Malaysia eRemit Companies <i>(Wise, Instaremit, MoneyMatch, SunwayMoney)</i> via APIs and stores them in a comma-separated-value (.csv) file.

Some applications for webscraping rates is storing them for future rates predictions and machine learning applications/projects.

## Disclaimer:
This repository is solely for learning purposes.<br/>
[Ethics in Web Scraping | Towards Data Science ](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01)

## Prerequisites
Ensure you have installed the following packages `requests` and `pandas`.
```python
pip install requests
pip install pandas
```

Clone the Repository
```
git clone https://github.com/lester-liam/weather-forecast-email.git
```
### Update Configuration File
In `config.csv`, ensure you added the currencies / rates you want.

## Running the Code
The code should run out of the box. However you can also configure the file output locations.

### Final CSV Output and Configuration File
```python
# Stores the Currency/Countries to Query
configFilename:str = "config.csv" 
# Final Output Filename
output_filename:str = f"rates_history/rates_history_{datetime.now().strftime("%d%b%y-%H%M")}.csv"
```

### Updating File Outputs
<b>main.py:</b> Line 30:
```python
# Read CSV Outputs
wise_rates = pd.read_csv("./output/wise.csv", ...)
instarem = pd.read_csv("./output/instarem.csv", ...)
sunway_money = pd.read_csv("./output/sunwaymoney.csv", ...)
money_match = pd.read_csv("./output/moneymatch.csv", ...)
```

<b>rates_funcs.py:</b> Line 323
```python
# Reset CSV Files:
filenames:list = ["./output/instarem.csv", "./output/moneymatch.csv", "./output/wise.csv", "./output/sunwaymoney.csv"]
for file in filenames:
    with open(file, 'w', newline="") as output:
        output.write('')
```

<b>rates_funcs.py:</b> Line 332:
``` python
# Define processes for each provider
processes = [
    Process(..., "./output/instarem.csv")),
    Process(..., "./output/sunwaymoney.csv")),
    Process(..., "./output/moneymatch.csv"))
]
```