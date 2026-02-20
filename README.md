# Guest Room Home Assistant Gateway

A minimal FastAPI-based gateway that exposes a restricted web interface for controlling selected Home Assistant entities inside a guest room.

The application is designed to run in a segregated guest network environment and only allows access to explicitly whitelisted entities.

---

## Purpose

In our home setup, guests connect to a dedicated guest Wi-Fi that does not have access to our internal Home Assistant instance.

This project provides:

- A lightweight web interface (Bootstrap 5)
- A secure FastAPI backend
- A strict whitelist for allowed entities
- Controlled access to selected lights and blinds only

The goal is to allow guests to control specific devices in the guest room without exposing the full Home Assistant system.

---

## Architecture Overview

### High-Level Flow

```
Guest Device (Guest Wi-Fi)
        │
        ▼
Ingress (Guest Network IP)
        │
        ▼
Kubernetes Pod (FastAPI App)
        │
        ▼
Internal Ingress (Home Network)
        │
        ▼
Home Assistant
```

### Network Separation

- The application will be deployed to a private Kubernetes cluster at home.
- It will run behind a dedicated Ingress exposed only to the Guest Wi-Fi network.
- The backend communicates with a second internal Ingress that exposes Home Assistant within the internal network.
- Guests never receive direct access to Home Assistant.

---

## Features

### Lights

- Toggle control (on/off)
- Strict alias-based access
- Backend validates entity whitelist
- Calls:
  - `light.turn_on`
  - `light.turn_off`

### Blinds

- Position control (0–100)
- Tilt control (0–100)
- Backend validation using Pydantic
- Calls:
  - `cover.set_cover_position`
  - `cover.set_cover_tilt_position`

---

## Security Design

- Home Assistant token is stored in `.env`
- `.env` is excluded via `.gitignore`
- Only predefined entity aliases are accepted
- No dynamic entity IDs from clients
- Input validation (0–100 range enforcement)

Example validation:

```python
value: int = Field(ge=0, le=100)
```

---

## Tech Stack

- Python 3
- FastAPI
- Pydantic
- httpx
- Bootstrap 5
- Kubernetes (deployment target)
- NGINX Ingress (planned)
- Home Assistant REST API

---

## Local Development

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn httpx python-dotenv
```

### Environment Variables

Create a `.env` file in the project root:

```
HA_BASE_URL=https://ha.example.local
HA_TOKEN=your_long_lived_token
```

### Run

```bash
uvicorn main:app --reload
```

---

## API Endpoints

### Health Check

```
GET /health
```

### Test Home Assistant Connection

```
GET /ha-test
```

### Toggle Light

```
POST /api/lights/{alias}
Body:
{
  "on": true
}
```

### Set Blind Position

```
POST /api/blinds/position
Body:
{
  "value": 0-100
}
```

### Set Blind Tilt

```
POST /api/blinds/tilt
Body:
{
  "value": 0-100
}
```

---

## Deployment Plan (Future)

- Containerize application
- Deploy to private home Kubernetes cluster
- Configure dedicated Guest-WLAN Ingress
- Route backend traffic to internal HA Ingress
- Isolate guest access from internal services

---

## Design Principles

- Minimal dependencies
- Explicit security boundaries
- Clear separation of frontend and backend
- Whitelist-based access control
- Learning-by-building API architecture

---

## Status

Functional v1 complete (backend + frontend integration).  
Awaiting hardware/network adjustments for full guest Wi-Fi deployment.
````
