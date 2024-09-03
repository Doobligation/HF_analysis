import os
import requests
import pandas as pd
import yfinance as yf


def get_each_company():
    with open("list_managers.csv", "r") as r:
        # TODO: Change the [1] to a for loop to access all companies
        company = r.readlines()[1].split(",")[0]
        url = f"https://www.dataroma.com/m/hist/p_hist.php?f={company}"

    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }

    page = requests.get(url, headers=headers)

    os.makedirs("companies", exist_ok=True)
    os.chdir("companies")

    with open(f"{company}.html", "w") as f:
        f.write(page.text)


def contextualize():
    os.chdir("companies")
    # TODO: Change the company
    table = pd.read_html("AIM.html")[0]

    for i in range(len(table.values)):
        # print(table.values[i][0], table.values[i][1])
        quarter = table.values[i][0].replace("&nbsp", "")  # .replace(" ", " ")
        budget = table.values[i][1]
        # TODO: $ conversion
        change_in_quarter = (table.values[i][1] - table.values[i + 1][1]) / table.values[i + 1][1]
        print(change_in_quarter)

    yf.ticker("SPY")

# def compare_vs_sp500():
#     # TODO
#     print("kongs")


# get_each_company()
contextualize()
