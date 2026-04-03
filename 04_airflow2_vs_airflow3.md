# Airflow 2.0 vs Airflow 3.0

Airflow 3.0 is the biggest release since 2.0 — a cleaner, faster, and more modern platform.

---

## Quick Comparison

| Feature | Airflow 2.0 | Airflow 3.0 |
|---------|-------------|-------------|
| Python support | 3.6+ | 3.9+ |
| DAG authoring | Traditional operators + TaskFlow API | TaskFlow API is the primary model |
| Scheduling | Time-based only | Time-based **+** event-driven (Assets) |
| `schedule_interval` param | ✅ Available | ❌ Removed — use `schedule` |
| `execution_date` | Primary run identifier | ❌ Replaced by `logical_date` |
| `catchup` default | `True` | `False` |
| SubDAGs | ✅ Supported | ❌ Removed — use TaskGroups |
| `airflow.contrib.*` | ✅ Available | ❌ Removed — use `airflow.providers.*` |
| Task execution | Subprocess on shared worker | Pluggable Task Execution Interface |
| UI framework | Angular (multiple separate views) | React (unified, real-time) |
| REST API | v1 — partial coverage | v2 — full OpenAPI 3.1 coverage |
| DAG serialization | Optional | Always on |
| Triggerer / deferrable operators | Introduced in 2.2 | Fully mature, recommended |
| Scheduler | Single process, fragile HA | Refactored — more reliable and scalable |

---

## Key Changes Explained

### DAG Authoring
Airflow 2.0 had two styles — the old verbose `PythonOperator` style and the newer `@task` decorator (TaskFlow API). In Airflow 3.0, **TaskFlow is the default**. The old-style is still supported but discouraged.

### Event-Driven Scheduling (Assets)
Airflow 2.0 only ran on a time schedule. Airflow 3.0 introduces **Assets** (previously called Datasets) — you can trigger a DAG to run when another DAG produces a result. You can combine conditions with AND/OR logic.

### Task Execution Interface
In Airflow 2.0, tasks run as subprocesses on the worker — every worker needs the full Airflow install. In 3.0, a pluggable **Task Execution Interface** allows tasks to run in isolated environments (containers, virtual envs) with just a lightweight Task SDK — not the full Airflow package.

### UI
Fully rewritten in **React**. All views (graph, grid, Gantt) are now unified in one page with real-time updates.

### REST API
Rebuilt from scratch as **OpenAPI 3.1** (v2). The UI itself now uses this API. Full coverage of all resources.

### Removed Legacy Features
Airflow 3.0 cleaned up everything that had been deprecated for years:
- `schedule_interval` → `schedule`
- `execution_date` → `logical_date`
- `SubDagOperator` → `TaskGroup`
- `airflow.contrib.*` → `airflow.providers.*`
- `airflow db upgrade` → `airflow db migrate`

---

## Migration Summary (2.x → 3.0)

If you have existing 2.x DAGs, the main things to fix are:

1. Replace `schedule_interval=` with `schedule=`
2. Replace `execution_date` with `logical_date`
3. Replace SubDagOperators with TaskGroups
4. Update all `airflow.contrib` imports to `airflow.providers`
5. Set `catchup=False` explicitly if you don't want backfills

---

> **Next:** [Sample ETL Pipeline →](./dags/sample_etl_pipeline.py)
