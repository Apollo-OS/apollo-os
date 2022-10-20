# APOLLO Market Analyzer
# Author: Dimitris Papakyriakopoulos
# Copyright protected under the MIT LICENSE
# Date: 10/09/2022


from turtle import st
from matplotlib.ticker import is_close_to_int
import pandas as pd
import yfinance as yf
import sqlite3
import pprint
import plotly.graph_objects as go
from colorama import Fore 
from colorama import Style
from tabulate import tabulate
import colored
import numpy as np
import scipy.stats as stats
import seaborn as sea
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename
from plotly.subplots import make_subplots
from sklearn import linear_model
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, r2_score


def menu():
    menu = []
    menu.append(["MENU", "Description"])
    menu.append(["info", " Learn more about key modules in Apollo"])
    menu.append(["stock", " Study a S&P 500 company"])
    menu.append(["index", " Filter S&P 500"])
    menu.append(["sml", " Security Market Line"])
    menu.append(["help", " Show menu"])
    menu.append(["Exit", " Exit Apollo OS"])
    menu= pd.DataFrame(menu, columns=["MENU", "Description"])

    pdtabulate=lambda menu:tabulate(menu,headers='firstrow',tablefmt='fancy_grid', showindex=False)
    print(colored.fg("sky_blue_1"), pdtabulate(menu))

def menuX():
    menu = []
    menu.append(["MENU", "Description"])
    menu.append(["info", " Learn more about key modules in Apollo"])
    menu.append(["stock", " Study a S&P 500 company"])
    menu.append(["index", " Filter S&P 500"])
    menu.append(["analysis", " Technical analysis of portfolio"])
    menu.append(["sml", " Security Market Line"])
    menu.append(["help", " Show menu"])
    menu.append(["save", " Save portfolio and data"])
    menu.append(["Exit", " Exit Apollo OS"])
    menu= pd.DataFrame(menu, columns=["MENU", "Description"])

    pdtabulate=lambda menu:tabulate(menu,headers='firstrow',tablefmt='fancy_grid', showindex=False)
    print(colored.fg("sky_blue_1"), pdtabulate(menu))



def infoMenu():
    menu = []
    menu.append(["MENU", "Description"])
    menu.append(["tickers", " Display all S&P 500 tickers"])
    menu.append(["sectors", " Display all sectors in S&P 500"])
    menu.append(["industries", " Display all industries in S&P 500"])
    menu.append(["docs", " Show Apollo-OS documentation"])
    menu.append(["help", " Show menu"])
    menu.append(["..", " Go back"])
    menu= pd.DataFrame(menu, columns=["MENU", "Description"])

    pdtabulate=lambda menu:tabulate(menu,headers='firstrow',tablefmt='fancy_grid', showindex=False)
    print(colored.fg("sky_blue_1"), pdtabulate(menu))


def displayTickers():
    # Create SQLite database
    connection = sqlite3.connect('apollo.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM Analysis''')
    connection.commit()

    data = cursor.fetchall()
    dataset = pd.DataFrame(data, columns=["Ticker", "Name", "Market Cap", "Sector", "Industry", "EPS", "PE", "ROE", "DE", "Interest Cov.", "EV/EBITDA", "Operating Margins", "Working Capital", "Gross Margins", "Book", "Divindend Yield", "Beta", "EarningsGrowth", "Quick ratio", "RPS"])
    pd.set_option('display.width', 5000)

    with pd.option_context('display.max_rows', None, 'display.max_columns', 2):  # more options can be specified also
            print(dataset[["Ticker", "Name"]])


    #Close DB connection
    connection.close()


def displaySectors():
    sectors = []
    sectors.append("Basic Materials")
    sectors.append("Communication Services")
    sectors.append("Consumer Cyclical")
    sectors.append("Consumer Defensive")
    sectors.append("Energy")
    sectors.append("Financial Services")
    sectors.append("Healthcare")
    sectors.append("Industrials")
    sectors.append("Real Estate")
    sectors.append("Technology")
    sectors.append("Utilities")
    pprint.pprint(sectors)


