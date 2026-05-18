# SWE Job Simulator — Dash Application

A production-grade software engineering job market intelligence dashboard built
with **Plotly Dash**, **NumPy**, and **Pandas**. Fully CI-ready with a
**pytest + unittest** test suite and a **GitHub Actions** workflow.

---

## Repository Structure

```
swe_job_sim/
├── app.py                      ← Dash application (entry point)
├── requirements.txt            ← Python dependencies
├── pytest.ini                  ← pytest configuration
├── README.md
├── tests/
│   ├── __init__.py
│   └── test_app.py             ← Full test suite (unittest + pytest)
└── .github/
    └── workflows/
        └── ci.yml              ← GitHub Actions CI pipeline
```

---

## Quick Start

### 1. Clone & create virtualenv

```bash
git clone https://github.com/YOUR_USERNAME/swe-job-simulator.git
cd swe_job_sim
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
# → Open http://localhost:8050
```

---

## Running the Test Suite

### All tests (recommended)

```bash
pytest tests/test_app.py -v
```

### With coverage report

```bash
pytest tests/test_app.py -v --cov=app --cov-report=term-missing
```

### Via unittest runner (alternative)

```bash
python -m unittest tests.test_app -v
```

### Generate JUnit XML (for CI)

```bash
mkdir -p reports
pytest tests/test_app.py -v --junitxml=reports/junit.xml
```

---

## Test Coverage

| Test Class              | What it checks                                              |
|-------------------------|-------------------------------------------------------------|
| `TestLayoutStructure`   | Header, region picker, viz section present in layout        |
| `TestJobData`           | Data completeness, type validity, value ranges              |
| `TestFigures`           | All 4 figure builders return valid `go.Figure` objects      |
| `TestAppServer`         | Flask server runs, `/` returns HTTP 200                     |
| `TestCallbacks`         | `update_dashboard` returns correct outputs for every region |
| Standalone pytest fns   | Quick smoke tests as bare functions                         |

**Total: 30+ individual test cases across 5 classes + standalone functions.**

---

## Continuous Integration

The `.github/workflows/ci.yml` pipeline runs automatically on every:

- `push` to `main`, `develop`, or any `feature/**` branch
- `pull_request` targeting `main`

It tests against **Python 3.10, 3.11, and 3.12** in parallel, uploads
JUnit/coverage XML as artifacts, and (optionally) sends coverage to Codecov.

### CI philosophy

> "Three developers using CI kept their feature branches up to date with `main`,
> spending far less time on merge conflicts and more time shipping features."

This repo follows that same principle:
- Small PRs merged frequently
- Every commit verified by the full test suite automatically
- Coverage enforced to catch regressions early

---

## Dashboard Features

| Feature          | Details                                                |
|------------------|--------------------------------------------------------|
| **Header**       | App branding, live badge, year range badge             |
| **Region Picker**| Dropdown: Global / North America / Europe / APAC / India / LatAm |
| **KPI Row**      | Total openings · Avg salary · Avg YoY growth · Top-paying role |
| **Bar Chart**    | Job openings by role for selected region               |
| **Scatter Plot** | Salary vs growth rate, bubble size = openings          |
| **Gauge**        | Average remote-work availability %                     |
| **Radar Chart**  | Normalised salary & openings comparison across roles   |

---

## License

MIT
