from typing import Literal
from random import randint
import math
from datetime import datetime
import itertools

obecny_rok = datetime.now().year


def __liczba_dni_w_miesiacu(miesiac_: int):
    dlugosci = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return dlugosci[miesiac_]


def __peselowy_miesiac(miesiac: int, stulecie: int):
    dodatki = {
        18: 80,
        19: 0,
        20: 20,
        21: 40,
        22: 60
    }
    return miesiac + dodatki[stulecie]


ostatnia_liczba_porzadkowa = 0


def __liczba_porzadkowa():
    return ostatnia_liczba_porzadkowa + 1 % 999


def __cyfra_kontrolna(rrmmddpppp):
    cyfry = list(rrmmddpppp)
    cyfra_plci = int(cyfry[len(cyfry) - 1])
    wagi = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    pomnozone = []
    for index, cyfra in enumerate(cyfry):
        pomnozone.append(int(list(str(int(cyfra) * wagi[index])).pop()))

    suma = 0
    for cyfra in pomnozone:
        suma += cyfra

    return 10 - int(list(str(suma)).pop())


def pesel(plec: str):
    rok = randint(obecny_rok - 85, obecny_rok - 18)
    miesiac = randint(1, 12)
    dzien = randint(1, __liczba_dni_w_miesiacu(miesiac))
    stulecie = rok // 100

    cyfry_plci = []
    if plec == 'k':
        cyfry_plci = [0, 2, 4, 6, 8]
    else:
        cyfry_plci = [1, 3, 5, 7, 9]
    cyfra_plci = cyfry_plci[randint(0, 4)]

    rr = str(rok)[2:4]
    mm = str(__peselowy_miesiac(miesiac, stulecie)).rjust(2, '0')
    dd = str(dzien).rjust(2, '0')
    pppp = str(__liczba_porzadkowa()).rjust(3, '0') + str(cyfra_plci)
    rrmmddpppp = rr + mm + dd + pppp
    rrmmddppppk = rrmmddpppp + str(__cyfra_kontrolna(rrmmddpppp))
    return rrmmddppppk
