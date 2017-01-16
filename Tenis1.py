import csv
import os
import requests
import sys
import re

def pripravi_imenik(ime_datoteke):
    '''Ce se ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url))
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno ze od prej!')
            return
        r = requests.get(url, headers={'Accept-Language': 'en'})
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke) as datoteka:
        vsebina = datoteka.read()
    return vsebina

def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]




strani = ["1-100", "101-200", "201-300", "301-400", "401-500", "501-600", "601-700", "701-800", "801-900", "901-1000"]

for stran in strani:
    osnovni_naslov = 'http://www.atpworldtour.com/en/rankings/singles/'
    parametri = 'rankDate=2017-1-2&countryCode=all'
    naslov = '{}?{}&rankRange={}'.format(osnovni_naslov, parametri, stran)
    datoteka = 'tenis/{}.txt'.format(stran)
    shrani(naslov, datoteka)

moj_regex = r'td class="rank-cell">.*?(\d{1,4}).*?</td>.*?alt="(\w{1,3})".*?data-ga-label="(.*?)".*?<td class="age-cell".*?(\d{2}).*?player-activity.*?matchType=singles" data-ga-label="(\d{1,3})".*?'


def ustvari_slovarje (ime_datoteke,regex_izraz):
    igralci = []

    for mapa in datoteke(ime_datoteke):
        with open(mapa) as f:
            vsebina = f.read()
            for (i, j, k, l, m) in re.findall(regex_izraz, vsebina, flags=re.DOTALL):
                igralec = {"id":(int(i)), "Ranking": (int(i)), "Drzava": (j.strip()), "Ime": (k.strip()), "Starost": (int(l)),
                           "Turnirji": (int(m))}
                igralci.append(igralec)

    return igralci



def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

igralci = ustvari_slovarje("tenis", moj_regex)

zapisi_tabelo(igralci, ["id","Ranking", "Drzava", "Ime", "Starost", "Turnirji"], "igralci.csv")