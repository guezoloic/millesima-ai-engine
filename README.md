# Millesima AI Engine 🍷

> A **University of Paris-Est Créteil (UPEC)** Semester 6 project.

## Documentation
- 🇫🇷 [Version Française](https://guezoloic.github.io/millesima-ai-engine)
> note: only french version enabled for now.
---

## Installation
> Make sure you have **Python 3.10+** installed.

1. **Clone the repository:**
    ```bash
    git clone https://github.com/votre-pseudo/millesima-ai-engine.git
    cd millesima-ai-engine
    ```

2. **Set up a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -e .
    ```

## Usage

### 1. Data Extraction (Scraping)
To fetch the latest wine data from Millesima:
```bash
python3 src/scraper.py
```
> Note: that will take some time to fetch all data depending on the catalog size.