def displayIndustries():
    sectors = []
    sectors.append("Basic Materials")
    sectors.append("Communication Services")
    sectors.append("Consumer Cyclical")
    sectors.append("Consumer Defensive")
    sectors.append("Energy")
    sectors.append("Financial Services")
    sectors.append("Healthcare")
    sectors.append("Industrials")
    sectors.append("Real Estate")
    sectors.append("Technology")
    sectors.append("Utilities")

    # Create SQLite database
    connection = sqlite3.connect('apollo.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM Analysis''')
    connection.commit()
    data = cursor.fetchall()
    dataset = pd.DataFrame(data, columns=["Ticker", "Name", "Market Cap", "Sector", "Industry", "EPS", "PE", "ROE", "DE", "Interest Cov.", "EV/EBITDA", "Operating Margins", "Working Capital", "Gross Margins", "Book", "Divindend Yield", "Beta", "EarningsGrowth", "Quick ratio", "RPS"])
    pd.set_option('display.width', 5000)
    #Close DB connection
    connection.close()
    ind = pd.DataFrame()
    for sector in sectors:
        working_dataset = dataset[dataset["Sector"] == sector]
        industries =  working_dataset["Industry"].unique()
        print(Fore.GREEN+"\nSector: "+ sector)
        print(Fore.WHITE+"")
        pprint.pprint(list(industries))

def info():
    infoMenu()
    option =input(Fore.WHITE+"Apollo-OS/home/info $ ")
    while option != "..":    
        if(option == "tickers"):
            displayTickers()
        elif(option == "sectors"):
            displaySectors()
        elif(option == "industries"):
            displayIndustries()
        elif(option == "docs"):
            print(Fore.YELLOW+"This function is not available yet.")
        elif(option == "help"):
            infoMenu()
        option = input(Fore.WHITE+"Apollo-OS/home/info $ ")

# ------------------------------------------------------------------------------------------------#

# ------------------------------------------------------------------------------------------------#

def stockMenu():
    menu = []
    menu.append(["MENU", "Description"])
    menu.append(["business", " Company Business Summary"])
    menu.append(["history", " Historical data"])
    menu.append(["actions", " Actions (Dividends, splits, etc.)"])
    menu.append(["financials", "Financials"])
    menu.append(["major", " Major Holders"])
    menu.append(["institutional", "Institutional Holders"])
    menu.append(["balance_sheet", "Balance Sheet"])
    menu.append(["cash_flow", "Cash Flow"])
    menu.append(["earnings", "Earnings"])
    menu.append(["sustainability", "Sustainability"])
    menu.append(["events", "Upcoming events"])
    menu.append(["news", "News"])
    menu.append(["options", "Options"])
    menu.append(["chart", "Chart"])
    menu.append(["summary", "Company summary table"])
    menu.append(["excel", "Export stock template to excel"])
    menu.append(["change", "Change company"])
    menu.append(["help", "Show menu"])
    menu.append(["..", "Go back"])
    menu= pd.DataFrame(menu, columns=["Options", "Description"])
    pdtabulate=lambda menu:tabulate(menu,headers='firstrow',tablefmt='fancy_grid')
    print(colored.fg("sky_blue_1"), pdtabulate(menu))


