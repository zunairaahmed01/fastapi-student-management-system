# 🎓 FastAPI Student Management System

A lightweight, fast, and scalable **Student Management API** built using **FastAPI**. 
This project includes full **CRUD operations**, **data validation**, **sorting**, 
and **computed fields** like **BMI**, with data persistence using a JSON file.

---

## 🚀 Features

- ✅ Create, Read, Update, Delete (CRUD) student records
- 🧪 Strong data validation using **Pydantic**
- 📊 BMI computed automatically based on height and weight
- 🔎 Sort students by age, gender, weight, or height
- 🔒 Validations for name, age, gender, DOB, email, and more
- 📂 Data persistence using `Students.json`
- ⚡ Powered by **FastAPI** for high performance

---

## 📁 Project Structure
students/
├── Students.json # Data store
├── README.md # Project documentation
├── pyproject.toml # Project configuration
├── poetry.lock # Dependency lock file
└── src/
└── students/
├── main.py # Main FastAPI app
└── init.py


---

## 📦 Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

Install dependencies using:

```bash
pip install fastapi uvicorn pydantic

Or if you're using Poetry:
poetry install
Run the FastAPI server:
 - poetry run st
