# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 21:23:24 2022

@author: RobWen
Version: 0.4.21
"""

# Packages
import requests
import pandas as pd
import numpy as np
from pandas import json_normalize

# Header
from .TickerRequest import *

class NASDAQRequest(TickerRequest):
    def __init__(self, ticker, headers_standard):
        super().__init__(ticker, headers_standard)
        self.__headers_standard = headers_standard
  
    #########################
    ###                   ###
    ###  NASDAQ Requests  ###
    ###                   ###
    #########################
    
    @property
    def summ(self):
        return self.__nasdaq_summary_df()
    
    @property
    def div_hist(self):
        return self.__nasdaq_dividend_history_df()
    
    @property
    def hist_quotes_stock(self):
        return self.__nasdaq_historical_data_stock_df()
    
    @property
    def hist_quotes_etf(self):
        return self.__nasdaq_historical_data_etf_df()
    
    @property
    def hist_nocp(self):
        return self.__nasdaq_historical_nocp_df()
    
    @property
    def fin_income_statement_y(self):
        return self.__nasdaq_financials_income_statement_y_df()
    
    @property
    def fin_balance_sheet_y(self):
        return self.__nasdaq_financials_balance_sheet_y_df()
    
    @property
    def fin_cash_flow_y(self):
        return self.__nasdaq_financials_cash_flow_y_df()
    
    @property
    def fin_fin_ratios_y(self):
        return self.__nasdaq_financials_financials_ratios_y_df()
    
    @property
    def fin_income_statement_q(self):
        return self.__nasdaq_financials_income_statement_q_df()
    
    @property
    def fin_balance_sheet_q(self):
        return self.__nasdaq_financials_balance_sheet_q_df()
    
    @property
    def fin_cash_flow_q(self):
        return self.__nasdaq_financials_cash_flow_q_df()
    
    @property
    def fin_fin_ratios_q(self):
        return self.__nasdaq_financials_financials_ratios_q_df()
    
    @property
    def earn_date_eps(self):
        return self.__nasdaq_earnings_date_eps_df()
    
    @property
    def earn_date_surprise(self):
        return self.__nasdaq_earnings_date_surprise_df()
    
    @property
    def yearly_earn_forecast(self):
        return self.__nasdaq_earnings_date_yearly_earnings_forecast_df()
    
    @property
    def quarterly_earn_forecast(self):
        return self.__nasdaq_earnings_date_quarterly_earnings_forecast_df()
    
    @property
    def pe_peg_forecast(self):
        return self.__forecast_pe_peg_df()
       
    #####################
    ###               ###
    ###  NASDAQ Data  ###
    ###               ###
    #####################
    
    ### Nasdaq Summary                                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda ###
    ### Rückgabe None implementiert und getestet                ###
    def __nasdaq_summary_df(self):
        
        try:
            # Fetch data from API
            url = f"https://api.nasdaq.com/api/quote/{self.ticker}/summary?assetclass=stocks"
            response = requests.get(url, headers=self.__headers_standard)
            response.raise_for_status()  # Ensure HTTP request was successful
            
            # Fetch JSON data
            data = response.json()['data']['summaryData']
            
            # Validate data
            if not data:
                print("No summary data found.")
                self.__nasdaq_summary_df = None
                return self.__nasdaq_summary_df
            
            # Keys of interest
            keys = [
                'Exchange', 'Sector', 'Industry', 'OneYrTarget', 'TodayHighLow', 'ShareVolume',
                'AverageVolume', 'PreviousClose', 'FiftTwoWeekHighLow', 'MarketCap', 'PERatio',
                'ForwardPE1Yr', 'EarningsPerShare', 'AnnualizedDividend', 'ExDividendDate',
                'DividendPaymentDate', 'Yield'
            ]
            
            # Extract values and labels, with defaults for missing keys (a bit more robust)
            array_value = [data.get(key, {}).get('value', 'N/A') for key in keys]
            array_index = [data.get(key, {}).get('label', key) for key in keys]
            
            # Create DataFrame
            self.__nasdaq_summary_df = pd.DataFrame(array_value, index=array_index, columns=[f"{self.ticker} Key Data"])
                
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            self.__nasdaq_summary_df = None
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.__nasdaq_summary_df = None

        return self.__nasdaq_summary_df
    
    ### Nasdaq Dividend History                                                  ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/dividend-history ###
    ### Rückgabe None implementiert und getestet                                 ###
    def __nasdaq_dividend_history_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/dividends?assetclass=stocks", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['dividends']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['dividends']['headers']
            df_headers = json_normalize(json_headers)
            self.__nasdaq_dividend_history_df = df.rename(columns=df_headers.loc[0])
        except:
            self.__nasdaq_dividend_history_df = None
        
        return self.__nasdaq_dividend_history_df
        
    ### Nasdaq Historical NOCP                                                  ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/historical-nocp ###
    ### Rückgabe None implementiert und getestet                                ###
    def __nasdaq_historical_nocp_df(self):    
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/historical-nocp?timeframe=y1", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['nocp']['nocpTable']
            df = json_normalize(json_data)
            json_headers = json['data']['headers']
            df_headers = json_normalize(json_headers)
            self.__nasdaq_historical_nocp_df = df.rename(columns=df_headers.loc[0])
        except:
            self.__nasdaq_historical_nocp_df = None
        
        return self.__nasdaq_historical_nocp_df
    
    ### Nasdaq Financials Annual Income Statement                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_income_statement_y_df(self): 
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_1 = json['data']['incomeStatementTable']['rows']
            df = json_normalize(json_1)
            json_headers_1 = json['data']['incomeStatementTable']['headers']
            df_headers_1 = json_normalize(json_headers_1)
            self.__nasdaq_financials_income_statement_df = df.rename(columns=df_headers_1.loc[0])
        except:
            self.__nasdaq_financials_income_statement_df = None
        
        return self.__nasdaq_financials_income_statement_df
    
    ### Nasdaq Financials Annual Balance Statement                         ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_balance_sheet_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_2 = json['data']['balanceSheetTable']['rows']
            df = json_normalize(json_2)
            json_headers_2 = json['data']['balanceSheetTable']['headers']
            df_headers_2 = json_normalize(json_headers_2)
            self.__nasdaq_financials_balance_sheet_df = df.rename(columns=df_headers_2.loc[0])
        except:
            self.__nasdaq_financials_balance_sheet_df = None
        
        return self.__nasdaq_financials_balance_sheet_df
    
    ### Nasdaq Financials Annual Cash Flow                                 ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_cash_flow_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_3 = json['data']['cashFlowTable']['rows']
            df = json_normalize(json_3)
            json_headers_3 = json['data']['cashFlowTable']['headers']
            df_headers_3 = json_normalize(json_headers_3)
            self.__nasdaq_financials_cash_flow_df = df.rename(columns=df_headers_3.loc[0])
        except:
            self.__nasdaq_financials_cash_flow_df = None
        
        return self.__nasdaq_financials_cash_flow_df
    
    ### Nasdaq Financials Annual Financial Ratios                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_financials_ratios_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_4 = json['data']['financialRatiosTable']['rows']
            df = json_normalize(json_4)
            json_headers_4 = json['data']['financialRatiosTable']['headers']
            df_headers_4 = json_normalize(json_headers_4)
            self.__nasdaq_financials_financials_ratios_df = df.rename(columns=df_headers_4.loc[0])
        except:
            self.__nasdaq_financials_financials_ratios_df = None
        
        return self.__nasdaq_financials_financials_ratios_df

    ### Nasdaq Financials Quarterly Income Statement                       ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_income_statement_q_df(self): 
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_1 = json['data']['incomeStatementTable']['rows']
            df = json_normalize(json_1)
            json_headers_1 = json['data']['incomeStatementTable']['headers']
            df_headers_1 = json_normalize(json_headers_1)
            self.__nasdaq_financials_income_statement_df = df.rename(columns=df_headers_1.loc[0])
        except:
            self.__nasdaq_financials_income_statement_df = None
        
        return self.__nasdaq_financials_income_statement_df
    
    ### Nasdaq Financials Quarterly Balance Statement                      ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_balance_sheet_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_2 = json['data']['balanceSheetTable']['rows']
            df = json_normalize(json_2)
            json_headers_2 = json['data']['balanceSheetTable']['headers']
            df_headers_2 = json_normalize(json_headers_2)
            self.__nasdaq_financials_balance_sheet_df = df.rename(columns=df_headers_2.loc[0])
        except:
            self.__nasdaq_financials_balance_sheet_df = None
        
        return self.__nasdaq_financials_balance_sheet_df
    
    ### Nasdaq Financials Quarterly Cash Flow                              ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_cash_flow_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_3 = json['data']['cashFlowTable']['rows']
            df = json_normalize(json_3)
            json_headers_3 = json['data']['cashFlowTable']['headers']
            df_headers_3 = json_normalize(json_headers_3)
            self.__nasdaq_financials_cash_flow_df = df.rename(columns=df_headers_3.loc[0])
        except:
            self.__nasdaq_financials_cash_flow_df = None
        
        return self.__nasdaq_financials_cash_flow_df
    
    ### Nasdaq Financials Quarterly Financial Ratios                       ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_financials_ratios_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_4 = json['data']['financialRatiosTable']['rows']
            df = json_normalize(json_4)
            json_headers_4 = json['data']['financialRatiosTable']['headers']
            df_headers_4 = json_normalize(json_headers_4)
            self.__nasdaq_financials_financials_ratios_df = df.rename(columns=df_headers_4.loc[0])
        except:
            self.__nasdaq_financials_financials_ratios_df = None
        
        return self.__nasdaq_financials_financials_ratios_df

    ### Nasdaq Earnings Date Earnings Per Share                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/earnings ###
    ### Rückgabe None implementiert und getestet                         ###
    def __nasdaq_earnings_date_eps_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/eps", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['earningsPerShare']
            self.__nasdaq_earnings_date_eps_df = json_normalize(json_data)
        except:
            self.__nasdaq_earnings_date_eps_df = None
        
        return self.__nasdaq_earnings_date_eps_df


    ### Nasdaq Earnings Date Quarterly Earnings Surprise Amount          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/earnings ###
    ### Rückgabe None implementiert und getestet                         ###
    def __nasdaq_earnings_date_surprise_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/earnings-surprise", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['earningsSurpriseTable']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['earningsSurpriseTable']['headers']
            df_headers = json_normalize(json_headers)
            self.__nasdaq_earnings_date_surprise_df = df.rename(columns=df_headers.loc[0])
        except:
            self.__nasdaq_earnings_date_surprise_df = None
        
        return self.__nasdaq_earnings_date_surprise_df
    
    ### Nasdaq Earnings Date Yearly Earnings Forecast                    ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/earnings ###
    ### Rückgabe None implementiert und getestet                         ###
    def __nasdaq_earnings_date_yearly_earnings_forecast_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/earnings-forecast", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['yearlyForecast']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['yearlyForecast']['headers']
            df_headers = json_normalize(json_headers)
            self.__nasdaq_earnings_date_yearly_earnings_forecast_df = df.rename(columns=df_headers.loc[0])
        except:
            self.__nasdaq_earnings_date_yearly_earnings_forecast_df = None
        
        return self.__nasdaq_earnings_date_yearly_earnings_forecast_df

    ### Nasdaq Earnings Date Quarterly Earnings                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/earnings ###
    ### Rückgabe None implementiert und getestet                         ### 
    def __nasdaq_earnings_date_quarterly_earnings_forecast_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/earnings-forecast", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['quarterlyForecast']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['quarterlyForecast']['headers']
            df_headers = json_normalize(json_headers)
            self.__nasdaq_earnings_date_quarterly_earnings_forecast_df = df.rename(columns=df_headers.loc[0])
        except:
            self.__nasdaq_earnings_date_quarterly_earnings_forecast_df = None
        
        return self.__nasdaq_earnings_date_quarterly_earnings_forecast_df
    
    ### Nasdaq Price/Earnings & PEG Ratios Forecast PEG Ratio                             ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/price-earnings-peg-ratios ###
    ### Rückgabe None implementiert und getestet                                          ###
    def __forecast_pe_peg_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/peg-ratio", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data_forecast_pe = json['data']['per']['peRatioChart']
            json_data_forecast_gr = json['data']['gr']['peGrowthChart']
            json_data_forecast_peg = json['data']['pegr']
            
            df_forecast_pe = json_normalize(json_data_forecast_pe)                  # Dataframe
            df_forecast_gr = json_normalize(json_data_forecast_gr)                  # Dataframe
            df_forecast_peg = json_normalize(json_data_forecast_peg)                # Dataframe
            
            df_forecast_gr_array = df_forecast_gr['z'] + ' ' + df_forecast_gr['x']  # Series

            arrays = [
                np.array(["Price/Earnings Ratio","Price/Earnings Ratio","Price/Earnings Ratio","Price/Earnings Ratio"
                          , "Forecast P/E Growth Rates", "Forecast P/E Growth Rates", "Forecast P/E Growth Rates"
                          , "Forecast P/E Growth Rates", "PEG Ratio"]),
                np.array(df_forecast_pe.iloc[0:,0].tolist() + df_forecast_gr_array.tolist() + df_forecast_peg.iloc[0:,0].tolist())]
            
            array_table = df_forecast_pe.iloc[0:,1].tolist() + df_forecast_gr.iloc[0:,2].tolist() + df_forecast_peg.iloc[0:,-1].tolist()
            
            s = pd.DataFrame(array_table , index=arrays, columns = [self.ticker + ' Price/Earnings & PEG Ratios'])
            
            self.__forecast_pe_peg_df = s
        except:
            self.__forecast_pe_peg_df = None
        
        return self.__forecast_pe_peg_df
    
    ### Nasdaq Historical Data Stocks                                      ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/historical ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_historical_data_stock_df(self):
        from datetime import datetime
        datum = datetime.today().strftime('%Y-%m-%d')
        
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/historical?assetclass=stocks&fromdate=2011-09-26&limit=9999&todate={datum}", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['tradesTable']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['tradesTable']['headers']
            df_headers = json_normalize(json_headers)
            self.__nasdaq_historical_data_stock_df = df.rename(columns=df_headers.loc[0])
        except:
            self.__nasdaq_historical_data_stock_df = None
        
        return self.__nasdaq_historical_data_stock_df
    
    ### Historical Data ETF                                                ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/historical ###
    ### Nasdaq Rückgabe None implementiert und getestet                    ###
    def __nasdaq_historical_data_etf_df(self):
        from datetime import datetime
        datum = datetime.today().strftime('%Y-%m-%d')
        
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/historical?assetclass=etf&fromdate=2011-09-26&limit=9999&todate={datum}", headers=self.__headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['tradesTable']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['tradesTable']['headers']
            df_headers = json_normalize(json_headers)
            self.__nasdaq_historical_data_etf_df = df.rename(columns=df_headers.loc[0])
        except:
            self.__nasdaq_historical_data_etf_df = None
        
        return self.__nasdaq_historical_data_etf_df