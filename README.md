# 📊 Statly

**Statly** è un'applicazione web interattiva per l'analisi statistica di file Excel. Progettata per essere semplice, veloce ed efficace, consente di caricare dataset Excel, generare analisi statistiche descrittive e visualizzare grafici dinamici. L'output può essere comodamente scaricato come file PDF, pronto per essere condiviso o archiviato.

## 🚀 Caratteristiche principali

- ✅ Upload di file Excel (.xlsx, .xls) - Progressi in palestra, misurazioni, dati tabellari
- ✅ Analisi statistiche descrittive automatiche (media, massimo, minimi, andamento nel tempo)
- ✅ Generazione di grafici dinamici (istogrammi, box plot, correlazioni, time series)
- ✅ Esportazione completa in PDF professionale
- ✅ Nessuna autenticazione necessaria: utilizzo immediato
- ✅ Interfaccia web moderna e responsive


---

## 🏗️ Architettura del Progetto

Il progetto è organizzato in due componenti principali:

```
statly/
│
├── backend/                  # Backend API in FastAPI
│   ├── main.py               # Endpoints principali
│   ├── analysis.py           # Funzioni per analisi statistiche
│   ├── pdf_generator.py      # Creazione del PDF con risultati e grafici
│   └── requirements.txt      # Dipendenze Python
│
├── frontend/                 # Interfaccia utente web
│   ├── index.html            # Pagina principale
│   ├── styles.css            # Stili base
│   └── script.js             # Script JS per upload e visualizzazione
│
├── Dockerfile                # Definizione dell'immagine backend
├── docker-compose.yml        # Composizione dei container per sviluppo
└── README.md                 # Documentazione del progetto
```

---

## ⚙️ Tecnologie Utilizzate

| Componente   | Tecnologia            |
|--------------|------------------------|
| Backend      | Python 3.11+, FastAPI |
| Analisi dati | pandas, matplotlib, seaborn |
| PDF export   | ReportLab, matplotlib  |
| Frontend     | HTML5, CSS3, JavaScript |
| File support | Excel (.xlsx, .xls) via openpyxl |
| Contenitori  | Docker, Docker Compose |

---

## 📦 Setup locale

> **Requisiti:** Python 3.11+ installato nel sistema.

### 🔧 Avvio in locale senza Docker

```bash
cd backend
python -m venv venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Il frontend sarà automaticamente servito su [http://localhost:8000](http://localhost:8000)

**Dipendenze principali:**
- `fastapi` - Framework web moderno per API
- `pandas` - Manipolazione e analisi dati
- `matplotlib` + `seaborn` - Generazione grafici
- `openpyxl` - Lettura file Excel
- `reportlab` - Generazione PDF professionale

### 🐳 Avvio tramite Docker

```bash
docker-compose up --build
```

Una volta in esecuzione, visita [http://localhost:8000](http://localhost:8000) per accedere all'interfaccia web completa.

---

## 📂 Esempio d'Uso

1. Carica un file Excel `.xlsx` o `.xls` con dati tabellari.
2. L'app effettua analisi statistiche automatiche sul dataset.
3. Viene generato un report completo contenente:
   - Statistiche descrittive (media, mediana, deviazione standard)
   - Grafici di distribuzione (istogrammi, box plot)
   - Matrice di correlazione tra variabili numeriche
   - Grafici temporali (se presenti colonne data/tempo)
   - Analisi categoriche (frequenze, distribuzioni)
4. Il PDF professionale è scaricabile direttamente dal browser.

---

## 📄 Esempio di Dataset Supportato

Crea un file Excel con colonne come:

**Dati Palestra:**
```
Data       | Esercizio | Peso | Ripetizioni
2025-06-01 | Panca     | 60   | 10
2025-06-08 | Panca     | 62.5 | 8
2025-06-15 | Panca     | 65   | 8
2025-06-22 | Squat     | 80   | 10
```

**Dati Business:**
```
Data       | Vendite | Regione | Prodotto
2025-01-01 | 1500    | Nord    | Laptop
2025-01-02 | 2300    | Sud     | Desktop
2025-01-03 | 1800    | Centro  | Tablet
```

**Dati Scientifici:**
```
Data       | Temperatura | Umidità | Città
2025-01-01 | 22.5       | 65      | Milano
2025-01-02 | 18.3       | 72      | Roma
2025-01-03 | 25.1       | 58      | Napoli
```

Il sistema riconosce automaticamente:
- **Colonne numeriche** → Statistiche descrittive, correlazioni
- **Colonne categoriche** → Distribuzioni, frequenze  
- **Colonne temporali** → Grafici di andamento nel tempo

---

## 🧪 Funzionalità future

- ⏳ Supporto file CSV in aggiunta a Excel
- ⏳ Analisi di regressione lineare e multivariata
- ⏳ Selezione interattiva colonne da analizzare
- ⏳ Grafici interattivi via Plotly.js
- ⏳ Export dati in formato JSON/CSV
- ⏳ Temi personalizzabili per i report PDF
- ⏳ Analisi predittive con machine learning

---

## 👤 Autore

**Statly** è un progetto open per fini didattici e personali, sviluppato per aiutare utenti a visualizzare e comprendere i propri dati senza complessità inutili.

---

## 📃 Licenza

Distribuito sotto licenza **MIT**. Vedi il file `LICENSE` per maggiori dettagli.
