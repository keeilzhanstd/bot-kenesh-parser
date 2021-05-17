import bs4 as bs
import urllib.request
import pandas as pd
import sys
import os


class Parlament:
    def __init__(self, deputies):
        self.deputies = deputies

        # DFrames
        self.ids = []
        self.names = []
        self.fractions = []
        self.deputyLinks = []
        self.fractionLinks = []

        for deputy in deputies:
            self.ids.append(deputy.id)
            self.names.append(deputy.name)
            self.fractions.append(deputy.fraction)
            self.deputyLinks.append(deputy.deputyLink)
            self.fractionLinks.append(deputy.fractionLink)

    def writeToExcel(self):
        deputiesDataFrame = pd.DataFrame(
            {'Идентификационный номер': self.ids,
             'ФИО Депутата': self.names,
             'Фракция': self.fractions,
             'Ссылка на страницу депутата': self.deputyLinks,
             'Ссылка на страницу фракции': self.fractionLinks})
        writer = pd.ExcelWriter('deputies.xlsx', engine='xlsxwriter')
        deputiesDataFrame.to_excel(writer, sheet_name='Депутаты', index=False)
        writer.save()

    def writeToCsv(self):
        deputiesDataFrame = pd.DataFrame(
            {'Идентификационный номер': self.ids,
             'ФИО Депутата': self.names,
             'Фракция': self.fractions,
             'Ссылка на страницу депутата': self.deputyLinks,
             'Ссылка на страницу фракции': self.fractionLinks})
        csvFileContents = deputiesDataFrame.to_csv(index=False)
        with open("deputies.csv", "w", encoding='utf-8') as f:
            f.write(csvFileContents)


class Deputy:
    def __init__(self, id, name, fraction, deputyLink, fractionLink):
        self.id = id
        self.name = name
        self.fraction = fraction
        self.deputyLink = deputyLink
        self.fractionLink = fractionLink

    def getProps(self):
        return [self.id, self.name, self.fraction, self.deputyLink, self.fractionLink]


def fetchDeputies():
    print("Deputies fetching...")
    url = "http://kenesh.kg/ru/deputy/list/35"
    source = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(source, 'html.parser')

    deputyTable = soup.find("table", attrs={"class": "table"})
    deputyTableRows = deputyTable.tbody.find_all("tr")

    deputies = []
    for tr in deputyTableRows:
        deputyProps = []
        trContents = tr.find_all("td")

        for td in trContents:
            deputyProps.append(td.text.replace('\n', ' ').strip())
        deputyProps.append('http://kenesh.kg' + trContents[1].a['href'])
        deputyProps.append('http://kenesh.kg' + trContents[2].a['href'])
        deputies.append(
            Deputy(deputyProps[0], deputyProps[1], deputyProps[2], deputyProps[3], deputyProps[4]))
    print("Deputies finished fetching. Data saved.")
    return deputies


parlament = Parlament(fetchDeputies())


def main():
    while True:
        userChoice = int(input(
            "How do you wish to save file?\n 1. Excel \n 2. CSV \n\n 0. Exit \nChoose: 1/2/0 => "))

        if userChoice == 1:
            parlament.writeToExcel()
            print("Saved in deputies.xlsx under the current directory: " + os.getcwd())
            break
        elif userChoice == 2:
            parlament.writeToCsv()
            print("Saved in deputies.csv under the current directory: " + os.getcwd())
            break
        elif userChoice == 0:
            break


if __name__ == '__main__':
    main()
