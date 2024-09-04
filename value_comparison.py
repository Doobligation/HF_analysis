import csv
import os
import requests
import pandas as pd
import yfinance as yf
from tqdm import tqdm
from time import sleep

START_DATE = "2006-01-01"
END_DATE = "2024-09-01"


def calculate_change_percentage(start_price, end_price):
    return (end_price - start_price) / start_price * 100


"""Fetching the data from dataroma.com of the superinvestors who are listed there"""
def get_each_company():
    """Make a directory called companies to store all the names of the companies"""
    os.makedirs("companies", exist_ok=True)

    with open("list_managers.csv", "r") as r:
        for company in tqdm(r, desc="Downloading"):
            url = f"https://www.dataroma.com/m/hist/p_hist.php?f={company.split(",")[0]}"

            headers = {
                "User-Agent":
                    "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
            }

            page = requests.get(url, headers=headers)

            with open(os.path.join("companies", f"{company.split(',')[0]}.html"), "w", encoding="utf-8") as f:
                f.write(page.text)
                sleep(2)


"""
Getting the S&P 500 data using YahooFinance API.
You can adjust the START DATE and the END_DATE from the beginning of this script.
"""
def get_SPY():
    yf.download("SPY", start=START_DATE, end=END_DATE, rounding=False).to_csv("sp500_df.csv")
    sp500_raw = pd.read_csv("sp500_df.csv", index_col="Date", parse_dates=True)

    # Filling in the missing dates such as Saturdays and Sundays.
    start_date = str(sp500_raw.index[0])
    end_date = str(sp500_raw.index[-1])
    idx = pd.date_range(start_date, end_date)
    sp500_raw = sp500_raw.reindex(idx)
    sp500_raw.ffill(inplace=True)

    sp500_raw.to_csv("sp500_df.csv", index_label="Date")


def contextualize():
    reader = pd.read_csv("sp500_df.csv")

    # Convert the list of lists into a dictionary for better accesses to dates.
    sp500_temp = reader.values.tolist()

    # Using Adjusted Close Price
    sp500_db = {row[0]: row[5] for row in sp500_temp}

    # Put all the companies in a list
    companies = []
    final = []

    with open("list_managers.csv", "r") as r:
        for company in r:
            companies.append(company.split(",")[0])


    os.chdir("companies")
    for comp in companies:
        table = pd.read_html(f"{comp}.html")[0]

        qAndBudget = []
        outperformace = []

        for company in range(len(table.values)):
            quarter = table.values[company][0].replace("&nbsp", "").replace("  ", "").replace("Q1",
                                    "-03-30").replace("Q2", "-06-30").replace("Q3", "-09-30").replace("Q4", "-12-31")
            budget = int(table.values[company][1].strip("$").replace(" M", "000000").replace(".", "").replace(" B", "0000000"))
            qAndBudget.append([quarter, budget])

        for company in range(len(qAndBudget) - 1):
            company_dif = calculate_change_percentage(qAndBudget[company + 1][1], qAndBudget[company][1])
            sp500_start_price = sp500_db[qAndBudget[company][0]]
            sp500_end_price = sp500_db[qAndBudget[company + 1][0]]
            sp500_dif = calculate_change_percentage(sp500_end_price, sp500_start_price)

            qAndBudget[company].append(company_dif)
            qAndBudget[company].append(sp500_dif)

            if company_dif > sp500_dif:
                outperformace.append(1)
            else:
                outperformace.append(0)

        final.append([comp, (sum(outperformace) / len(outperformace))])

    os.chdir("..")
    with open('evaluation.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(final)


if __name__ == "__main__":
    get_each_company()
    get_SPY()
    contextualize()
