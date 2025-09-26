# Robot IMU Comparison Dataset

Tento dataset obsahuje data pro porovnání trajektorie robota získané z referenčního systému (ground truth) a trajektorie naměřené pomocí senzorů IMU.

## Popis souborů

- **R1.csv** a **R6.csv**: Referenční trajektorie robota (ground truth) pro dvě různé trajektorie (R1 a R6).
- **sens1_01.csv**: Naměřené hodnoty IMU senzorem cislo 1 pro trajektorii 1.
- **sens2_06.csv**: Naměřená hodnoty IMU senzorem cislo 2 pro trajektorii 6.

## Účel

Dataset slouží k analýze přesnosti měření IMU senzorů ve srovnání s referenční trajektorií robota. Umožňuje vizualizaci a vyhodnocení odchylek mezi skutečnou a měřenou trajektorií.

## Struktura dat

Každý CSV soubor obsahuje časové řady s pozicemi (např. X, Y, případně další údaje) zaznamenanými během pohybu robota.

## Použití

Data lze využít pro:
- Porovnání přesnosti různých IMU senzorů.
- Testování algoritmů pro zpracování a korekci trajektorie.
- Vizualizaci trajektorií a analýzu chyb měření.