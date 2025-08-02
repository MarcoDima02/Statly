# 📊 Statly

**Statly** è un'applicazione web interattiva per l’analisi statistica di file CSV. Progettata per essere semplice, veloce ed efficace, consente di caricare dataset, generare analisi statistiche descrittive e visualizzare grafici dinamici. L'output può essere comodamente scaricato come file PDF, pronto per essere condiviso o archiviato.

## 🚀 Caratteristiche principali

- ✅ Upload di file CSV (es. progressi in palestra, misurazioni, dati tabellari)
- ✅ Analisi statistiche descrittive automatiche (media, massimo, minimi, andamento nel tempo)
- ✅ Generazione di grafici dinamici (es. linea, barre)
- ✅ Esportazione completa in PDF
- ✅ Nessuna autenticazione necessaria: utilizzo immediato

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
| Backend      | Python 3.11, FastAPI   |
| Analisi dati | pandas, matplotlib     |
| PDF export   | ReportLab, matplotlib  |
| Frontend     | HTML5, CSS3, JS        |
| Contenitori  | Docker, Docker Compose |

---

## 📦 Setup locale

> Requisiti: Python 3.11+ e Docker installati.

### 🔧 Avvio in locale senza Docker

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 🐳 Avvio tramite Docker

```bash
docker-compose up --build
```

Una volta in esecuzione, visita [http://localhost:8000](http://localhost:8000) per accedere all'interfaccia.

---

## 📂 Esempio d'Uso

1. Carica un file `.csv` con dati tabellari.
2. L'app effettua analisi statistiche sul dataset.
3. Viene generato un PDF contenente:
   - Dati riassuntivi (media, massimo, conteggi)
   - Grafici (es. andamento di un esercizio nel tempo)
4. Il PDF è scaricabile direttamente dal browser.

---

## 📄 Esempio di Dataset Supportato

```csv
Data,Esercizio,Peso,Ripetizioni
2025-06-01,Panca,60,10
2025-06-08,Panca,62.5,8
2025-06-15,Panca,65,8
2025-06-22,Squat,80,10
...
```

---

## 🧪 Funzionalità future

- ⏳ Analisi di correlazione e regressione lineare
- ⏳ Selezione colonne da analizzare
- ⏳ Supporto a file Excel (.xlsx)
- ⏳ Interfaccia grafica migliorata (con grafici interattivi via Plotly.js)

---

## 👤 Autore

**Statly** è un progetto open per fini didattici e personali, sviluppato per aiutare utenti a visualizzare e comprendere i propri dati senza complessità inutili.

---

## 📃 Licenza

Distribuito sotto licenza **MIT**. Vedi il file `LICENSE` per maggiori dettagli.
