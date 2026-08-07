# 🏥 Patient Management System API

A fully functional REST API for managing patient records, built with **FastAPI**, validated with **Pydantic v2**, and containerized with **Docker**. The API automatically computes each patient's BMI and health verdict from their height and weight.

## ✨ Features
- **Full CRUD operations** — create, read, update, and delete patient records.
- **Automatic BMI & verdict computation** using Pydantic computed fields — recalculated on every update.
- **Robust input validation** — type checking, value constraints, and enum-restricted fields.
- **Partial updates** — the PUT /edit endpoint updates only the fields you send.
- **Sorting** — sort patients by height, weight, or BMI.
- **Interactive API docs** — auto-generated Swagger UI at /docs.
- **Fully containerized** — runs anywhere with a single docker run.

## 🛠️ Tech Stack
FastAPI · Pydantic v2 · Uvicorn · Docker

## 📋 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /view | Retrieve all patients |
| GET | /patient/{id} | Retrieve a single patient |
| GET | /sort | Sort patients by a field |
| POST | /create | Create a new patient |
| PUT | /edit/{id} | Update a patient (partial) |
| DELETE | /delete/{id} | Delete a patient |

## 🚀 Running with Docker
\\\ash
docker build -t patient-api .
docker run -p 8000:8000 patient-api
\\\
Then open http://localhost:8000/docs

## 💻 Running Locally
\\\ash
pip install -r requirements.txt
uvicorn main:app --reload
\\\

## 📊 BMI Categories
| Verdict | BMI Range |
|---------|-----------|
| Underweight | < 18.5 |
| Normal | 18.5 – 24.9 |
| Overweight | 25 – 29.9 |
| Obese | ≥ 30 |

## 👤 Author
**Sufian Kanaan** — [GitHub](https://github.com/Sufiankanaan)
