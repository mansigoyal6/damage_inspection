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

Live url to run api - https://f9549383-2858-4449-97d3-e6cd7eaa1d09-00-2qwaxs40p1ioj.sisko.replit.dev/

Curls-
1)Signup-
curl --location 'https://f9549383-2858-4449-97d3-e6cd7eaa1d09-00-2qwaxs40p1ioj.sisko.replit.dev/signup' \
--header 'Content-Type: application/json' \
--header 'X-Requested-With: XMLHttpRequest' \
--header 'Origin: https://damageinspection.mansigoyal5678.repl.co' \
--data '{
    "username": "Mansi",
    "password": "testpassm"
}'

2)Login-
curl --location 'https://f9549383-2858-4449-97d3-e6cd7eaa1d09-00-2qwaxs40p1ioj.sisko.replit.dev/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "Mansi",
    "password": "testpassm"
}'

3)create inspection -
curl --location 'https://f9549383-2858-4449-97d3-e6cd7eaa1d09-00-2qwaxs40p1ioj.sisko.replit.dev/inspection' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDU4NTc4NywianRpIjoiN2FiMjU1NjgtZGE1MS00NWNlLWI5YzYtYzZlY2ZjYjNhODg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTQ1ODU3ODcsImNzcmYiOiIwOWE3Nzc1Yi1lZDcxLTQ1N2ItYTk3MC0wMTlmMDkxMTdlMDAiLCJleHAiOjE3NTQ2Mjg5ODd9.9_fljMJbJ-byNnqWQb8jVr8B__dkGePKsVKmRchxj2o' \
--data '{
    "vehicle_number": "DL01AB1234",
    "damage_report": "Broken tail light",
    "image_url": "https://damageimg.com/image.jpg"
}'

4)Get inspection by id-
curl --location --request GET 'https://f9549383-2858-4449-97d3-e6cd7eaa1d09-00-2qwaxs40p1ioj.sisko.replit.dev/inspection/4' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDU4NTc4NywianRpIjoiN2FiMjU1NjgtZGE1MS00NWNlLWI5YzYtYzZlY2ZjYjNhODg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTQ1ODU3ODcsImNzcmYiOiIwOWE3Nzc1Yi1lZDcxLTQ1N2ItYTk3MC0wMTlmMDkxMTdlMDAiLCJleHAiOjE3NTQ2Mjg5ODd9.9_fljMJbJ-byNnqWQb8jVr8B__dkGePKsVKmRchxj2o' \
--header 'Content-Type: application/json' \
--data '{}'

5)update status-
curl --location --request PATCH 'https://f9549383-2858-4449-97d3-e6cd7eaa1d09-00-2qwaxs40p1ioj.sisko.replit.dev/inspection/4' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDU4NTc4NywianRpIjoiN2FiMjU1NjgtZGE1MS00NWNlLWI5YzYtYzZlY2ZjYjNhODg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTQ1ODU3ODcsImNzcmYiOiIwOWE3Nzc1Yi1lZDcxLTQ1N2ItYTk3MC0wMTlmMDkxMTdlMDAiLCJleHAiOjE3NTQ2Mjg5ODd9.9_fljMJbJ-byNnqWQb8jVr8B__dkGePKsVKmRchxj2o' \
--data '{"status": "reviewed"}'

6)Get all inspection-
curl --location --request GET 'https://f9549383-2858-4449-97d3-e6cd7eaa1d09-00-2qwaxs40p1ioj.sisko.replit.dev/inspection' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDU4NTc4NywianRpIjoiN2FiMjU1NjgtZGE1MS00NWNlLWI5YzYtYzZlY2ZjYjNhODg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTQ1ODU3ODcsImNzcmYiOiIwOWE3Nzc1Yi1lZDcxLTQ1N2ItYTk3MC0wMTlmMDkxMTdlMDAiLCJleHAiOjE3NTQ2Mjg5ODd9.9_fljMJbJ-byNnqWQb8jVr8B__dkGePKsVKmRchxj2o' \
--header 'Content-Type: application/json' \
--data '{}'

7)Get all inspection by status-
curl --location --request GET 'https://f9549383-2858-4449-97d3-e6cd7eaa1d09-00-2qwaxs40p1ioj.sisko.replit.dev/inspection?status=reviewed' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NDU4NTc4NywianRpIjoiN2FiMjU1NjgtZGE1MS00NWNlLWI5YzYtYzZlY2ZjYjNhODg5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NTQ1ODU3ODcsImNzcmYiOiIwOWE3Nzc1Yi1lZDcxLTQ1N2ItYTk3MC0wMTlmMDkxMTdlMDAiLCJleHAiOjE3NTQ2Mjg5ODd9.9_fljMJbJ-byNnqWQb8jVr8B__dkGePKsVKmRchxj2o' \
--header 'Content-Type: application/json' \
--data '{}'
