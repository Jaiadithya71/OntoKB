# Docker Guide for ontoKBv2

This directory contains resources for containerizing and distributing the ontoKBv2 application.

---

## 1. Quick Start with Docker Compose (Recommended)

To build and start the ontoKB container with persistent storage and port forwarding:

```powershell
docker compose up -d
```

- **Web & API Access**: [http://localhost:8765](http://localhost:8765)
- **Persisted Data**:
  - `data/` (SQLite graph database)
  - `vault/` (Obsidian markdown notes and reports)
  - `config/` (Settings and configuration YAML)

To stop the container:
```powershell
docker compose down
```

---

## 2. Manual Docker Build & Run

### Build the Image
```powershell
docker build -t ontokb:latest .
```

### Run the Container
```powershell
docker run -d `
  --name ontokb-app `
  -p 8765:8765 `
  -v "${PWD}/data:/app/data" `
  -v "${PWD}/vault:/app/vault" `
  -v "${PWD}/config:/app/config" `
  ontokb:latest
```

---

## 3. Storing / Exporting the Image as a File

If you want to keep a portable offline image package in the project folder or transfer it to another server:

### Automated Script
Run the helper script:
```powershell
.\docker\build_and_save.ps1
```
This builds `ontokb:latest` and exports it to `docker/ontokb-latest.tar`.

### Manual Save & Load Commands
```powershell
# Save image to tarball
docker save -o docker/ontokb-latest.tar ontokb:latest

# On another machine, load the tarball
docker load -i docker/ontokb-latest.tar
```

---

## 4. Running CLI Commands Inside the Container

You can execute any `ontokb` CLI command directly in the running container:

```powershell
# Ingest an article or video URL
docker exec -it ontokb-app python -m ontokb.cli ingest "https://www.163.com/dy/article/..."

# Check knowledge graph status
docker exec -it ontokb-app python -m ontokb.cli status

# Run rule engine
docker exec -it ontokb-app python -m ontokb.cli rules
```
