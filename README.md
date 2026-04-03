# Apache Airflow — Teaching Course

A structured, classroom-ready repository covering Apache Airflow from the ground up.  
All examples target **Airflow 3.x** running on Docker + WSL.

---

## Course Outline

| # | File | What You Will Learn |
|---|------|---------------------|
| 1 | [Introduction to Airflow](./01_introduction_to_airflow.md) | What Airflow is, why it exists, evolution from cron |
| 2 | [Airflow Architecture](./02_airflow_architecture.md) | Core components, how they interact, execution model |
| 3 | [Setup Guide (Docker + WSL)](./03_setup_guide.md) | Installing and running Airflow locally on Windows |
| 4 | [Airflow 2.0 vs Airflow 3.0](./04_airflow2_vs_airflow3.md) | Key differences, breaking changes, what's new |
| 5 | [Sample ETL Pipeline DAG](./dags/sample_etl_pipeline.py) | A runnable 4-task ETL DAG to explore in the UI |

---

## Quick Start

1. Follow the [Setup Guide](./03_setup_guide.md) to get Airflow running locally.
2. Copy `dags/sample_etl_pipeline.py` into your Airflow `dags/` folder.
3. Open `http://localhost:8080` and trigger the DAG named **`sample_etl_pipeline`**.

---

## Prerequisites

- Windows 10/11 with WSL 2
- Docker Desktop
- Basic Python knowledge

---

## Repository Structure

```
airflow-teaching-course/
├── README.md                        ← You are here (course index)
├── 01_introduction_to_airflow.md   ← What is Airflow & why it matters
├── 02_airflow_architecture.md      ← Architecture deep-dive
├── 03_setup_guide.md               ← Installation on Docker + WSL
├── 04_airflow2_vs_airflow3.md      ← Version comparison
└── dags/
    └── sample_etl_pipeline.py      ← Runnable ETL example
```

---

> **License:** Provided for educational purposes.
