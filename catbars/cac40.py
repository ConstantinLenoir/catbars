

"""
Financial data relative to the CAC 40 components
16/03/2020

'data' is a dict mapping company names to a list of three
features with three significant digits:
1. closing price,
2. market cap.,
3. ICB industry sector.

NOTE
An outstanding share number includes the share float but
not treasury shares.

ICB (industry classification benchmark) is a globally
utilized standard for the categorization and
comparison of companies by industry and sector.

SOURCE
https://live.euronext.com/en/markets/paris/equities/list
"""

date = '16/03/2020'

data = {
    'LVMH': [298, 150e9, 'Consumer goods'] ,
    'L\'OREAL': [208, 116e9, 'Consumer goods'],
    'SANOFI' : [77.0, 96.0e9, 'Health care'],
    'AIRBUS' : [69, 54.0e9, 'Industrials'],
    'TOTAL' : [24.3, 63.3e9, 'Oil and gas'],
    'HERMES' : [548, 57.9e9, 'Consumer goods'],
    'KERING' : [378, 47.7e9, 'Consumer services'],
    'AIR LIQUIDE' : [99.2, 47.0e9, 'Basic materials'],
    'BNP PARIBAS' : [27.4, 34.3e9, 'Financials'],
    'VINCI' : [59.0, 35.8e9, 'Industrials'],
    'ESSILORLUXOTTICA' : [96.0, 41.9e9, 'Health care'],
    'SCHNEIDER ELECTRIC' : [70.4, 41.0e9, 'Industrials'],
    'AXA' : [13.4, 32.5e9, 'Financials'],
    'SAFRAN' : [74.5, 29.9e9, 'Industrials'],
    'DANONE' : [54.0, 37.0e9, 'Consumer goods'],
    'PERNOD RICARD' : [122, 32.4e9, 'Consumer goods'],
    'ENGIE' : [10.0, 24.3e9, 'Utilities'],
    'DASSAULT SYSTEMES' : [108, 28.5e9, 'Technology'],
    'ORANGE' : [9.40, 25.0e9, 'Telecommunications'],
    'CREDIT AGRICOLE' : [6.08, 17.5e9, 'Financials'],
    'VIVENDI' : [17.6, 20.8e9, 'Consumer services'],
    'SOCIETE GENERALE' : [14.5, 12.4e9,'Financials'],
    'STMICROELECTRONICS' : [16.4, 15.0e9, 'Technology'],
    'THALES' : [65.8, 14.0e9, 'Industrials'],
    'LEGRAND' : [50.8, 13.6e9, 'Industrials'],
    'SAINT-GOBAIN' : [19.4, 10.5e9, 'Industrials'],
    'MICHELIN' : [71.0, 12.7e9, 'Consumer goods'],
    'CAPGEMINI' : [62.7, 10.6e9, 'Technology'],
    'PSA' : [11.0, 9.98e9, 'Consumer goods'],
    'UNIBAIL-RODAMCO-WESTFIELD' : [58.1, 8.04e9, 'Financials'],
    'VEOLIA' : [17.5, 9.95e9, 'Utilities'],
    'BOUYGUES' : [24.2, 9.20e9, 'Industrials'],
    'ARCELORMITTAL' : [7.19, 7.34e9, 'Basic materials'],
    'SODEXO' : [56.5, 8.33e9, 'Consumer services'],
    'CARREFOUR' : [12.9, 10.4e9, 'Consumer services'],
    'ACCOR' : [24.2, 6.54e9, 'Consumer services'],
    'PUBLICIS' : [22.9, 5.51e9, 'Consumer services'],
    'RENAULT' : [14.6, 4.30e9, 'Consumer goods'],
    'ATOS' : [47.6, 5.20e9, 'Technology'],
    'TECHNIPFMC' : [5.92, 2.65e9, 'Oil and gas']
    }

    
