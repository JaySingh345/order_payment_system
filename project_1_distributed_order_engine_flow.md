# Project 1: Distributed Order Processing Engine

---

### 🎯 Quick Pitch (How to Explain in 30 Seconds)
> *"This project is an enterprise distributed checkout engine built with **FastAPI**, **Temporal.io**, **PostgreSQL**, and **JWT**. When a user places an order, FastAPI accepts it in **15 milliseconds** and returns an instant response. In the background, Temporal workers run a crash-proof 7-step workflow that handles inventory validation, zero-CPU manager approval pauses, atomic SQL stock deductions, and email receipts."*

---

### 🔀 Step-by-Step System Logic & Execution Flow

```mermaid
flowchart TD
    A([🚀 Customer Checkout Request]) --> B

    subgraph AUTH ["🔐 1. AUTHENTICATION & SECURITY GUARD"]
        B["Customer POST /auth/login (username + password)"]
        B --> C["Passlib Bcrypt Password Check"]
        C --> D{{"Password\nvalid?"}}
        D -- No --> E["Return HTTP 401 Unauthorized"]
        D -- Yes --> F["Mint Stateless HMAC-SHA256 JWT Token\nsub = customer_id · exp = 1 hour\nReturn Token in Auth Header"]
    end

    F --> M

    subgraph TEMPORAL ["🔄 2. TEMPORAL DURABLE WORKFLOW ENGINE"]
        M["Temporal Worker accepts workflow task"]
        M --> N["Log workflow start event to disk\nEvent-sourced log: crash-proof state recovery"]

        subgraph ACT1 ["4. INVENTORY STOCK CHECK"]
            N --> O1["Execute validate_order_activity in PostgreSQL"]
            O1 --> O2{{"Stock >=\nQuantity?"}}
            O2 -- No --> O3(["❌ Order Failed: Out of Stock"])
            O2 -- Yes --> P
        end

        subgraph ACT2 ["5. ZERO-CPU HUMAN APPROVAL PAUSE"]
            P["workflow.wait_condition()\nFreezes state in Temporal event log\n0% CPU & 0 DB connections held during wait"]
            P --> Q1{{"Manager Signal\nReceived?"}}
            Q1 -- Timeout (1h) --> Q2(["❌ Order Cancelled: Approval Timeout"])
            Q1 -- Approved --> R
        end

        subgraph ACT3 ["6. PAYMENT & ATOMIC CHECKOUT"]
            R["Execute process_payment_activity\nCharge customer card → mint payment txn UUID"]
            R --> S["Execute reserve_inventory_activity in PostgreSQL"]
            S --> T["Atomic SQL: SELECT ... FOR UPDATE\nRow lock stock row → deduct quantity → commit\nThread-safe: eliminates flash sale race conditions"]
        end

        T --> U

        subgraph ACT4 ["7. FULFILLMENT & NOTIFICATION"]
            U["Execute ship_order_activity → Mint tracking UUID"]
            U --> V["Execute save_order_activity → Update status to COMPLETED in DB"]
            V --> W["Execute send_email_activity → Dispatch HTML receipt via SMTP TLS"]
        end

        W --> X(["✅ ORDER COMPLETED SUCCESSFULLY"])
    end

    subgraph RETRIES ["🔁 RETRY POLICY & EXCEPTION HANDLING"]
        O1 & R & S & U & V -- Transient DB Lock / Network Error --> RET["Temporal RetryPolicy Triggered\nExponential Backoff: 1s, 2s, 4s, 8s (max 5x)"]
        RET --> O1
    end
```

---

### 💡 4 Key Takeaways to Highlight to the Audience
1. **15ms Response Speed**: Customers receive instant checkout confirmation while heavy background processing runs in Temporal queues.
2. **Crash-Proof Durability**: Temporal records every event to disk, resuming execution automatically if server pods restart mid-checkout.
3. **Zero-CPU Execution Pauses**: Pauses high-value orders for manager approval without consuming CPU memory or DB connections.
4. **Atomic Stock Locking**: SQL `SELECT ... FOR UPDATE` row locks eliminate stock overselling during flash sales.
