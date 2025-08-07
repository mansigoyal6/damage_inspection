# Damage Inspection System

A modular backend system simulating a vehicle damage inspection workflow, built with Flask, SQLAlchemy (SQLite), and JWT authentication.

## Features
- User signup/login with JWT authentication
- Create, view, update, and list vehicle inspections
- Image URL validation
- Logging and robust error handling
- Easy deployment (I used Replit)


## API Endpoints
- `POST /signup` — Register user
- `POST /login` — Login, get JWT
- `POST /inspection` — Create inspection (JWT required)
- `GET /inspection/<id>` — Get inspection (JWT required)
- `PATCH /inspection/<id>` — Update status (JWT required)
- `GET /inspection?status=pending` — List inspections (JWT required)

---
