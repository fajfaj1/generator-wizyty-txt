from pesel import pesel, __liczba_dni_w_miesiacu
from szczepionki import szczepionki
from random import randint, shuffle
import json

pacjenci_z_min_jedna_dawka_sz12_3d = {
    'm': 17,
    'k': 7
}


def losowa_data(miesiace: [int]):
    miesiac = miesiace[randint(0, len(miesiace) - 1)]
    mm = str(miesiac).rjust(2, '0')
    dd = str(randint(1, __liczba_dni_w_miesiacu(miesiac))).rjust(2, '0')
    return f"2023-{mm}-{dd}"


def liczba_dawek_z_kodu(k_szczepionki):
    return int(k_szczepionki[len(k_szczepionki) - 2])


def losowa_plec():
    return ['k', 'm'][randint(0, 1)]


# [pesel, kod_szczepionki, data_szczepienia, numer_dawki]
wizyty = []

a = 0
b = 0
# 8.2
# This motherfucker ensures the total number of doses applied of sz12_3d will be 60 (17x2 + 6x1 + 7x2 + 6x1)
liczba_dawek_sz12_3d = 3
for plec in pacjenci_z_min_jedna_dawka_sz12_3d:
    liczba_pacjentow = pacjenci_z_min_jedna_dawka_sz12_3d[plec]
    print(liczba_pacjentow, liczba_pacjentow * 2)
    for numer_pacjenta in range(0, liczba_pacjentow):
        pesel_pacjenta = pesel(plec)
        for dawka in [0, 1]:
            wizyty.append([pesel_pacjenta, 'sz12_3d', losowa_data([1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]), str(dawka)])
            a += 1
        if numer_pacjenta < 6:
            wizyty.append([pesel_pacjenta, 'sz12_3d', losowa_data([1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]), str(3)])
            b += 1

print(f"{a} + {b}")
szczepionki['sz12_3d'] -= 60

# 8.3
pesele_konczacych_wsyzstkie_dawki_w_maju2023 = list(map(lambda x: pesel(losowa_plec()), [None] * 48))
for pesel_pacjenta in pesele_konczacych_wsyzstkie_dawki_w_maju2023:
    for szczepionka in szczepionki.copy():
        if szczepionki[szczepionka] <= 0:
            del szczepionki[szczepionka]
    kod_szczepionki = list(szczepionki.keys())[randint(0, len(szczepionki) - 1)]
    liczba_dawek = liczba_dawek_z_kodu(kod_szczepionki)
    for dawka in range(1, liczba_dawek):
        wizyty.append([pesel_pacjenta, kod_szczepionki, losowa_data([5]), str(dawka)])
        szczepionki[kod_szczepionki] -= 1
    wizyty.append([pesel_pacjenta, kod_szczepionki, losowa_data([5]), str(liczba_dawek)])
    szczepionki[kod_szczepionki] -= 1

# 8.1
for szczepionka in szczepionki:

    liczba_dawek = liczba_dawek_z_kodu(szczepionka)
    pozostala_liczba_szczepien = szczepionki[szczepionka]
    while pozostala_liczba_szczepien > 0:

        pesel_pacjenta = pesel(losowa_plec())
        for dawka in range(1, randint(1, liczba_dawek + 1)):

            if pozostala_liczba_szczepien > 0:
                wizyty.append(
                    [pesel_pacjenta, szczepionka, losowa_data([1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]), str(dawka)])
                szczepionki[szczepionka] -= 1
                pozostala_liczba_szczepien -= 1

with open('wizyty.txt', 'w') as f:
    shuffle(wizyty)
    f.write(
        "	".join(['Pesel', 'kod_szczepionki', 'data_szczepienia', 'dawka']) + "\n" +
        "\n".join(
            list(map("	".join, wizyty))
        )
    )
