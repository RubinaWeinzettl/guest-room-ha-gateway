# Guest Room Control  
## Home Assistant Gateway (Concept Phase)

---

## Status

This project is currently in the **architecture and planning phase**.  
No implementation has been started yet.

The goal is to design a secure and minimal web-based control interface for a guest room without exposing the full Home Assistant system.

---

## Project Idea

Guests connected to the guest Wi-Fi should be able to control a limited set of predefined devices:

- 4 light toggles
- Blind position (open / close)
- Blind tilt (lamella angle)

Direct access to Home Assistant from the guest network must remain blocked.

The application will act as a controlled API gateway between the guest network and Home Assistant.

---

## Planned Architecture

### Frontend
- Static HTML
- Bootstrap (via CDN)
- Minimal JavaScript (Fetch API)

### Backend
- Python
- FastAPI
- REST communication with Home Assistant
- Strict whitelist validation for allowed entities
- Alias mapping (UI identifiers ≠ Home Assistant entity IDs)

Home Assistant remains isolated in the internal network.

---

## Development Plan

Initial development will take place locally using:

- Python virtual environment (`venv`)
- ddev
- Apache

Migration to the existing Kubernetes cluster is planned **after** the application logic is complete and validated.

---

## Design Principles

- Network isolation between guest Wi-Fi and Home Assistant
- Application-level access control via whitelist
- No exposure of internal entity names
- Minimal frontend complexity
- Clear separation between UI, backend logic, and infrastructure

---

## Purpose of the Project

- Practice API design with FastAPI
- Design secure service exposure patterns
- Implement whitelist-based access control
- Prepare for later containerization and Kubernetes deployment
- Bridge development and infrastructure thinking in a practical smart home use case
