# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:58:25 2024

@author: RobWen
Version: 0.4.16
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Header
from .TickerRequest import *

class BoersengefluesterRequest(TickerRequest):
    def __init__(self, ticker, headers_standard):
        super().__init__(ticker, headers_standard)
        self.__headers_standard = headers_standard

    ##############################
    ###                        ###
    ###  Boersengefluester     ###
    ###       Requests         ###
    ###                        ###
    ##############################

    @property
    def finanzdaten(self):
            return self.__boersengefluester_finanzdaten()
    
    @property
    def dataselect_universum(self):
            return self.__boersengefluester_finanzdaten_dataselect()

    ##############################
    ###                        ###
    ###  Boersengefluester     ###
    ###         Data           ###
    ###                        ###
    ##############################

    def __boersengefluester_finanzdaten_dataselect(self):
        try:
            # Fetch the webpage content
            url = "https://www.boersengefluester.de/dataselect/"
            page = requests.get(url)
            page.raise_for_status()  # Raise an error for non-200 status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the webpage: {e}")
            return None
    
        try:
            # Parse the webpage content
            soup = BeautifulSoup(page.content, 'html.parser')
    
            # Find all relevant <td> elements
            td_elements = soup.find_all('td', style='text-align:left; padding-left:8px; font-family: tahoma;')
    
            if not td_elements:
                raise ValueError("No matching <td> elements found")
    
            # Initialize an empty list to store the extracted data
            data = []
    
            # Loop through the td elements and process the data
            for i in range(0, len(td_elements), 3):
                try:
                    data.append({
                        'Company Name': td_elements[i].text.strip(),
                        'ISIN': td_elements[i + 1].find('a').text.strip(),
                        'Ticker': td_elements[i + 2].text.strip()
                    })
                except (IndexError, AttributeError) as e:
                    print(f"Error extracting data from elements: {e}")
                    continue
    
            # Convert the list of dictionaries into a Pandas DataFrame
            df = pd.DataFrame(data)
    
            return df
    
        except Exception as e:
            print(f"An error occurred during parsing or data extraction: {e}")
            return None

    def __boersengefluester_finanzdaten(self):
        df = self.__boersengefluester_finanzdaten_dataselect()
        isin_to_check = self.ticker
        if isin_to_check in df['ISIN'].values:
            try:
                url = f"https://www.boersengefluester.de/isin-details/?isin={self.ticker}"
                page = requests.get(url, headers = self.__headers_standard)
                page.raise_for_status()  # Raise an error for non-200 status codes
                soup = BeautifulSoup(page.content, 'html.parser')
        
                dividende_table = soup.find_all('div', {'class':'dividende_table'})
                if not dividende_table:
                    raise ValueError("Dividende table not found")
        
                # Entfernt leere Felder
                data = dividende_table[1].text.splitlines()
                data = [item for item in data if item.strip()]
                
                # Extracting column names
                columns = data[1:13]
        
                # Extracting data values
                data_values = [data[i:i+13] for i in range(13, len(data), 13)]
        
                # Specifying index names
                index = ['Umsatzerlöse', 'EBITDA', 'EBITDA-Marge', 'EBIT', 'EBIT-Marge', 
                         'Jahresüberschuss', 'Netto-Marge', 'Cashflow', 'Ergebnis je Aktie', 'Dividende']
                
                # Creating DataFrame
                return pd.DataFrame([data_values[i][1:] for i in range(len(data_values))], columns=columns, index=index)
        
            except requests.RequestException as e:
                print(f"Error fetching data: {e}")
                return None
            except ValueError as e:
                print(f"Error: {e}")
                return None
        else:
            print("No data found")
            return None