def to_excel(company):
    cc = ["Name", "Ticker", "Sector", "Industry", "Market Cap", "Beta", "Rating", "Summary"]
    l = []
    l.append(company.info['longName'])
    l.append(company.info['symbol'])
    l.append(company.info['sector'])
    l.append(company.info['industry'])
    l.append(company.info['marketCap'])
    l.append(company.info['beta'])
    l.append(company.info['morningStarOverallRating'])
    l.append(company.info['longBusinessSummary'])
    df = pd.DataFrame (l, columns = ['Data'])
    df['COMPANY'] = cc
    df.set_index('COMPANY', drop=True, inplace=True)

    history = yf.download(company.info['symbol'], period="2y", interval="1d", auto_adjust=True) #historical data for last 2y

    Tk().withdraw()
    file = asksaveasfilename(defaultextension=".xlsx")
    with pd.ExcelWriter(file) as writer:
       df.to_excel(writer, sheet_name="COMPANY INFO")
       history.to_excel(writer, sheet_name="HISTORICAL DATA")
       company.balance_sheet.to_excel(writer, sheet_name="BALANCE SHEET")
       company.earnings.to_excel(writer, sheet_name="EARNINGS")
       company.financials.to_excel(writer, sheet_name="FINANCIALS")
       company.cashflow.to_excel(writer, sheet_name="CASH FLOW")



def stockSummary(company):
    cc = ["Name", "Ticker", "Sector", "Industry", "Market Cap", "Beta", "Rating", "Summary", "EBITDA", "EARNINGS GROWTH", "PAYOUT RATIO", "QUICK RATIO", "RPS", "P/B", "Target High Price", "Target Low Price", "EPS", "PE", "DE", "avg VOLUME"]
    l = []
    l.append(company.info['longName'])
    l.append(company.info['symbol'])
    l.append(company.info['sector'])
    l.append(company.info['industry'])
    l.append(company.info['marketCap'])
    l.append(company.info['beta'])
    l.append(company.info['morningStarOverallRating'])
    l.append(company.info['longBusinessSummary'])
    l.append(company.info['ebitda'])
    l.append(company.info['earningsGrowth'])
    l.append(company.info['payoutRatio'])
    l.append(company.info['quickRatio'])
    l.append(company.info['revenuePerShare'])
    l.append(company.info['priceToBook'])
    l.append(company.info['targetHighPrice'])
    l.append(company.info['targetLowPrice'])
    l.append(company.info['trailingEps'])
    l.append(company.info['trailingPE'])
    l.append(company.info['debtToEquity'])
    l.append(company.info['averageVolume'])
    df = pd.DataFrame (l, columns = ['Data'])
    df['COMPANY'] = cc
    df.set_index('COMPANY', drop=True, inplace=True)
    with pd.option_context('display.max_rows', None, 'display.max_columns', 2):  # more options can be specified also
            print(df)



def studyStock():
    stock = input("Choose a ticker: ")
    company = yf.Ticker(stock)  #error handling needed
    stockMenu()
    option =input(Fore.WHITE+"Apollo-OS/home/stock $ ")
    while option != "..":
        if(option == "business"):
          pprint.pprint(company.info['longBusinessSummary'])
        elif(option == "history"):
            print("Choose a timeframe:")
            print("1d\t5d\t1mo\t3mo\t6mo\t1y\t2y\t5y\t10y\tmax\tytd")
            p = input("Timeframe: ")
            pprint.pprint(company.history(period=p))
        elif(option == "actions"):
            pprint.pprint(company.actions)
        elif(option == "financials"):
           pprint.pprint(company.financials)
        elif(option == "major"):
            pprint.pprint(company.major_holders)
        elif(option == "institutionals"):
            pprint.pprint(company.institutional_holders)
        elif(option == "balance_sheet"):
            pprint.pprint(company.balance_sheet)
        elif(option == "cash_flow"):
            pprint.pprint(company.cashflow)
        elif(option == "earnings"):
            pprint.pprint(company.earnings)
        elif(option == "sustainability"):
            pprint.pprint(company.sustainability)
        elif(option == "events"):
            pprint.pprint(company.calendar)
        elif(option == "news"):
            pprint.pprint(company.news)
        elif(option == "options"):
            pprint.pprint(company.options)
        elif(option == "chart"):
            data = yf.download(stock, period="2y", interval="1d", auto_adjust=True) #Fix time series for chart
            fig3 = make_subplots(specs=[[{"secondary_y": True}]])
            fig3.add_trace(go.Candlestick(x=data.index,
                                        open=data['Open'],
                                        high=data['High'],
                                        low=data['Low'],
                                        close=data['Close'],
                                        name='Price'))
            fig3.add_trace(go.Scatter(x=data.index,y=data['Close'].rolling(window=20).mean(),marker_color='blue',name='20 Day MA'))
            fig3.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', marker={'color':'red'}),secondary_y=True)
            fig3.update_yaxes(range=[0,700000000],secondary_y=True)
            fig3.update_yaxes(visible=False, secondary_y=True)
            fig3.update_layout(xaxis_rangeslider_visible=False)  #hide range slider
            fig3.update_layout(title={'text':stock, 'x':0.5})
            fig3.show()
        elif(option == "summary"):
            stockSummary(company)
        elif(option == "excel"):
            to_excel(company)
        elif(option == "change"):
            stock = input("Choose a ticker: ")
            company = yf.Ticker(stock)   #error handling needed
        elif(option == "help"):
            stockMenu()
        else:
            print("Error! Invalid input.\n")
        option = input(Fore.WHITE+"Apollo-OS/home/stock $ ")

