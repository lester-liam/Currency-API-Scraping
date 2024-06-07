# Import Libraries and Functions
from datetime import datetime

from rates_funcs import *


# Initialize Depedancies
configFilename:str = "config.csv" # Stores the Currency/Countries to Query
output_filename:str = f"rates_history/rates_history_{datetime.now().strftime("%d%b%y-%H%M")}.csv" # Final Output Filename

# Links to API URLs for Companies
providers_api:dict = {
    "instarem":"https://www.instarem.com/api/v1/public/transaction/computed-value",
    "moneymatch_rates":"https://transfer.moneymatch.co/utility/rate/MYR",
    "moneymatch_fees":"https://transfer.moneymatch.co/fees?from=MYR",
    "sunwaymoney":"https://sunwaymoney.com/information/getRate/",
    "wise":"https://api.transferwise.com/v3/comparisons/"
}

# Main Function
if __name__ == '__main__':
    
    print("========== Script Started ==========")
    # Generate CSV for Rates
    print("Starting Rates Processes: ")
    getRates(configFilename, providers_api)
    print()

    # Read CSV Outputs
    wise_rates = pd.read_csv("./output/wise.csv", on_bad_lines="skip", encoding='utf8', header=None)
    instarem = pd.read_csv("./output/instarem.csv", on_bad_lines="skip", encoding='utf8', header=None)
    sunway_money = pd.read_csv("./output/sunwaymoney.csv", on_bad_lines="skip", encoding='utf8', header=None)
    money_match = pd.read_csv("./output/moneymatch.csv", on_bad_lines="skip", encoding='utf8', header=None)

    # Merge DataFrames
    output_df = pd.concat([wise_rates, instarem, sunway_money, money_match])

    # Generate Excel File
    output_df.to_csv(output_filename, index=None, header=["Provider", "Country", "Currency", "Amount (RM)", "Rate", "Fees (RM)", "Receive Amount"])
    print("Final Excel Exported: ", output_filename)
    print("========== Script Ended ==========")