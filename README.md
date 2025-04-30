# IBKR German Tax Helper
The German Informational Tax Report from Interactive Brokers is often incorrect and is delivered very late (July and later). This rudimentary script can be used to calculate the figures for the tax return independently and earlier. The figures shown here correspond most closely to the Activity Report from Interactive Brokers. If the tax office asks for proof of capital gains or losses, the Activity Report should be submitted and not the German Informational Tax Report.

# Disclaimer
No tax, investment or legal advice.
No guarantee for the correctness of the figures.
Consult a tax advisor if necessary.

# Requirements
- Python >= 3.12   
- pandas==2.2.3   
- yfinance==0.2.56

Older versions should work aswell.

# Setup
Create an Interactive Brokers Flex Report and select the following features.

Cash Transactions:

![ib_flex_cash_75](https://github.com/user-attachments/assets/ed709c96-8fa2-4d4a-ac8c-b39092e490f0)


Trades:

![ib_flex_trades_75](https://github.com/user-attachments/assets/0f8fa027-df81-4d53-a320-85ee7cd5c095)

More characteristics can also be selected, but this makes the file easy to read by humans.

Run the created Flex Query and select XML as format and a user-defined date range. Select the year for which the figures are to be determined, e.g. 01.01.2024 - 31.12.2024.
Currently, last year cannot be selected for the Flex Query period, so a query via API is not possible.

Insert the file path in line 19 in the script and execute it.

# Notes
- The number for line 19 must be totaled manually.
- CFDs are currently not evaluated.
- Gains or losses from shares bought or sold via executed options may not be calculated correctly. The costs for the options can be taken into account as the purchase price for the shares.
- The lines in KAP-INV for sold ETFs are not displayed. Each ETF must be checked individually here.
- Vorabpauschale is not calculated.

# Feedback
If I have forgotten assets or specific trades or if there are better ways to get the numbers, I am happy to receive feedback.
