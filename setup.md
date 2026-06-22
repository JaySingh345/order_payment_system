# Order Payment System – Setup

## Overview

This project demonstrates an Order Payment System built using:

* Python
* Temporal
* Temporal Python SDK
* FastAPI
* PostgreSQL
* Temporal UI

The system processes orders through the following stages:

1. Validate Order
2. Reserve Inventory
3. Process Payment
4. Ship Order
5. Send Email

---

# Prerequisites

Ensure the following are installed:

* Python 3.11+
* PostgreSQL
* Temporal CLI
* Git

---

# Clone Repository

```bash
git clone <https://github.com/JaySingh345/order_payment_system>
cd order_payment_system
```

---

# Create Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate environment:

```bash
.venv\Scripts\activate
```

---

# Install Dependencies


```bash
pip install temporalio fastapi uvicorn sqlalchemy psycopg2-binary
```

---

# PostgreSQL Setup

Create database:

```sql
CREATE DATABASE order_payment_db;
```

Update database connection inside:

```
database/database.py
```

Example:

```python
DATABASE_URL = "postgresql://postgres:<password>@localhost:5432/order_payment_db"
```

---

# Create Database Tables

From the project root:

```bash
python -m database.create_tables
```

This creates the Orders table.

---

# Start Temporal Development Server

Open a new terminal:

```bash
temporal server start-dev
```

Default ports:

* Temporal Server: 7233
* Temporal UI: 8233

Temporal UI:

```
http://localhost:8233
```

---

# Start Worker

Open another terminal:

```bash
python -m workflow_service.worker.order_worker
```

The worker polls the task queue and executes workflows and activities.

---

# Start FastAPI Server

Open another terminal:

```bash
uvicorn fast_api.api:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Create Order

POST

```
/orders
```

Sample Request:

```json
{
  "order_id": 1,
  "customer_id": 101,
  "amount": 400,
  "items": [
    {
      "name": "product",
      "quantity": 1
    }
  ],
  "address": "city",
  "email": "name@example.com"
}
```

---

## Get All Orders

GET

```
/orders
```

Returns all orders stored in PostgreSQL.

---

# Project Structure

```
order_payment_system
│
├── fast_api
│   ├── api.py
│   ├── schemas.py
│
├── database
│   ├── database.py
│   ├── models.py
│   ├── create_tables.py
│
├── shared
│   └── models.py
│
├── workflow_service
│   ├── activities
│   ├── workflows
│   └── worker
│
└── starter.py
```

---

# Execution Flow

```
Client
   ↓
FastAPI
   ↓
Store Order in PostgreSQL
   ↓
Start OrderWorkflow
   ↓
Temporal Server
   ↓
Worker
   ↓
Validate Order
   ↓
Reserve Inventory
   ↓
Process Payment
   ↓
Ship Order
   ↓
Send Email
```

---

# Monitoring

Temporal UI:

```
http://localhost:8233
```

Features:

* Workflow execution history
* Activity execution status
* Retry attempts
* Execution timeline
* Workflow details

---

# Stopping Services

Stop FastAPI:

```
Ctrl + C
```

Stop Worker:

```
Ctrl + C
```

Stop Temporal Server:

```
Ctrl + C
```

---

# Technologies Used

* Python
* FastAPI
* Temporal
* Temporal Python SDK
* PostgreSQL
* SQLAlchemy
* Uvicorn

---

# Source Repository

```
<https://github.com/JaySingh345/order_payment_system>
```
