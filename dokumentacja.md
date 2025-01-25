# Dokumentacja projektu - Weather API Service

### link do strony: https://proud-water-05321801e.5.azurestaticapps.net/

## 1. Opis projektu

Aplikacja serwerowa zbudowana w FastAPI, służąca do pobierania danych pogodowych oraz szacowania produkcji energii z instalacji fotowoltaicznych. Frontend został zbudowany za pomocą NEXT.js + TypeScript

## 2. Architektura

```
projekt/
├── app.py                  # Główna aplikacja FastAPI
├── weatherClass.py         # Klasa serwisu pogodowego
├── weeklySummaryClass.py   # Klasa podsumowań tygodniowych
├── requirements.txt        # Zależności projektu
└── Procfile               # Konfiguracja wdrożenia
```

## 3. Zastosowane technologie

- FastAPI - nowoczesny framework asynchroniczny
- Uvicorn - serwer ASGI
- Requests - klient HTTP
- Azure App Service - platforma hostingowa

## 4. Endpointy API

### GET /forecast

Zwraca prognozę pogody i szacowaną produkcję energii.

**Parametry:**

- lat: float (szerokość geograficzna)
- lon: float (długość geograficzna)

**Odpowiedź:**

```json
{
	"date": "2024-01-25T00:00:00.000Z",
	"weatherCode": 3,
	"temperature2mMax": 5.55,
	"temperature2mMin": -0.25,
	"estimatedEnergy": 4.3
}
```

### GET /weekly_summary

Zwraca tygodniowe podsumowanie pogody.

**Parametry:**

- lat: float (szerokość geograficzna)
- lon: float (długość geograficzna)

**Odpowiedź:**

```json
{
	"averagePressure": 1013.25,
	"averageSunshineDuration": 28800,
	"maxTemperature": 25.5,
	"minTemperature": 15.5,
	"precipitationDays": 2,
	"weatherSummary": "bez opadów",
	"windAverage": 12.3
}
```

## 5. Instalacja i uruchomienie

```bash
# Instalacja zależności
pip install -r requirements.txt

# Uruchomienie lokalne
uvicorn app:app --reload

# Uruchomienie produkcyjne
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 2
```

## 6. Wdrożenie

Aplikacja została wdrożona na Azure App Service z użyciem:

- Plan B1
- Python 3.10
- 2 workerów Uvicorn
- Automatycznego skalowania

## 7. Zaawansowane koncepty Pythona użyte w projekcie

- Programowanie asynchroniczne (async/await)
- Programowanie obiektowe (klasy, dziedziczenie)
- Type hints i walidacja typów
- Integracja z zewnętrznym API
- Obsługa błędów i wyjątków
- Deployment na platformie chmurowej
