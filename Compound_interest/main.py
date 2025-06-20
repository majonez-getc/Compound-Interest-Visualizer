import matplotlib.pyplot as plt
import numpy as np

def oblicz_portfel(roczny_zwrot, wklad_miesieczny, ilosc_lat, roczne_wydatki, inflacja=0.03, miesiace_bez_wplatow=None):
    okres_miesieczny = ilosc_lat * 12
    miesieczny_zwrot = (1 + roczny_zwrot) ** (1 / 12) - 1
    miesieczna_inflacja = (1 + inflacja) ** (1 / 12) - 1

    wartosc_portfela = [0]
    wklad_wlasny = [0]
    saldo = 0
    zysk_roczny = []
    zysk_roczny_procentowy = []
    fire_miesiac = None

    docelowa_wartosc_fire = 25 * roczne_wydatki
    docelowa_wartosc_fire_realna = docelowa_wartosc_fire

    for miesiac in range(1, okres_miesieczny + 1):
        if miesiace_bez_wplatow is None or miesiac <= miesiace_bez_wplatow:
            saldo += wklad_miesieczny
        saldo *= (1 + miesieczny_zwrot)
        wartosc_portfela.append(saldo)
        wklad_wlasny.append(wklad_miesieczny * miesiac if miesiace_bez_wplatow is None or miesiac <= miesiace_bez_wplatow else wklad_wlasny[-1])

        docelowa_wartosc_fire_realna *= (1 + miesieczna_inflacja)

        if saldo >= docelowa_wartosc_fire_realna and fire_miesiac is None:
            fire_miesiac = miesiac

        if miesiac % 12 == 0:
            roczny_zysk = saldo - wklad_wlasny[miesiac]
            roczny_zysk_procentowy = (roczny_zysk / wklad_wlasny[miesiac]) * 100
            zysk_roczny.append(roczny_zysk)
            zysk_roczny_procentowy.append(roczny_zysk_procentowy)

    return wartosc_portfela, wklad_wlasny, zysk_roczny, zysk_roczny_procentowy, fire_miesiac

def format_number(number):
    return f"{number:,.2f}".replace(",", " ").replace(".", ",")

def wyswietl_wyniki(zysk_roczny, zysk_roczny_procentowy, wklad_wlasny, wartosc_portfela, fire_miesiac):
    finalna_wartosc_portfela = wartosc_portfela[-1]
    finalny_wklad_wlasny = wklad_wlasny[-1]
    finalny_zwrot = finalna_wartosc_portfela - finalny_wklad_wlasny

    print(f"{'Rok':<5}{'Wkład własny (PLN)':<25}{'Zysk roczny (PLN)':<20}{'Zwrot (%)':<15}")
    for i in range(1, len(zysk_roczny) + 1):
        print(f"{i:<5}{format_number(wklad_wlasny[i * 12]):<25}{format_number(zysk_roczny[i - 1]):<20}{zysk_roczny_procentowy[i - 1]:<15.2f}")

    print(f"\nFinalna wartość portfela: {format_number(finalna_wartosc_portfela)} PLN")
    print(f"Całkowity wkład własny: {format_number(finalny_wklad_wlasny)} PLN")
    print(f"Łączny zysk z inwestycji: {format_number(finalny_zwrot)} PLN")

    if fire_miesiac:
        rok_fire = fire_miesiac // 12
        miesiac_fire = fire_miesiac % 12
        if miesiac_fire == 0:
            miesiac_fire = 12
            rok_fire -= 1
        print(f"Możesz przejść na FIRE w miesiącu {miesiac_fire} roku {rok_fire} od dziś.")
    else:
        print("Nie osiągnięto FIRE w podanym okresie.")

def stworz_wykresy(wartosc_portfela, wklad_wlasny, zysk_roczny, finalna_wartosc_portfela, finalny_wklad_wlasny, finalny_zwrot, fire_miesiac):
    plt.figure(figsize=(8, 4))

    # Wykres 1: Wartość portfela i wkład własny
    plt.subplot(1, 2, 1)
    plt.plot(wartosc_portfela, label='Wartość portfela', color='blue')
    plt.plot(wklad_wlasny, label='Wkład własny', color='green', linestyle='--')
    plt.xlabel('Miesiące')
    plt.ylabel('Wartość w PLN')
    plt.title('Wartość portfela w czasie')
    plt.legend()
    plt.grid(True)

    # Wykres 2: Roczne zyski
    plt.subplot(1, 2, 2)
    plt.bar(range(1, len(zysk_roczny) + 1), zysk_roczny, color='purple', alpha=0.7)
    plt.xlabel('Rok')
    plt.ylabel('Zysk roczny (PLN)')
    plt.title('Roczne zyski portfela')

    plt.tight_layout(rect=(0, 0.1, 1, 1))

    # Dodanie podsumowania pod wykresami
    podsumowanie = f"Finalna wartość portfela: {format_number(finalna_wartosc_portfela)} PLN\n" \
                  f"Całkowity wkład własny: {format_number(finalny_wklad_wlasny)} PLN\n" \
                  f"Łączny zysk z inwestycji: {format_number(finalny_zwrot)} PLN\n"
    if fire_miesiac:
        rok_fire = fire_miesiac // 12
        miesiac_fire = fire_miesiac % 12
        if miesiac_fire == 0:
            miesiac_fire = 12
            rok_fire -= 1
        podsumowanie += f"Możesz przejść na FIRE po {rok_fire} latach od dziś."
    else:
        podsumowanie += "Nie osiągnięto FIRE w podanym okresie."

    plt.gcf().text(0.5, 0.02, podsumowanie, ha='center', va='bottom', fontsize=11, bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))
    plt.show()
    plt.close('all')

def main():
    roczny_zwrot = 0.10
    wklad_miesieczny = 1000
    ilosc_lat = 42
    roczne_wydatki = 72000
    inflacja = 0.03
    miesiace_bez_wplatow = 120 # Przykładowo, przestajemy wpłacać po 10 latach (120 miesiącach)
    wartosc_portfela, wklad_wlasny, zysk_roczny, zysk_roczny_procentowy, fire_miesiac = oblicz_portfel(
        roczny_zwrot, wklad_miesieczny, ilosc_lat, roczne_wydatki, inflacja, miesiace_bez_wplatow
    )

    wyswietl_wyniki(zysk_roczny, zysk_roczny_procentowy, wklad_wlasny, wartosc_portfela, fire_miesiac)
    finalna_wartosc_portfela = wartosc_portfela[-1]
    finalny_wklad_wlasny = wklad_wlasny[-1]
    finalny_zwrot = finalna_wartosc_portfela - finalny_wklad_wlasny
    stworz_wykresy(wartosc_portfela, wklad_wlasny, zysk_roczny, finalna_wartosc_portfela, finalny_wklad_wlasny, finalny_zwrot, fire_miesiac)

if __name__ == "__main__":
    main()
    
    