# ------------------------------------------------------------------------------------------------#

# ------------------------------------------------------------------------------------------------#

def apolloMenu():
    menu = []
    menu.append(["MENU", "Description"])
    menu.append(["display", " Display all stocks"])
    menu.append(["displaylong", "  Display all stocks long"])
    menu.append(["add", " Add filter"])
    menu.append(["delete", " Delete filter"])
    menu.append(["clear", " Clear filters"])
    menu.append(["sort", " Sort companies based on attribute"])
    menu.append(["top10", " Display top 10 companies based on current filters and sort order"])
    menu.append(["top50", " Display top 50 companies based on current filters and sort order"])
    menu.append(["top100", " Display top 100 companies based on current filters and sort order"])
    menu.append(["hold", "Save current assets with applied filters and order"])
    menu.append(["score", "Rank assets based on cummulative score"])
    menu.append(["..", " Go back"])
    menu= pd.DataFrame(menu, columns=["MENU", "Description"])

    pdtabulate=lambda menu:tabulate(menu,headers='firstrow',tablefmt='fancy_grid', showindex=False)
    print(colored.fg("sky_blue_1"), pdtabulate(menu))


def filtersList():
    ratios =  ["name", "marketcap", "sector", "industry", "eps", "pe", "roe", "de", "intcov", "ev/ebitda", "opem", "working", "gm", "book", "divYield", "beta", "earnings", "quick", "rps"]
    print("\n")
    print("-------- CHOOSE A RATIO --------")
    count = 0
    for x in ratios:
        count += 1
        print(str(count) + ".  " + x + "\t", end=" ")
        if(count % 2 == 0):
            print("\n", end=" ")
    print("\n")


def examineRule(rule):  
    ratios =  ["name", "marketcap", "sector", "industry", "eps", "pe", "roe", "de", "intcov", "ev/ebitda", "opem", "working", "gm", "book", "divYield", "beta", "earnings", "quick", "rps"]
    operators = ["<", "<=", "=", ">=", ">"]
    fouls = 0
    ratio = ""
    value = ""
    operator = ""
    found = False
    isList = False
    for i in range(len(rule)):
        if (rule[i] == "<" or rule[i] == "=" or rule[i] == ">"):
            if (found == True):
                operator += rule[i]
            else:
                operator += rule[i]
                found = True
        elif (found == False):
            ratio += rule[i]
        else:
            value += rule[i]
    if (operator not in operators):
        print(Fore.RED+"Operator is not valid. Try again!\n\n")
        fouls +=1
    if (ratio not in ratios):
        print(Fore.RED+"Filter is not valid. Try again!\n\n")
        fouls += 1
    if ( ratio != "name" and ratio != "sector" and ratio != "industry"):
        try:
            v = float(value)
        except:
            print(Fore.RED+"Value must be a number. Try again!\n\n")    
            fouls += 1
    if (ratio == "sector"):
        if (value[0] == "["):
            isList = True
        if isList:
            values = []
            current = ""
            for i in range(1, len(value)):
                if (value[i] == "," or value[i] == "]"):
                    values.append(current)
                    current = ""
                else:
                    current += value[i]
            value = values  
    return ratio, operator, value, fouls, isList    


