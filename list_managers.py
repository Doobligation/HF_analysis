# We are going to use data from dataroma.com
import requests
import re
import csv


def get_managers_html():
    url = "https://www.dataroma.com/m/managers.php"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    page = requests.get(url, headers=headers)

    with open("managers.html", "w") as f:
        f.write(page.text)


def td_class_man():
    ls = []
    ls2 = []

    with open("managers.html", 'r') as html:
        for line in html:
            if '<td class="man">' in line:
                ls.append(line.strip())

    for comp in ls[1:]:
        match = re.search(r'm=([A-Z]+).*?>([^<]+)</a>', comp)
        if match:
            m_value = match.group(1)  # Extracts 'AKO'
            text = match.group(2)  # Extracts 'AKO Capital'
            ls2.append([m_value, text])

    with open('list_managers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(ls2)


if __name__ == "__main__":
    get_managers_html()
    td_class_man()
