# Airflow Architecture

---

## Overview

Airflow is built on a **separation of concerns** — each component has one job, and they all communicate through a central **Metadata Database**.

```
  dags/ folder
       │  (Python files)
       ▼
  Scheduler  ◄──────────────────────► Webserver (UI)
       │                                    │
       ▼                                    │
  Metadata DB  ◄──────────────────────────-┘
       │
       ▼
   Executor
  ┌────┼────┐
Worker Worker Worker
```

---

## Core Components

### Webserver
- Serves the **Airflow UI** at `http://localhost:8080`.
- Reads state from the Metadata DB — does **not** run or schedule tasks.
- Used for: viewing DAGs, triggering runs, inspecting logs.

### Scheduler
- The **heart of Airflow**.
- Continuously scans the `dags/` folder, parses DAG files.
- Creates DAG Runs and Task Instances at the right time.
- Sends ready tasks to the Executor.

### Executor
- Decides **how** tasks are run (local subprocess, distributed workers, Kubernetes pods).
- Does not run tasks itself — it dispatches them.

| Executor | Use Case |
|----------|----------|
| **LocalExecutor** | Single machine, parallel tasks |
| **CeleryExecutor** | Distributed workers via Redis/RabbitMQ |
| **KubernetesExecutor** | One pod per task — cloud-native |
| **SequentialExecutor** | Dev/testing only (one task at a time) |

### Worker
- The process that **actually executes task code**.
- Reports success or failure back to the Metadata DB.

### Triggerer
- Handles **deferrable (async) tasks** — tasks that wait for external events (e.g., file arrives on S3).
- Frees up worker slots instead of polling and blocking.

### Metadata Database
- The **single source of truth** — stores DAG metadata, run history, task states, logs, connections, and variables.
- Supported: **PostgreSQL** (production), MySQL, SQLite (dev only).

### DAG Folder
- A directory of `.py` files. The Scheduler scans it every ~30 seconds.
- In Docker, this folder is **volume-mounted** into the containers.

---

## How a DAG Run Works (Step by Step)

```
1. You drop a .py DAG file into dags/
2. Scheduler parses it → stores metadata in DB
3. At the scheduled time → Scheduler creates a DAG Run
4. Tasks with no upstream dependencies → set to "queued"
5. Executor picks up queued tasks → sends to Workers
6. Worker runs the task → writes logs → updates state in DB
7. Scheduler sees completed tasks → queues downstream tasks
8. Repeat until all tasks succeed or one fails
9. Webserver reflects the final state in the UI
```

---

## Task Lifecycle States

```
queued → running → success
                 ↘ failed → up_for_retry → queued
                 ↘ skipped  (branch logic)
                 ↘ deferred (async trigger)
                 ↘ upstream_failed (parent task failed)
```

---

## XCom — Passing Data Between Tasks

Tasks run as isolated processes. **XCom** lets them share small pieces of data.

- A task **pushes** a value; a downstream task **pulls** it.
- Stored in the Metadata DB — use for small values only (IDs, counts, file paths).
- With the TaskFlow API (`@task`), XCom is handled automatically via return values.

---

## Connections and Variables

- **Connection** — a named, stored credential (DB host, API key). Referenced by `conn_id` in operators — keeps secrets out of DAG code.
- **Variable** — a key-value config pair stored in Airflow. Useful for environment-specific settings (bucket names, table names, flags).

---

> **Next:** [Setup Guide →](./03_setup_guide.md)