def applyRule(dataset, dct,  rules):
    for rule in rules:
        ratio = rule[0]
        operator = rule[1]
        value = rule[2]
        if (ratio != "name" and ratio != "sector" and ratio != "industry"):
            if (operator == "<="):
                custom = dataset[dataset[dct[ratio]] <= float(value)]
            elif (operator == "<"):
                custom = dataset[dataset[dct[ratio]] < float(value)]
            elif (operator == "="):
                custom = dataset[dataset[dct[ratio]] == float(value)]
            elif (operator == ">"):
                custom = dataset[dataset[dct[ratio]] > float(value)]
            elif (operator == ">="):
                custom = dataset[dataset[dct[ratio]] >= float(value)]
        elif (ratio == "sector" and rule[3] == True):
            custom = dataset[dataset["Sector"].isin(value)]
        else:
            custom = dataset[dataset[dct[ratio]] == value]
        dataset = custom.copy()
    if (len(rules) == 0):
        return dataset
    else:
        return custom        


def addFilter(dataset, rules):
    ratios =  ["name", "marketcap", "sector", "industry", "eps", "pe", "roe", "de", "intcov", "ev/ebitda", "opem", "working", "gm", "book", "divYield", "beta", "earnings", "quick", "rps"]
    a = ["Name", "Market Cap", "Sector", "Industry", "EPS", "PE", "ROE", "DE", "Interest Cov.", "EV/EBITDA", "Operating Margins", "Working Capital", "Gross Margins", "Book", "Divindend Yield", "Beta", "EarningsGrowth", "Quick ratio", "RPS"]
    dct = dict(zip(ratios, a))
    filtersList()
    print("\n")
    accepted = False
    while accepted == False:
        print(Fore.CYAN+"Filter rules MUST follow this format: {filter}{operator}{value}. For example: eps>1.5\n\n")
        rule = input(Fore.LIGHTYELLOW_EX+"Add rule:  ")
        ratio, operator, value, fouls, isList = examineRule(rule)
        if (fouls == 0):
            accepted = True
    if (accepted == True):
        rule_new = [ratio, operator, value, isList]
        rules.append(rule_new)
        return rules


def deleteFilter(rules, long):
    if (len(rules) == 0 and long == None):
        print(Fore.WHITE+"There are no rules to delete!")
    else:
        print(Fore.WHITE+"Choose which filter to delete:\n")
        print(Fore.GREEN+"For example: Choose {1} to delete first filter\n")
        print(Fore.WHITE+"---------------- RULES ----------------\n")
        index = 0
        for rule in rules:
            index += 1
            ratio = rule[0]
            operator = rule[1]
            value = rule[2]
            print(str(index) + ". " + ratio + " " + operator + " " + value)
        if long != None:
            index += 1
            print(str(index) + ". " + "Top"+str(long))
        delete = int(input(Fore.LIGHTYELLOW_EX+"Delete filter rule:  "))
        while delete > index:
            print(Fore.RED+"Error! There is no such filter. Try again\n")
            delete = int(input(Fore.LIGHTYELLOW_EX+"Delete filter rule:  "))
        if (delete == index):
            long = None
        else:
            del(rules[delete - 1])
    return rules, long      


