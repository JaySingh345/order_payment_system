# Setup Guide

This guide explains how to configure and run the **Order Processing System** locally.

---

# Prerequisites

Ensure the following software is installed before proceeding.

| Software     | Recommended Version |
| ------------ | ------------------- |
| Python       | 3.11 or later       |
| PostgreSQL   | Latest              |
| Git          | Latest              |
| Temporal CLI | Latest              |

---

# Clone the Repository

```bash
git clone https://github.com/JaySingh345/order_payment_system.git

cd order_payment_system
```

---

# Create a Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate the virtual environment

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# Install Project Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not available, install the dependencies manually.

```bash
pip install fastapi uvicorn temporalio sqlalchemy psycopg2-binary python-dotenv python-jose[cryptography] passlib[bcrypt] python-multipart
```

---

# PostgreSQL Setup

Create a PostgreSQL database.

```sql
CREATE DATABASE order_payment_db;
```

---

# Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://postgres:<your_password>@localhost:5432/order_payment_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

EMAIL_USER=your_email@gmail.com

EMAIL_PASS=your_email_app_password
```

Replace the placeholder values with your own credentials.

---

# Create Database Tables

Run the following command from the project root.

```bash
python -m database.create_tables
```

This will create the required database tables:

* Customers
* Orders
* Inventory

---

# Start the Temporal Development Server

Open a new terminal.

Run:

```bash
temporal server start-dev
```

By default:

| Service         | Port |
| --------------- | ---- |
| Temporal Server | 7233 |
| Temporal UI     | 8233 |

Temporal UI can be accessed at

```text
http://localhost:8233
```

---

# Start the Temporal Worker

Open another terminal.

Activate the virtual environment and run:

```bash
python -m workflow_service.worker.order_worker
```

The worker listens to the configured task queue and executes workflow activities.

---

# Start the FastAPI Application

Open another terminal.

Activate the virtual environment and run:

```bash
uvicorn fast_api.api:app --reload
```

FastAPI will be available at

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Running the Application

## Step 1 - Register

Use the `/register` endpoint to create a customer account.

Example

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
}
```

---

## Step 2 - Login

Use the `/login` endpoint.

Enter your credentials.

After successful authentication, a JWT access token will be returned.

Example response

```json
{
    "access_token": "<JWT_TOKEN>",
    "token_type": "bearer"
}
```

---

## Step 3 - Authorize Swagger

Click the **Authorize** button in Swagger UI.

Enter:

* Username → Your registered email
* Password → Your registered password

Swagger will automatically retrieve and attach the JWT access token to protected API requests.

---

## Step 4 - Add Inventory

Before creating an order, add products to the inventory using the inventory API.

Example

```json
{
    "product_name": "charger",
    "quantity": 20,
    "amount": 500
}
```

---

## Step 5 - Create an Order

Create an order using the authenticated endpoint.

Example request

```json
{
    "items": [
        {
            "name": "charger",
            "quantity": 2
        }
    ],
    "address": "Noida, India"
}
```

Customer ID and Email are automatically extracted from the authenticated user's JWT token.

---

## Step 6 - Monitor the Workflow

Open the Temporal UI.

```text
http://localhost:8233
```

Select the running workflow.

You can monitor:

* Workflow execution history
* Activity execution
* Retry attempts
* Workflow events
* Input and output payloads
* Signals

---

## Step 7 - Approve the Order

After inventory validation, the workflow pauses while waiting for an approval signal.

In the Temporal UI:

1. Open the running workflow.
2. Navigate to the **Signals** section.
3. Enter the signal name:

```text
approve_order
```

4. Submit the signal.

The workflow resumes automatically and continues with:

* Payment Processing
* Inventory Reservation
* Shipment
* Order Persistence
* Email Notification

---

# Expected Workflow

```text
Customer Login
      │
      ▼
JWT Authentication
      │
      ▼
Create Order
      │
      ▼
Temporal Workflow Started
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
Save Order
      │
      ▼
Send Confirmation Email
      │
      ▼
Workflow Completed
```

---

# Monitoring

Temporal UI provides:

* Workflow History
* Activity History
* Event Timeline
* Signals
* Retry Attempts
* Workflow Inputs
* Workflow Outputs
* Execution Duration

---

# Stopping the Application

Stop FastAPI

```text
Ctrl + C
```

Stop Worker

```text
Ctrl + C
```

Stop Temporal Server

```text
Ctrl + C
```

---

# Troubleshooting

## Database Connection Issues

* Verify PostgreSQL is running.
* Verify the `DATABASE_URL` in `.env`.
* Ensure the database exists.

---

## Authentication Issues

* Ensure the user is registered.
* Verify the JWT token has not expired.
* Re-login to generate a new access token.

---

## Workflow Not Starting

* Verify the Temporal Server is running.
* Verify the Worker is running.
* Ensure the task queue names match.

---

## Email Not Sending

* Verify `EMAIL_USER` and `EMAIL_PASS` in `.env`.
* If using Gmail, use an App Password instead of your account password.

---

# Additional Resources

* Swagger UI

```text
http://127.0.0.1:8000/docs
```

* Temporal UI

```text
http://localhost:8233
```

For a complete overview of the project architecture, workflow, and implementation details, refer to the `README.md` file.
