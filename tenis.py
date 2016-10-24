import csv
import os
#import requests
import sys
import re

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
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
    with open(ime_datoteke) as datoteka:
        vsebina = datoteka.read()

def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]




strani = ["1-100", "101-200", "201-300", "301-400", "401-500", "501-600", "601-700", "701-800", "801-900", "901-1000"]

#for stran in strani:
    #osnovni_naslov = 'http://www.atpworldtour.com/en/rankings/singles/'
    #parametri = 'rankDate=2016-10-17&countryCode=all'
    #naslov = '{}?{}&rankRange={}'.format(osnovni_naslov, parametri, stran)
    #datoteka = 'tenis/{}.txt'.format(stran)
    #shrani(naslov, datoteka)


for mapa in datoteke("tekstovne datoteke"):
    with open(mapa) as f:
        vsebina = f.read()
        for (i,j,k,l) in re.findall(r'<td class="rank-cell">.*?(\d{1,4}).*?</td>.*?alt="(\w{1,3})".*?data-ga-label="(.*?)".*?<td class="age-cell".*?(\d{2})', vsebina, flags=re.DOTALL):
            print((i,j,k,l))



