# Apache Airflow Setup Guide (WSL + Docker)

---

## Prerequisites

- Windows 10/11 with **WSL 2** enabled
- **Docker Desktop** installed and running
- **Ubuntu** set as your default WSL distro

---

## Step-by-Step Setup

### 1. Install Ubuntu on WSL

Open PowerShell as Administrator:

```bash
wsl --install -d Ubuntu
```

Launch Ubuntu from the Start Menu and create a username + password.

---

### 2. Enable Docker in WSL

1. Open **Docker Desktop → Settings → Resources → WSL Integration**
2. Enable integration with Ubuntu
3. Click **Apply & Restart**

Verify inside Ubuntu:

```bash
docker --version
docker compose version
```

---

### 3. Create a Working Directory

```bash
mkdir airflow-docker
cd airflow-docker
mkdir -p ./dags ./logs ./plugins ./config
```

---

### 4. Download Docker Compose File

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

---

### 5. Create the `.env` File

```bash
echo -e "AIRFLOW_UID=50000" > .env
```

This sets the correct file permissions for Docker containers.

---

### 6. Initialize Airflow

```bash
docker compose up airflow-init
```

Wait for it to finish (you'll see `exited with code 0`), then press `Ctrl + C`.

---

### 7. Start Airflow

```bash
docker compose up -d
```

Check containers are running:

```bash
docker ps
```

You should see: **webserver, scheduler, triggerer, worker, postgres, redis**.  
Wait 1–2 minutes for everything to become healthy.

---

### 8. Open the UI

Go to `http://localhost:8080`

- **Username:** `airflow`
- **Password:** `airflow`

---

### 9. Add Your DAGs

Copy your DAG file into the `dags/` folder — Airflow picks it up automatically within ~30 seconds.

```bash
cp sample_etl_pipeline.py ./dags/
```

---

### 10. Stop / Restart

```bash
# Stop
docker compose down

# Start again
docker compose up -d

# Full reset (deletes all history)
docker compose down --volumes --remove-orphans
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| UI not loading | Wait 2 min; run `docker ps` and check containers are `healthy` |
| Port 8080 in use | Change left port in `docker-compose.yaml` → `"8081:8080"` |
| Permission errors | Check `.env` has `AIRFLOW_UID=50000`; check `dags/` folder exists |
| DAG not showing in UI | Check syntax with `python your_dag.py`; check scheduler logs |

```bash
# View logs for any container
docker logs airflow-airflow-scheduler-1
docker logs airflow-airflow-webserver-1
```

---

> **Next:** [Airflow 2.0 vs Airflow 3.0 →](./04_airflow2_vs_airflow3.md)
