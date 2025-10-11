# Apache Airflow 3.1.0 Setup Guide (WSL + Docker)

This guide explains how to install and run **Apache Airflow 3.1.0** using Docker Compose inside a WSL (Windows Subsystem for Linux) environment. It covers all steps from setting up Ubuntu to accessing the Airflow web interface.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
  - [1. Install Ubuntu on WSL](#1-install-ubuntu-on-wsl)
  - [2. Enable Docker Integration with WSL](#2-enable-docker-integration-with-wsl)
  - [3. Set Up a Working Directory](#3-set-up-a-working-directory)
  - [4. Download the Airflow Docker Compose File](#4-download-the-airflow-docker-compose-file)
  - [5. Create the Environment File](#5-create-the-environment-file)
  - [6. Initialize Airflow](#6-initialize-airflow)
  - [7. Start Airflow](#7-start-airflow)
  - [8. Access the Airflow Web Interface](#8-access-the-airflow-web-interface)
  - [9. Stop and Restart Airflow](#9-stop-and-restart-airflow)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you start, make sure you have the following installed:

1. **Windows 10 or 11** with **WSL 2 enabled**
2. **Docker Desktop** installed and running
3. **Ubuntu** configured as your default WSL distribution


---

## Installation Steps

### 1. Install Ubuntu on WSL

Open **PowerShell** as an Administrator and run:

```bash
wsl --install -d Ubuntu
```

Once installed, launch Ubuntu from the Start Menu and complete the setup (create username and password).

> **Note:** You can open the Ubuntu terminal any time by searching for "Ubuntu" in the Start Menu.

---

### 2. Enable Docker Integration with WSL

1. Open **Docker Desktop**
2. Go to **Settings** â†’ **Resources** â†’ **WSL Integration**
3. Enable **"Enable integration with my default WSL distro"**
4. Check that **Ubuntu** is selected
5. Click **Apply & Restart**

After Docker restarts, verify that Docker works inside Ubuntu:

```bash
docker --version
docker compose version
```

You should see valid version outputs for both commands.

---

### 3. Set Up a Working Directory

In your Ubuntu terminal, create a working directory:

```bash
mkdir airflow-docker
cd airflow-docker
```

This will be your main Airflow project directory.

---

### 4. Download the Airflow Docker Compose File

Download the official Docker Compose file for Airflow 3.1.0:

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.1.0/docker-compose.yaml'
```

Verify that the file is downloaded:

```bash
ls
```

You should see a file named `docker-compose.yaml`.

---

### 5. Create the Environment File

Airflow uses a `.env` file to define environment variables such as the user ID.

Run the following command to create it:

```bash
echo -e "AIRFLOW_UID=50000" > .env
```

This ensures Docker containers have proper permission to write files on your system.

---

### 6. Initialize Airflow

Before running Airflow, initialize its database and default user:

```bash
docker compose up airflow-init
```

This command downloads required images and sets up the Airflow database.

> **Note:** Once the process completes, stop it by pressing `Ctrl + C`.

---

### 7. Start Airflow

Start all Airflow services in the background:

```bash
docker compose up --build -d
```

You can check that all containers are running with:

```bash
docker ps
```

You should see containers for the **webserver**, **scheduler**, **triggerer**, **PostgreSQL**, and **Redis**.

---

### 8. Access the Airflow Web Interface

When the containers are healthy, open your browser and go to:

```
http://localhost:8080
```

**Default credentials:**

- **Username:** `airflow`
- **Password:** `airflow`

> **Note:** The webserver may take a few minutes to start on first run.

---

### 9. Stop and Restart Airflow

**To stop all containers:**

```bash
docker compose down
```

**To start them again later:**

```bash
docker compose up -d
```

**To check container status:**

```bash
docker ps
```

---

## Troubleshooting

### Airflow UI not loading

Wait a few minutes after startup; the webserver takes time to initialize.

### Port 8080 already in use

Stop any process using port 8080 or change the port mapping in `docker-compose.yaml`.

### Permission errors

Ensure your `.env` file exists and contains `AIRFLOW_UID=50000`.

### Checking Container Logs

To check logs for any container:

```bash
docker logs <container_name>
```

**Example:**

```bash
docker logs airflow-webserver-1
```

---

## Additional Resources

- [Apache Airflow Official Documentation](https://airflow.apache.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)

---

## License

This setup guide is provided as-is for educational and development purposes.