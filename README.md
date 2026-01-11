# Library Manager Project

**Autor:** Tobiáš Gruber  
**Škola:** SPŠE Ječná  
**Datum:** 2026  
**Typ:** Školní projekt (D1 - Repository Pattern)

## Popis
Aplikace pro správu knihovny. Umožňuje evidovat knihy, autory, členy a realizovat výpůjčky.

## Instalace a Spuštění
1. **Databáze:**
   - Nainstalujte MySQL/MariaDB.
   - Spusťte skript `data/database_schema.sql` (vytvoří databázi `library_db`).
   - Vytvořte uživatele nebo upravte konfiguraci.

2. **Konfigurace:**
   - Otevřete `config/settings.json`.
   - Nastavte `user` a `password` k vaší databázi.

3. **Python:**
   - Nainstalujte závislosti: `pip install -r requirements.txt`.
   - Spusťte aplikaci: `python src/main.py`.

## Funkce
- Evidence knih (Repository Pattern).
- Transakční zpracování výpůjček (Loan Service).
- Import dat z CSV.
- Statistický report.