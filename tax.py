# NO TAX, LEGAL OR FINANCIAL ADVICE

import os
from pathlib import Path

import pandas as pd
import yfinance as yf
from dotenv import load_dotenv

pd.options.mode.copy_on_write = True

# load environment variables from .env file
# make sure to set the PATH_TO_FILE environment variable in .env file
load_dotenv()
file_path = os.getenv("PATH_TO_FILE")
if file_path is None:
    raise ValueError("Please set the PATH_TO_FILE environment variable.")

# load the local XML file
path_to_file = Path(file_path)

print(path_to_file)

df_trades = pd.read_xml(path_to_file, xpath=".//Trade")
df_divi = pd.read_xml(path_to_file, xpath=".//CashTransaction")

# filter df for realized trades and calculate PnL in EUR
filtered_df_trades = df_trades[(df_trades["fifoPnlRealized"] != 0)]
filtered_df_trades["FifoPnlRealizedEUR"] = (
    filtered_df_trades["fifoPnlRealized"] * filtered_df_trades["fxRateToBase"]
).round(2)

### Stocks, Futures and Options
# Insert assets here
derivates = ["FOP", "OPT", "FUT"]
stocks = ["STK"]

# sum per asset
sum_derivates = (
    filtered_df_trades[filtered_df_trades["assetCategory"].isin(derivates)][
        "FifoPnlRealizedEUR"
    ]
    .sum()
    .round(2)
)
sum_stocks = (
    filtered_df_trades[filtered_df_trades["assetCategory"].isin(stocks)][
        "FifoPnlRealizedEUR"
    ]
    .sum()
    .round(2)
)

# results for Anlage KAP
print("***")
print("Gewinne und Verluste für Aktien und Derivate")
print("***")
if sum_derivates > 0:
    print(
        f"KAP Zeile 21 Gewinne aus Stillhalterprämien und Gewinne aus Termingeschäften: {sum_derivates} EUR"
    )
elif sum_derivates < 0:
    print(f"KAP Zeile 24 Verlust aus Termingeschäften: {sum_derivates} EUR")
elif sum_derivates == 0:
    print(f"KAP Zeile 21 und Zeile 24: {sum_derivates} EUR")

if sum_stocks > 0:
    print(f"KAP Zeile 20 Gewinne aus Aktienverkäufen: {sum_stocks} EUR")
elif sum_stocks < 0:
    print(f"KAP Zeile 23 Verluste aus Aktienverkäufen: {sum_stocks} EUR")
elif sum_stocks == 0:
    print(f"KAP Zeile 20 und Zeile 23: {sum_stocks} EUR")

### Dividends
# Replace Payment In Lieu Of Dividends with Dividends for easier grouping
df_divi["type"] = df_divi["type"].replace("Payment In Lieu Of Dividends", "Dividends")
# calculate PnL in EUR
df_divi["FifoPnlRealizedEUR"] = (df_divi["amount"] * df_divi["fxRateToBase"]).round(2)
grouped_df_divi = (
    df_divi.groupby(["subCategory", "type"], dropna=False)["FifoPnlRealizedEUR"]
    .sum()
    .reset_index()
)

# results for Anlage KAP und KAP-INV
print("***")
print("Gewinne und Verluste für Dividenden und Zinsen")
print("***")
for idx, row in grouped_df_divi.iterrows():
    sub = row["subCategory"]
    typ = row["type"]
    val = row["FifoPnlRealizedEUR"]
    if pd.isna(sub) and typ == "Broker Interest Received":
        print(f"KAP Zeile 18 Inländische Kapitelerträge: {val}")
    elif sub == "COMMON" and typ == "Dividends":
        print(f"KAP Zeile 19 Ausländische Kapitalerträge: {val} EUR")
    elif sub == "COMMON" and typ == "Withholding Tax":
        print(f"KAP Zeile 41 Noch anzurechnende ausländische Steuer: {abs(val)} EUR")
    elif sub == "ETF" and typ == "Dividends":
        print(f"KAP-INV Zeile 8 Ausschüttung aus sonstigen Investmentfonds: {val} EUR")
    elif sub == "ETF" and typ == "Withholding Tax":
        print(f"KAP-INV Noch anzurechnende ausländische Steuer: {abs(val)}")
print("***")

### ETFs and Funds
# filter df for realized trades and calculate PnL in EUR
filtered_df_etf = df_trades[(df_trades["subCategory"] == "ETF")]
filtered_df_etf["FifoPnlRealizedEUR"] = (
    filtered_df_etf["fifoPnlRealized"] * filtered_df_etf["fxRateToBase"]
).round(2)
grouped_df_etf = (
    filtered_df_etf.groupby(["assetCategory", "subCategory", "symbol"])[
        "FifoPnlRealizedEUR"
    ]
    .sum()
    .reset_index()
)

# add new column for asset_classes
grouped_df_etf["asset_classes"] = None

for idx, row in grouped_df_etf.iterrows():
    ticker = row["symbol"]
    # search for yahoo finance ticker
    search = yf.Search(ticker, max_results=1).quotes
    if search:
        symbol = search[0]["symbol"]
        # create yfinance object
        t = yf.Ticker(symbol).funds_data
        # get asset classses and insert in df
        try:
            grouped_df_etf.at[idx, "asset_classes"] = t.asset_classes
        except Exception:
            grouped_df_etf.at[idx, "asset_classes"] = None
    else:
        grouped_df_etf.at[idx, "asset_classes"] = None

# add exploded asset_classes to df and drop asset_classes
grouped_df_etf_expanded = grouped_df_etf["asset_classes"].apply(pd.Series)
df_etf = pd.concat([grouped_df_etf, grouped_df_etf_expanded], axis=1)
df_etf = df_etf.drop(columns=["asset_classes"])

# results for ETFs and other funds
print("Gewinne und Verluste für ETFs und Funds")
print("***")
for idx, row in df_etf.iterrows():
    stock = row["stockPosition"]
    symbol = row["symbol"]
    val = row["FifoPnlRealizedEUR"]
    if stock > 50:
        print(f"({symbol}) KAP-INV Aktienfonds (30% Teilfreistellung): {val} EUR")
    elif stock <= 50 and stock >= 25:
        print(f"({symbol}) KAP-INV Mischfonds (15% Teilfreistellung): {val} EUR")
    elif stock < 25:
        print(f"({symbol}) KAP-INV Sonstige Fonds (0% Teilfreistellung): {val} EUR")
print("***")
