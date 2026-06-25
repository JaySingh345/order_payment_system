# Order Processing System using FastAPI, Temporal & PostgreSQL

## Overview

This project demonstrates the implementation of a reliable and fault-tolerant **Order Processing System** using **FastAPI**, **Temporal**, and **PostgreSQL**.

The application simulates the complete lifecycle of an order placed on an e-commerce platform. Instead of executing all business logic within a single API request, long-running business processes are delegated to **Temporal Workflows**, providing durability, automatic retries, failure recovery, and workflow state persistence.

The project also implements **JWT-based Authentication**, allowing users to securely register, log in, and access only their own order information while protecting all sensitive APIs.

This repository serves as both a learning resource for developers exploring Temporal and a reference implementation for building workflow-driven backend services.

---

# Features

* User Registration
* User Login with JWT Authentication
* Password Hashing using bcrypt
* JWT Authorization for Protected APIs
* Automatic Customer Identification using JWT
* Order Creation through FastAPI
* Inventory Validation
* Manual Order Approval using Temporal Signals
* Payment Processing
* Inventory Reservation
* Shipment Tracking ID Generation
* Order Persistence using PostgreSQL
* Email Notification
* Inventory Management APIs
* Workflow Monitoring through Temporal UI

---

# Order Processing Workflow

```text
Customer Registration
        │
        ▼
Customer Login
        │
        ▼
Generate JWT Token
        │
        ▼
Authenticate Request
        │
        ▼
Create Order
        │
        ▼
Start Temporal Workflow
        │
        ▼
Validate Inventory
        │
        ▼
Wait for Approval Signal
        │
        ▼
Process Payment
        │
        ▼
Reserve Inventory
        │
        ▼
Generate Tracking ID
        │
        ▼
Save Order in PostgreSQL
        │
        ▼
Send Confirmation Email
        │
        ▼
Workflow Completed
```

---

# Project Architecture

```text
                              +-----------------------+
                              |      Client/User      |
                              +-----------+-----------+
                                          |
                                          ▼
                                 +------------------+
                                 |     FastAPI      |
                                 +------------------+
                                  │              │
                     JWT Authentication     Start Workflow
                                  │              │
                                  ▼              ▼
                          +-----------------------------+
                          |      Temporal Server        |
                          +-----------------------------+
                                         │
                                         ▼
                                +----------------+
                                | Temporal Worker|
                                +----------------+
                                         │
     -------------------------------------------------------------------------
     │              │                │              │               │
     ▼              ▼                ▼              ▼               ▼
Validate      Wait for Signal    Payment      Reserve Stock    Ship Order
                                         │
                                         ▼
                               Save Order to PostgreSQL
                                         │
                                         ▼
                               Send Confirmation Email
```

---

# Technology Stack

| Category               | Technology       |
| ---------------------- | ---------------- |
| Language               | Python           |
| API Framework          | FastAPI          |
| Workflow Engine        | Temporal         |
| Database               | PostgreSQL       |
| ORM                    | SQLAlchemy       |
| Authentication         | JWT              |
| Password Hashing       | Passlib + bcrypt |
| Data Validation        | Pydantic         |
| Email Service          | SMTP             |
| ASGI Server            | Uvicorn          |
| Environment Management | python-dotenv    |

---

# Key Concepts Demonstrated

* Durable Workflow Orchestration
* Long Running Business Processes
* Activities and Workers
* Retry Policies
* Workflow Signals
* Human Approval Workflow
* JWT Authentication & Authorization
* Password Hashing
* REST API Development
* SQLAlchemy ORM
* PostgreSQL Integration
* Environment Variable Management
* Inventory Management
* Database Transactions

---

# Authentication Flow

All protected APIs require JWT authentication.

```text
Register
    │
    ▼
Login
    │
    ▼
Receive JWT Access Token
    │
    ▼
Authorize in Swagger UI
    │
    ▼
Access Protected APIs
```

Customer information such as **Customer ID** and **Email Address** is automatically extracted from the JWT token and therefore does not need to be supplied while placing an order.

---

# Workflow Signals

One of the key features demonstrated by this project is the use of **Temporal Signals**.

After validating the inventory, the workflow pauses execution and waits for an **Order Approval Signal**.

Once the signal is sent from the Temporal UI, the workflow resumes automatically and continues processing the order.

This demonstrates how Temporal can coordinate long-running workflows that require human interaction without blocking application resources.

---

# REST APIs

| Method | Endpoint                  | Description                      | Authentication |
| ------ | ------------------------- | -------------------------------- | -------------- |
| POST   | `/register`               | Register a new customer          | No             |
| POST   | `/login`                  | Login and receive JWT            | No             |
| POST   | `/api/orders`             | Create a new order               | Yes            |
| GET    | `/api/orders/users`       | View logged-in customer's orders | Yes            |
| GET    | `/api/orders`             | View all orders                  | Yes            |
| GET    | `/api/orders/id/{id}`     | Get order by Order ID            | Yes            |
| GET    | `/api/orders/mail/{mail}` | Get orders by Email              | Yes            |
| GET    | `/api/inventory/quantity` | View inventory                   | Yes            |
| POST   | `/api/inventory/add`      | Add inventory                    | Yes            |
| DELETE | `/api/inventory/delete`   | Remove inventory                 | Yes            |

---

# Project Structure

```text
order_payment_system/
│
├── auth/
│   ├── hashing.py
│   ├── oauth.py
│   └── token.py
│
├── database/
│   ├── create_tables.py
│   ├── database.py
│   └── models.py
│
├── fast_api/
│   ├── api.py
│   └── schemas.py
│
├── shared/
│   └── models.py
│
├── workflow_service/
│   ├── activities/
│   ├── workflows/
│   └── worker/
│
├── .env
├── requirements.txt
├── README.md
└── SETUP.md
```

---

# Monitoring

The project can be monitored through the Temporal UI.

Default URL:

```text
http://localhost:8233
```

Temporal UI allows you to inspect:

* Workflow Execution History
* Activity Execution Status
* Workflow Signals
* Retry Attempts
* Event Timeline
* Workflow Inputs and Outputs
* Workflow State
* Workflow Duration

---

# Future Enhancements

* Role-Based Access Control (Admin & Customer)
* Payment Gateway Integration (Stripe, Razorpay)
* Order Cancellation Workflow
* Refund Workflow
* Shipment Provider Integration
* Docker & Docker Compose Support
* CI/CD Pipeline
* Unit & Integration Testing
* Monitoring & Logging
* Workflow Versioning
* Notification Service (Email, SMS, Push)
* Distributed Worker Deployment
* Multiple Task Queues
* Order Status Tracking API

---

# Learning Objectives

This project demonstrates how modern backend applications can combine REST APIs, authentication, relational databases, and durable workflow orchestration to build reliable distributed systems.

It covers several important software engineering concepts, including workflow orchestration, asynchronous processing, JWT authentication, SQLAlchemy ORM, database persistence, dependency injection, environment configuration, and fault-tolerant application design.

---

# Setup

For complete installation, configuration, and execution instructions, refer to **SETUP.md**.

The setup guide includes:

* Installing prerequisites
* Configuring PostgreSQL
* Setting up environment variables
* Running the Temporal Server
* Starting the Worker
* Launching the FastAPI application
* Registering and logging in users
* Using Swagger UI
* Monitoring workflows through Temporal UI