def sortStocks():
    ratios =  ["name", "marketcap", "sector", "industry", "eps", "pe", "roe", "de", "intcov", "ev/ebitda", "opem", "working", "gm", "book", "divYield", "beta", "earnings", "quick", "rps"]
    a = ["Name", "Market Cap", "Sector", "Industry", "EPS", "PE", "ROE", "DE", "Interest Cov.", "EV/EBITDA", "Operating Margins", "Working Capital", "Gross Margins", "Book", "Divindend Yield", "Beta", "EarningsGrowth", "Quick ratio", "RPS"]
    dct = dict(zip(ratios, a))
    filtersList()
    print("\n")
    accepted = False
    while accepted == False:
        print(Fore.CYAN+"Sorting options MUST follow this format: {filter}{,}{sort_option}. For example: marketcap,asc\n\n")
        try:
            ratio, order = input(Fore.LIGHTYELLOW_EX+"Add sorting option:  ").split(",")
            accepted = True
        except:
            accepted = False
        if ((ratio not in ratios) or (order != "asc" and order != "desc")  ):
            accepted = False
    return True, order, dct[ratio]
        

def printStocks(dataset, rules, long = None, sorted = False, order = None, key = None, returns_dataset: bool = False):
    ratios =  ["name", "marketcap", "sector", "industry", "eps", "pe", "roe", "de", "intcov", "ev/ebitda", "opem", "working", "gm", "book", "divYield", "beta", "earnings", "quick", "rps"]
    a = ["Name", "Market Cap", "Sector", "Industry", "EPS", "PE", "ROE", "DE", "Interest Cov.", "EV/EBITDA", "Operating Margins", "Working Capital", "Gross Margins", "Book", "Divindend Yield", "Beta", "EarningsGrowth", "Quick ratio", "RPS"]
    dct = dict(zip(ratios, a))
    custom = applyRule(dataset, dct, rules)
    if (sorted == True):
        if (order == "asc"):
            custom.sort_values(by=[key], inplace = True)
        else:
            custom.sort_values(by=[key], inplace = True, ascending= False)
    if (returns_dataset == True):
        if (long != None):
            custom = custom.head(long)
        return custom
    else:
        c = custom[["Ticker", "Name", "Sector", "Industry", "Market Cap", "EPS", "PE", "Beta", "Quick ratio"]]
        if (long != None):
            c = c.head(long)
        with pd.option_context('display.max_rows', None, 'display.max_columns', 8):  # more options can be specified also
            print(c)


def apollo(rules, sorted = False, order = None, key = None, long = None, saved = False):
    # Create SQLite database
    connection = sqlite3.connect('apollo.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM Analysis''')
    connection.commit()

    data = cursor.fetchall()
    dataset = pd.DataFrame(data, columns=["Ticker", "Name", "Market Cap", "Sector", "Industry", "EPS", "PE", "ROE", "DE", "Interest Cov.", "EV/EBITDA", "Operating Margins", "Working Capital", "Gross Margins", "Book", "Divindend Yield", "Beta", "EarningsGrowth", "Quick ratio", "RPS"])
    pd.set_option('display.width', 5000)
    pd.set_option('display.max_rows', dataset.shape[0]+1)
    apolloMenu()
    option = input(Fore.WHITE+"Apollo-OS/home/index $ ")
    while option != "..":
        if(option == "display"):
            printStocks(dataset, rules, 50, sorted, order, key)
        elif(option == "displaylong"):
            printStocks(dataset, rules, long, sorted, order, key)
        elif(option == "add"):
            rules = addFilter(dataset, rules)
        elif(option == "delete"):
            rules, long = deleteFilter(rules, long)
        elif(option == "clear"):
            rules.clear()
            sorted = False
            order = None
            key = None
            long = None
        elif(option == "sort"):
            sorted, order, key = sortStocks()
        elif(option == "top10"):
            long = 10
            printStocks(dataset, rules, long, sorted, order, key)
        elif(option == "top50"):
            long = 50
            printStocks(dataset, rules, long, sorted, order, key)
        elif(option == "top100"):
            long = 100
            printStocks(dataset, rules, long, sorted, order, key)
        elif(option == "hold"):
            saved = True
            custom = printStocks(dataset, rules, long, sorted, order, key, returns_dataset=True)
        elif(option == "score"):
            pass
        elif(option == "help"):
            apolloMenu()
        else:
            print(Fore.RED+"Error! This is not a valid command.\n")
        option = input(Fore.WHITE+"Apollo-OS/home/index $ ")
    #Close DB connection
    connection.close()
    if saved:
        return custom, rules, saved, sorted, order, key, long
    else:
        return None, rules, saved, sorted, order, key, long

