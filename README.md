# 🏥 Patient Management System API

A fully functional REST API for managing patient records, built with **FastAPI**, validated with **Pydantic v2**, and containerized with **Docker**. The API automatically computes each patient's BMI and health verdict from their height and weight.

---

## ✨ Features

- **Full CRUD operations** — create, read, update, and delete patient records.
- **Automatic BMI & verdict computation** using Pydantic computed fields — recalculated on every update.
- **Robust input validation** — type checking, value constraints (positive height/weight, age bounds), and enum-restricted fields (`gender`).
- **Partial updates** — the `PUT /edit` endpoint updates only the fields you send, leaving the rest untouched.
- **Sorting** — sort patients by height, weight, or BMI in ascending or descending order.
- **Interactive API docs** — auto-generated Swagger UI at `/docs`.
- **Fully containerized** — runs anywhere with a single `docker run`.

---

## 🛠️ Tech Stack

- **FastAPI** — web framework
- **Pydantic v2** — data validation & computed fields
- **Uvicorn** — ASGI server
- **Docker** — containerization

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/about` | API description |
| `GET` | `/view` | Retrieve all patients |
| `GET` | `/patient/{patient_id}` | Retrieve a single patient by ID |
| `GET` | `/sort?sort_by=bmi&order=desc` | Sort patients by a field |
| `POST` | `/create` | Create a new patient |
| `PUT` | `/edit/{patient_id}` | Update an existing patient (partial) |
| `DELETE` | `/delete/{patient_id}` | Delete a patient |

---

## 🚀 Running with Docker

**Build the image:**
```bash
docker build -t patient-api .
```

**Run the container:**
```bash
docker run -p 8000:8000 patient-api
```

Then open the interactive docs at:
```
http://localhost:8000/docs
```

---

## 💻 Running Locally (without Docker)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📦 Example — Create a Patient

**Request** — `POST /create`
```json
{
  "id": "P011",
  "name": "John Carter",
  "city": "Austin",
  "age": 34,
  "gender": "male",
  "height": 1.78,
  "weight": 82
}
```

**Response** — `201 Created`
```json
{ "message": "patient created successfully" }
```

The BMI (`25.88`) and verdict (`Overweight`) are computed automatically.

---

## 📊 BMI Categories

| Verdict | BMI Range |
|---------|-----------|
| Underweight | < 18.5 |
| Normal | 18.5 – 24.9 |
| Overweight | 25 – 29.9 |
| Obese | ≥ 30 |

---

## 👤 Author

**[Sufian kanaan]** — [GitHub](https://github.com/Sufiankanaan)
