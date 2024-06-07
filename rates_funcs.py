# Import Libraries
import csv
import time
from multiprocessing import Process

import requests
import pandas as pd


# ==================================================
"""
Appends a CSV File and Inserts a New Row/Record

Parameters: 
	`provider` = Currency Exchange Provider
	`country` = Recipient Country
	`currency` = Received Currency
	`amt` = Amount Sending
	`fees` = Exchange Fees
	`receive_amt` = Amount Receivable

Returns:
	int: Success (0), Fail (1)
"""
def appendRow(output_filename, provider, country, currency, amt, rates, fees, receive_amt) -> int:

    try:
        
        with open(output_filename, 'a', newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([provider, country, currency, amt, rates, fees, receive_amt])

        return(0)
    except Exception as e:
        print(e)
        return(1)

# ==================================================
# Get Wise Rates
"""
Get Rates from Wise API

Parameters: 
	`api` = Quote API
	`rates_df` = Parameters to Query & Output (provider, to country, to currency, send amount)
	`currency` = Received Currency
	`output_filename` = File to Store Results

Returns: None
"""
def getWiseRates(api, rates_df, output_filename) -> None:
	
	# Initialize variables names to Default Values
	rates = "-"
	fees = "-"
	receive_amt = "-"

	failedFlag = False		# Flag `TRUE` if Failed GET Response / Bad Insert Row
	
	# For Each Row, Send GET Requests and Append Row
	for i in range(0, len(rates_df)):
		row = rates_df.iloc[i]

		# Retrieve Query Rates (Config) Values
		provider = row.iloc[0]
		country = row.iloc[1]
		currency = row.iloc[2]
		amt = row.iloc[3]

		# Send GET Requests
		response = requests.get(
					url=api, params={
						"sourceCurrency": "MYR",
						"targetCurrency": currency,
						"sendAmount": amt,
						"sourceCountry": "MY"
					})
		
		# Update Flag if Status Code not 200
		response_status_code:int = response.status_code
		if(response_status_code != 200):
			failedFlag = True
			continue
		
		else:
			# Convert Response Data to JSON
			data = response.json()
			
			# Get Quote provided by Wise
			quoteProviders = data['providers']			
			for quoteProvider in quoteProviders:
				
				# Retrieve Values & Insert Row
				if (quoteProvider['name'] == "Wise"):
					rates = float(quoteProvider['quotes'][0]['rate'])
					fees = float(quoteProvider['quotes'][0]['fee'])

					receive_amt = round((rates * amt) + fees, 2)
					receive_amt = round(receive_amt, 2)
					
					appendStatus = appendRow(output_filename, provider, country, currency, amt, rates, fees, receive_amt)

					# Update Flag if insert row failed
					if (appendStatus != 0):
						failedFlag = True
					
					time.sleep(10) # Wait for 10 seconds before next API Call
				else:
					continue

	# If failure occured, return 1, else 0
	if (failedFlag):
		print("[Warning] Rates Extracted for Wise with Failures.")
	else:
		print("[Success] Rates Extracted for Wise.")

# ==================================================
# Get Instarem Rates
"""
Get Rates from Instarem API

Parameters: 
	`api` = Instarem's API
	`rates_df` = Parameters to Query & Output (provider, to country, to currency, send amount)
	`currency` = Received Currency
	`output_filename` = File to Store Results

Returns: None
"""
def getInstaremRates(api, rates_df, output_filename) -> None:
	
	# Initialize variables names to Default Values
	rates = "-"
	fees = "-"
	receive_amt = "-"

	failedFlag = False		# Flag `TRUE` if Failed GET Response / Bad Insert Row
	
	# For Each Row, Send GET Requests and Append Row
	for i in range(0, len(rates_df)):
		row = rates_df.iloc[i]

		# Retrieve Query Rates (Config) Values
		provider = row.iloc[0]
		country = row.iloc[1]
		currency = row.iloc[2]
		amt = row.iloc[3]

		response = requests.get(url=f"{api}?source_currency=MYR&destination_currency={currency}&instarem_bank_account_id=26&source_amount={amt}&country_code=MY")
	
		# Update Flag if Status Code not 200
		response_status_code:int = response.status_code
		if(response_status_code != 200):
			failedFlag = True
			continue
		else:
			# Convert Response Data to JSON
			data = response.json()

			rates = float(data['data']['instarem_fx_rate'])
			fees = float(data['data']['regular_transaction_fee_amount'])

			receive_amt = float(data['data']['destination_amount'])
			receive_amt = round(receive_amt, 2)
			
			# Retrieve Values & Insert Row
			appendStatus = appendRow(output_filename, provider, country, currency, amt, rates, fees, receive_amt)

			# Update Flag if insert row failed
			if (appendStatus != 0):
				failedFlag = True
			
			time.sleep(10) # Wait for 10 seconds before next API Call

	# If failure occured, return 1, else 0
	if (failedFlag):
		print("[Warning] Rates Extracted for Instarem with Failures.")
	else:
		print("[Success] Rates Extracted for Instarem.")

# ==================================================
# Get Sunway Money Rates
"""
Get Rates from Sunway Money API

Parameters: 
	`api` = Sunway Money's API
	`rates_df` = Parameters to Query & Output (provider, to country, to currency, send amount, corridor)
	`currency` = Received Currency
	`output_filename` = File to Store Results

Returns: None
"""
def getSunwayMoneyRates(api, rates_df, output_filename) -> None:
	
	# Initialize variables names to Default Values
	rates = "-"
	fees = "-"
	receive_amt = "-"

	failedFlag = False		# Flag `TRUE` if Failed GET Response / Bad Insert Row
	
	# For Each Row, Send GET Requests and Append Row
	for i in range(0, len(rates_df)):
		row = rates_df.iloc[i]

		# Retrieve Query Rates (Config) Values
		provider = row.iloc[0]
		country = row.iloc[1]
		currency = row.iloc[2]
		amt = row.iloc[3]
		corridor = row.iloc[4]

		response = requests.get(url=f"{api}/{corridor}")
	
		# Update Flag if Status Code not 200
		response_status_code:int = response.status_code
		if(response_status_code != 200):
			failedFlag = True
			continue
		else:
			# Convert Response Data to JSON
			data = response.json()

			rates = float(data['myrRate'])

			receive_amt = rates * int(amt) 
			receive_amt = round(receive_amt, 2)
			
			# Retrieve Values & Insert Row
			appendStatus = appendRow(output_filename, provider, country, currency, amt, rates, fees, receive_amt)

			# Update Flag if insert row failed
			if (appendStatus != 0):
				failedFlag = True
			
			time.sleep(10) # Wait for 10 seconds before next API Call

	# If failure occured, return 1, else 0
	if (failedFlag):
		print("[Warning] Rates Extracted for Sunway Money with Failures.")
	else:
		print("[Success] Rates Extracted for Sunway Money.")

# ==================================================
# Get MoneyMatch Rates
"""
Get Rates from MoneyMatch API

Parameters: 
	`api` = MoneyMatch's API
	`rates_df` = Parameters to Query & Output (provider, to country, to currency, send amount, corridor)
	`currency` = Received Currency
	`output_filename` = File to Store Results

Returns: None
"""
def getMoneyMatchRates(api1, api2, rates_df, output_filename) -> None:
	
	# Initialize variables names to Default Values
	rates = "-"
	fees = "-"
	receive_amt = "-"

	failedFlag = False		# Flag `TRUE` if Failed GET Response / Bad Insert Row
	
	# For Each Row, Send GET Requests and Append Row
	for i in range(0, len(rates_df)):
		row = rates_df.iloc[i]

		# Retrieve Query Rates (Config) Values
		provider = row.iloc[0]
		country = row.iloc[1]
		currency = row.iloc[2]
		amt = row.iloc[3]

		response1 = requests.get(f"{api1}/{currency}")
		response2 = requests.get(f"{api2}&to={currency}")

		# Update Flag if Status Code not 200
		response1_status_code:int = response1.status_code
		response2_status_code:int = response2.status_code
		if(response1_status_code != 200 or response2_status_code != 200):
			failedFlag = True
			continue
		else:
			# Convert Response Data to JSON
			rates = response1.text
			fees = response2.text

			receive_amt = (float(rates) * float(amt)) + float(fees)
			receive_amt = round(receive_amt, 2)
			
			# Retrieve Values & Insert Row
			appendStatus = appendRow(output_filename, provider, country, currency, amt, rates, fees, receive_amt)

			# Update Flag if insert row failed
			if (appendStatus != 0):
				failedFlag = True
			
			time.sleep(10) # Wait for 10 seconds before next API Call

	# If failure occured, return 1, else 0
	if (failedFlag):
		print("[Warning] Rates Extracted for MoneyMatch with Failures.")
	else:
		print("[Success] Rates Extracted for MoneyMatch.")

# ==================================================
# Generate Rates CSV File
"""
Get rates from each get{Provider}Rates(..) simulatenously using `multiprocessing`.
Stores results in the folder './output/...'

Parameters: 
	`configFilename`:str = Configuration File to read/process
	`providers_api`:dict = Dictionary of Providers and Their API URLs

Returns: None
"""
def getRates(configFilename:str, providers_api:dict) -> None:
    
    # Reset CSV Files:
    filenames:list = ["./output/instarem.csv", "./output/moneymatch.csv", "./output/wise.csv", "./output/sunwaymoney.csv"]
    for file in filenames:
        with open(file, 'w', newline="") as output:
            output.write('')
    
    # Read Configuration File as List
    configData = pd.read_csv(configFilename, on_bad_lines="warn", encoding='utf-8', dtype={"amount":int})

    # Define processes for each provider
    processes = [
        Process(target=getWiseRates, args=(providers_api['wise'], configData[configData['provider'] == "Wise"], "./output/wise.csv")),
        Process(target=getInstaremRates, args=(providers_api['instarem'], configData[configData['provider'] == "Instarem"], "./output/instarem.csv")),
        Process(target=getSunwayMoneyRates, args=(providers_api['sunwaymoney'], configData[configData['provider'] == "SunwayMoney"], "./output/sunwaymoney.csv")),
        Process(target=getMoneyMatchRates, args=(providers_api['moneymatch_rates'], providers_api['moneymatch_fees'], configData[configData['provider'] == "MoneyMatch"], "./output/moneymatch.csv"))
    ]

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("All rates have been processed and saved.")