def analysisMenu():
    menu = []
    menu.append(["MENU", "Description"])
    menu.append(["descriptive", " Calculate a range of descriptive statistics (Mean, Var, StDev, Kurtosis, Skewness"])
    menu.append(["corr", " Calculate correlation matrix of portfolio"])
    menu.append(["cov", " Calculate covariance matrix of portfolio"])
    menu.append(["help", " Show menu"])
    menu.append(["..", " Go back"])
    menu= pd.DataFrame(menu, columns=["MENU", "Description"])

    pdtabulate=lambda menu:tabulate(menu,headers='firstrow',tablefmt='fancy_grid', showindex=False)
    print(colored.fg("sky_blue_1"), pdtabulate(menu))


def descriptive(tickers, historical_data):
    krts = []
    skews = []
    for i in range(len(tickers)):
        kurtosis = stats.kurtosis(historical_data.iloc[:,i])
        krts.append(kurtosis)
        skewness = stats.kurtosis(historical_data.iloc[:,i])
        skews.append(skewness)
    df = pd.DataFrame(list(zip(krts,skews)), columns=["Kurtosis", "Skewness"],  index=tickers)
    frames = [historical_data.describe().transpose().sort_index(axis=0), df.sort_index(axis=0)]
    result = pd.concat(frames, axis=1)
    print(result)
    return result


def correlation(historical_data):
    plt.figure(figsize=(16, 6))
    heatmap = sea.heatmap(historical_data.corr(), vmin=-1, vmax=1, annot=True)
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':10}, pad=12)
    plt.show()
    return historical_data.corr()


def covariance(historical_data):
    plt.figure(figsize=(16, 6))
    heatmap = sea.heatmap(historical_data.cov(), annot=True)
    heatmap.set_title('Covariance Heatmap', fontdict={'fontsize':10}, pad=12)
    plt.show()
    return historical_data.cov()


def analysis(tickers):
    historical_data = yf.download(tickers, period="2y", interval="1d", auto_adjust=True)['Close']
    desc = None
    cor = None
    cov = None
    analysisMenu()
    option = input(Fore.WHITE+"Apollo-OS/home/analysis $ ")
    while option != "..":
        if(option == "descriptive"):
            desc = descriptive(tickers, historical_data)
        elif(option == "corr"):
            cor = correlation(historical_data)
        elif(option == "cov"):
            cov = covariance(historical_data)
        elif(option == "help"):
            analysisMenu()
        else:
            print(Fore.RED+"Error! This is not a valid command.\n")
        option = input(Fore.WHITE+"Apollo-OS/home/analysis $ ")
    return historical_data, desc



def save(custom, historical_data, descriptive):
    Tk().withdraw()
    file = asksaveasfilename(defaultextension=".xlsx")
    with pd.ExcelWriter(file) as writer:  
        custom.to_excel(writer, sheet_name='Asset Overview')
        historical_data.to_excel(writer, sheet_name='Historical Data')
        descriptive.to_excel(writer, sheet_name='Descriptive')
        historical_data.corr().to_excel(writer, sheet_name='Correlation')
        historical_data.cov().to_excel(writer, sheet_name='Covariance')


def smlMenu():
    menu = []
    menu.append(["MENU", "Description"])
    menu.append(["summary", "Summary on coefficients"])
    menu.append(["chart", " Display Security Market Line"])
    menu.append(["rating", " Table of under/fair/over valued companies based on SML"])
    menu.append(["help", " Show menu"])
    menu.append(["..", " Go back"])
    menu= pd.DataFrame(menu, columns=["MENU", "Description"])

    pdtabulate=lambda menu:tabulate(menu,headers='firstrow',tablefmt='fancy_grid', showindex=False)
    print(colored.fg("sky_blue_1"), pdtabulate(menu))


