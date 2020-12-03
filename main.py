import requests
import bs4
import pandas as pd

es_list_url = "https://www.letudiant.fr/palmares/liste-profils/palmares-des-ecoles-d-ingenieurs/palmares-general-des" \
              "-ecoles-d-ingenieurs/home.html#indicateurs=900659,900660,900661,900677&criterias "

es_list = requests.get(es_list_url)

soup = bs4.BeautifulSoup(es_list.text, 'html.parser')
es_row = soup.select("#main > div.l-layout > section > div > div.c-pmd-wrap > table")[0].find_all("tr")

urls = [row.find_all("a")[0].get('href') for row in es_row[2:]]

cols = ["Nom", "Description", "Public", "Filles", "Durée", "Adresse"]

rows = []
for url in urls:
    es = requests.get(url)
    es_soup = bs4.BeautifulSoup(es.text, 'html.parser')
    name = es_soup.select('#main > div.t-section-superieur > '
                          'div.c-hero.u-themed-reverse.c-hero--has-aside.c-hero--icon-right.c-hero--has-actions.t'
                          '-section-superieur > div.c-hero__etablissement > div > h1')[0].text.strip()
    # if len(es_soup.select('#jqDescContent')) == 0:
    #     description = es_soup.select('#descContent')[0].text.strip()
    # else:
    #     description = es_soup.select('#jqDescContent')[0].text.strip()
    description = ""
    pourcentage_filles = es_soup.select("#main > div.l-layout > section > div > div.c-pmd-wrap > table > tbody > "
                                        "tr:nth-child(72) > td.c-pmd-table__value > span")[0].text.strip()
    public = es_soup.select("#main > div.t-section-superieur > "
                            "div.c-hero.u-themed-reverse.c-hero--has-aside.c-hero--icon-right.c-hero--has-actions.t"
                            "-section-superieur > div.c-hero__etablissement > div > "
                            "div.c-hero__etablissement__info__tags > div:nth-child(2)")[0].text.strip()
    duree = "3 ans" if es_soup.select("#main > div.l-layout > section > div > div.c-pmd-wrap > table > tbody > "
                                      "tr:nth-child(48) > td.c-pmd-table__value > span")[0]\
        .text.strip() == "Pas de prépa intégrée" else "5 ans"

    adresse = es_soup.select('#main > div.t-section-superieur > '
                             'div.c-hero.u-themed-reverse.c-hero--has-aside.c-hero--icon-right.c-hero--has-actions.t'
                             '-section-superieur > aside > div.c-hero__aside__location > '
                             'div.c-hero__aside__location__coord > '
                             'div.c-hero__aside__location__coord__info.c-hero__aside__item')[0].text.strip()

    print(name)
    rows.append({
        cols[0]: name,
        cols[1]: description,
        cols[2]: public,
        cols[3]: pourcentage_filles,
        cols[4]: duree,
        cols[5]: adresse
    })

df = pd.DataFrame(rows)
df.to_csv('out.csv')
