# Dokumentace projektu: Library Manager

**Název projektu:** Library Manager (Správa knihovny)
**Autor:** Tobiáš Gruber
**Kontakt:** gruber2@spsejecna.cz
**Škola:** SPŠE Ječná
**Datum vypracování:** Leden 2026
**Typ:** Školní projekt (Varianta D1 - Repository Pattern)

---

## 1. Závěrečné resumé projektu
Cílem projektu bylo vytvořit konzolovou aplikaci v jazyce Python pro správu knižního fondu a výpůjček. Aplikace demonstruje využití relační databáze MySQL, transakčního zpracování dat a návrhového vzoru Repository. Projekt splňuje všechny zadané požadavky včetně importu dat, generování reportů a oddělení vrstev aplikace. Aplikace je plně funkční a připravena k nasazení na školní PC.

---

## 2. Specifikace požadavků a Use Case
Aplikace je navržena pro knihovníka, který potřebuje efektivně spravovat fond.

**Hlavní případy užití (Use Cases):**
1.  **Správa knih:** Uživatel může zobrazit seznam knih, přidat novou knihu a smazat existující knihu.
2.  **Výpůjčky (Transakce):** Uživatel může realizovat výpůjčku knihy členem. Tento proces probíhá v transakci (zápis do tabulky výpůjček + aktualizace aktivity člena).
3.  **Import dat:** Uživatel může hromadně nahrát knihy a vydavatele z CSV souboru.
4.  **Reporting:** Uživatel může generovat statistický přehled o nejaktivnějších členech a hodnotě půjčených knih.

---

## 3. Architektura aplikace
Projekt využívá vrstvenou architekturu s oddělením logiky a datového přístupu.

### Použité návrhové vzory
* **Repository Pattern (D1):** Třída `BookRepository` zapouzdřuje veškerou logiku pro přístup k tabulce knih. Zbytek aplikace neobsahuje přímé SQL dotazy na knihy.
* **Service Layer:** Třídy `LoanService`, `ImportService` a `ReportingService` obsahují byznys logiku (transakce, validace, agregace).
* **Singleton:** Třída `DatabaseConnection` zajišťuje jediné, sdílené připojení k databázi.

### Struktura projektu
* `/src`: Zdrojové kódy aplikace (moduly, služby, repozitáře).
* `/data`: SQL skripty pro databázi a CSV soubory pro import.
* `/config`: Konfigurační soubory.
* `/tests` / `/doc`: Dokumentace a testovací scénáře.

---

## 4. Databázový model (E-R Model)
Aplikace využívá relační databázi MySQL. Export databáze je umístěn v souboru `data/database_schema.sql` a obsahuje DDL i DML příkazy.

**Tabulky a atributy:**
* **authors:** `author_id` (PK), `first_name`, `last_name`, `birth_date` (Date).
* **publishers:** `publisher_id` (PK), `name` (String), `website`.
* **books:** `book_id` (PK), `title` (String), `isbn` (Unique), `price` (Float), `is_active` (Bool), `publisher_id` (FK).
* **members:** `member_id` (PK), `full_name`, `email`, `membership_type` (Enum: BASIC/PREMIUM/STUDENT), `joined_at` (Datetime).
* **loans:** `loan_id` (PK), `member_id` (FK), `book_id` (FK), `loan_date`, `status`.
* **book_authors:** Vazební tabulka (M:N) pro propojení knih a autorů.

---

## 5. Schéma importovaných souborů
Aplikace podporuje import knih z formátu CSV. Import automaticky plní dvě tabulky (`publishers` a `books`).

**Soubor:** `/data/import_books.csv`
**Formát:** Textový soubor oddělený čárkami, kódování UTF-8.
**Povinná hlavička a struktura:**
`publisher_name,book_title,isbn,price`

**Popis položek:**
* `publisher_name`: Název vydavatele (String)
* `book_title`: Název knihy (String)
* `isbn`: Unikátní identifikátor (String)
* `price`: Cena (Float)

---

## 6. Konfigurace
Nastavení aplikace je uloženo v souboru `config/settings.json`.

**Přípustné volby:**
```json
{
    "database": {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "library_db"
    },
    "app": {
        "name": "Library Manager v1.0",
        "currency": "CZK"
    }
}