def sumSML(coef, con, mse, cod):
    print(Fore.YELLOW+'Intercept: \n', con)
    print(Fore.YELLOW+'Coefficients: \n', coef)
    print(Fore.YELLOW+"Mean squared error: %.2f",  mse)
    print(Fore.YELLOW+"Coefficient of determination: %.2f", cod)


def graphSML(x, y, y2, labels):
    fig = plt.figure(figsize=(12,8))
    axes = fig.gca()
    axes.set_xlabel('Beta')
    axes.set_ylabel('Return')
    axes.set_title("Security Market Line")
    axes.scatter(x, y, color = 'lightblue')
    axes.plot(x, y2, color='darkslategray')
    fig.show()


def sml():
    print(Fore.WHITE+"Predicting SML model...")
    print(Fore.CYAN+"", end="")
    connection = sqlite3.connect('apollo.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM Analysis''')
    connection.commit()
    data = cursor.fetchall()
    dataset = pd.DataFrame(data, columns=["Ticker", "Name", "Market Cap", "Sector", "Industry", "EPS", "PE", "ROE", "DE", "Interest Cov.", "EV/EBITDA", "Operating Margins", "Working Capital", "Gross Margins", "Book", "Divindend Yield", "Beta", "EarningsGrowth", "Quick ratio", "RPS"])
    connection.close()
    b = dataset.copy()[["Ticker", "Beta"]]
    b = b.dropna()
    labels = b['Ticker']
    x = b['Beta']
    x = x.array.reshape(-1, 1)
    dd = yf.download(labels.tolist(),period="2y", interval="1d", auto_adjust=True)['Close']
    y = dd.pct_change(1).mean(axis = 0)
    y = y.array.reshape(-1, 1)
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    y2 =  regr.predict(x)
    smlMenu()
    option = input(Fore.WHITE+"Apollo-OS/sml $ ")
    while option != "..":
        if(option == "summary"):
            sumSML(regr.coef_, regr.intercept_, mean_squared_error(y, y2), r2_score(y, y2))
        elif(option == "chart"):
            graphSML(x, y, y2, labels)
        elif(option == "rating"):
            print(Fore.YELLOW+"This function is not available yet.")
        elif(option == "help"):
            smlMenu()
        else:
            print(Fore.RED+"Error! This is not a valid command.\n")
        option = input(Fore.WHITE+"Apollo-OS/sml $ ")        


def main():
    savedportfolio = False #Declares if a portfoloio of stocks has been saved
    sorted = False #Declares if data is sorted
    order = None # Declares order of sort
    key = None # Key of sort
    long = None # No. of chosen assets from filtered dataset
    descriptive = None
    company_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    menu()
    rules = list()
    option = input(Fore.WHITE+"Apollo-OS/home $ ")
    while option != "exit":
        if(option == "info"):
           info()
        elif(option == "stock"):
            studyStock()
        elif(option == "index"):
            custom, rules, savedportfolio, sorted, order, key, long = apollo(rules, sorted, order, key, long)
        elif(option == "analysis" and savedportfolio == True):
            historical_data, descriptive = analysis(custom.iloc[:,0].values.tolist())
        elif(option == "save" and savedportfolio == True):
            try:
                save(custom, historical_data, descriptive)
            except:
                print(Fore.RED+"Error! We were unable to perform this command. Please try again.\n")
        elif(option == "sml"):
            sml()
        elif(option == "help"):
            if (savedportfolio == True):
                menuX()
            else:
                menu()
        else:
            print(Fore.RED+"Error! This is not a valid command.\n")
        option = input(Fore.WHITE+"Apollo-OS/home $ ")
        



# The following line calls the initiation of Apollo.
main()
