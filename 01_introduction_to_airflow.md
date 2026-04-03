# Introduction to Apache Airflow

---

## What is Apache Airflow?

**Apache Airflow** is an open-source platform to **author, schedule, and monitor workflows** as Python code.

- Created at **Airbnb in 2014**, open-sourced in 2015, Apache top-level project in 2019.
- Workflows are defined as **Python code** — version-controlled, testable, and dynamic.
- A workflow is called a **DAG** (Directed Acyclic Graph) — a set of tasks with defined dependencies.

```
Extract → Transform → Load
```

---

## The Problem Before Airflow — Cron

`cron` schedules a script to run at a fixed time. It works fine for simple, one-shot jobs.

**Where cron breaks down:**

| Problem | Cron's limitation |
|---------|------------------|
| Task dependencies | Cannot wait for another job to succeed |
| Visibility | No UI — no idea what ran or failed |
| Retries | No automatic retry on failure |
| Backfilling | Cannot re-run past dates easily |
| Parallelism | No built-in parallel execution |
| Alerts | No notifications on failure |

> Imagine 50 cron jobs. One fails silently at 2 AM. You find out the next morning from stale dashboards — with no idea which job failed or why.

---

## How Data Engineering Evolved

| Era | Situation |
|-----|-----------|
| Early 2000s | Simple ETL — one script, one server, cron was enough |
| 2010s | Big Data boom — Hadoop, Spark, dozens of interdependent jobs |
| Mid-2010s | Teams hacked Jenkins/Nagios as orchestrators — brittle and unmaintainable |
| 2014 | Airbnb built **Airflow** to solve orchestration at scale |
| Today | Airflow is the industry standard — used by Google, LinkedIn, Lyft, and thousands more |

---

## Problems Airflow Solves

- **Dependencies** — Task B runs only after Task A succeeds. Failure stops the chain.
- **Scheduling** — Cron expressions, presets (`@daily`, `@hourly`), or event-based triggers.
- **Backfilling** — Re-run the pipeline for any historical date range.
- **Monitoring** — Visual graph UI showing task status, logs, and run history.
- **Retries** — Automatic retry with configurable delay.
- **Alerts** — Email or Slack notifications on failure.
- **Dynamic Pipelines** — Generate tasks programmatically using Python loops.
- **Integrations** — Built-in operators for Postgres, S3, BigQuery, Snowflake, Spark, dbt, and more.

---

## Core Concepts

| Term | What it is |
|------|-----------|
| **DAG** | The pipeline — a graph of tasks |
| **Task** | One unit of work |
| **Operator** | The type of task (PythonOperator, BashOperator, etc.) |
| **Scheduler** | Decides when to run DAGs |
| **Executor** | Dispatches tasks to workers |
| **Worker** | Actually runs the task code |
| **Webserver** | The UI at `localhost:8080` |
| **Metadata DB** | Stores all state, logs, history |
| **XCom** | Passes small data between tasks |
| **Connection** | Stored credential (DB URL, API key) |
| **Variable** | Key-value config store |

---

## When to Use Airflow

- Multi-step data pipelines (ETL / ELT)
- Jobs with complex dependencies
- Pipelines that need monitoring and alerting
- Historical backfills
- Team workflows where code review and version control matter

## When NOT to Use Airflow

| Situation | Better tool |
|-----------|------------|
| Simple one-script schedule | Plain cron |
| Real-time / streaming | Kafka, Flink |
| CI/CD pipelines | GitHub Actions, Jenkins |

> Airflow is a **batch orchestrator** — not a streaming engine.

---

> **Next:** [Airflow Architecture →](./02_airflow_architecture.md)
