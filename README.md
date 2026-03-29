# Vlastní Handheld herní konzole 

![Fotka dokončené konzole](docs/IMG_20260318_023212.jpg)

## O projektu
Tento repozitář obsahuje seznam všech součástek, 3D modely a zdrojové kódy pro vlastnoručně postavenou přenosnou herní konzoli poháněnou počítačem **Raspberry Pi 5**.

### Technické úkoly, které jsem na projektu řešil:
* Návrh a 3D tisk vlastní krabičky pro konzoli.
* Propojení **Raspberry Pi 5** s 5" kapacitním dotykovým displejem a 15 fyzickými mikrospínači přes GPIO rozhraní.
* Návrh napájení pomocí 3,7V 8000mAh Li-Pol baterie.
* Zapojení audia (8Ω 2W reproduktor Waveshare) a řešení odvodu tepla (52Pi aktivní chladič).
* Vývoj hlavní softwarové logiky a ovládání v **Pythonu**.

## Struktura repozitáře

### Hardware
Fyzické komponenty a návrh zapojení najdete ve složce `/hardware/`:
* `Seznam součástek.csv` a `Seznam součástek.xlsx` - Kompletní seznam součástek + kde je koupit/sehnat

### 3D Modely
Soubory pro výrobu krabičky najdete ve složce `/3d-modely/`:
* `Dolní část krabičky.stl` a `Horní část krabičky.stl` - Modely připravené pro 3D tisk.

### Software (Zdrojové kódy)
* `/src/` - Zde se nachází zdrojový kód, který spravuje veškerou logiku ovladače

### Docs (Dokumentace)
* Ukazuje postupný vývoj herní konzole

## Použité technologie
* **Hardware:** Raspberry Pi 5 (Single Board Computer), GPIO rozhraní, Pájení elektroniky
* **Software:** Python, OS Linux (Raspberry Pi OS)
* **Konstrukce:** 3D modelování, 3D tisk

---
*Vytvořil Ondřej Kučera (2025/2026) - Student IT na SPŠE Ječná*
