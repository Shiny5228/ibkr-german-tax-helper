# IBKR German Tax Helper

The **IBKR German Tax Helper** is a Python script designed to assist in calculating figures for the German tax return based on Interactive Brokers' Activity Report. The German Informational Tax Report from Interactive Brokers is often delayed and may contain inaccuracies. This script provides a way to independently calculate the required figures earlier and more reliably.

## Disclaimer

- **No tax, investment, or legal advice is provided.**
- **No guarantee for the correctness of the figures.**
- Consult a tax advisor if necessary.

## Features

- Processes Interactive Brokers' Flex Report in XML format.
- Calculates realized profits and losses for stocks, derivatives, and ETFs.
- Handles dividends and withholding taxes.
- Outputs results in a format suitable for German tax forms (e.g., Anlage KAP and KAP-INV).
- Sses yfinance to categorize ETFs based on their holdings for Teilfreistellung.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shiny5228/ibkr-german-tax-helper.git
   cd ibkr-german-tax-helper
   ```

2. Install dependencies using `pyproject.toml`:
   ```bash
   uv sync
   ```

## Setup
### Create an Interactive Brokers Flex Report and select the following features.
Cash Transactions:

![ib_flex_cash_75](https://github.com/user-attachments/assets/ed709c96-8fa2-4d4a-ac8c-b39092e490f0)


Trades:

![ib_flex_trades_75](https://github.com/user-attachments/assets/0f8fa027-df81-4d53-a320-85ee7cd5c095)

The selected characteristics is more then needed for the script to work, but this makes the file easy to read by humans.

Run the created Flex Query and select XML as format and a user-defined date range. Select the year for which the figures are to be determined, e.g. 01.01.2024 - 31.12.2024.
Currently last year cannot be selected for the Flex Query period, so a query via API is not possible.

### Configure the `.env` file:
- Copy the `.env_sample` file to `.env`.
- Set the `PATH_TO_FILE` variable to the path of the generated XML file.


## Notes
- The script currently groups all (sub-)accounts together. If results are needed for individual accounts, additional filtering must be implemented.
- Certain calculations, such as Vorabpauschale, are not included.
- Gains or losses from shares bought or sold via executed options may not be calculated correctly.
- CFDs are not evaluated.
- For ETFs, the script attempts to classify asset classes using Yahoo Finance. Ensure the ticker symbols are valid.

## Output
The script outputs the following results:
1. Stocks and Derivatives:
    * Gains and losses for stocks and derivatives are displayed in the format required for Anlage KAP.
2. Dividends and Withholding Taxes:
    * Dividends and withholding taxes are grouped and displayed for Anlage KAP and KAP-INV.
3. ETFs and Funds:
    * Realized profits and losses for ETFs are classified based on asset classes (e.g., equity funds, mixed funds).

## Feedback
If you encounter issues, have suggestions for improvement, or notice missing features, feel free to provide feedback.

## License
This project is licensed under the MIT License.
