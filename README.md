# ZeroWasteByte Foundation - Full-Stack Food Rescue Platform

A production-ready full-stack web application connecting PG/hostel owners who have surplus food directly with local NGOs in Bengaluru. Built with **FastAPI**, **MongoDB**, and modern responsive web technologies.

---

## 🏗️ Architecture Overview

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13) with asynchronous request handling via `Motor` and `uvicorn`.
- **Database**: [MongoDB](https://www.mongodb.com/) (`zerowaste_db`) running on `localhost:27017`.
- **Frontend**: Responsive, modern glassmorphic UI with Tailwind CSS, FontAwesome 6, Inter typography, Dark/Light mode, live MongoDB state synchronization, and dynamic counters.
- **API Documentation**: Automated interactive Swagger UI available at `http://localhost:8000/docs`.

---

## 🚀 Quick Start

### 1. Start the Full-Stack Server
Double-click `start.bat` or run:

```powershell
.venv\Scripts\python.exe server.py
```

Open your browser at:
- **Application**: [http://localhost:8000](http://localhost:8000) (or via Live Server on port 5501)
- **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🍃 MongoDB Collections & Schema

1. **`users`**:
   - `id`: String identifier (e.g. `pg123`, `ngo456`)
   - `name`: Organization or person name
   - `email`: Contact email
   - `role`: `'PG Owner'` or `'NGO'`
   - `phone`: Contact number
   - `address`: Location / Area in Bengaluru

2. **`listings`** (Surplus Food Items):
   - `id`: Unique listing ID
   - `pgId`: ID of donating PG
   - `pgName`: Name of donor
   - `foodName`: Food name & description
   - `quantity`: Number of people fed
   - `pickupTime`: Pickup deadline
   - `location`: Pickup address
   - `photoFilename`: Attached photo URL / filename
   - `status`: `'Available'` or `'Claimed'`
   - `claimedByNgoId`: NGO claiming the package
   - `claimedByNgoName`: Name of claiming NGO

3. **`requests`** (NGO Essential Supplies):
   - `id`: Unique request ID
   - `ngoId`: Requesting NGO ID
   - `ngoName`: NGO name
   - `itemName`: Requested item (e.g., containers, delivery bags)
   - `quantity`: Quantity needed
   - `status`: `'Needed'` or `'Fulfilled'`
   - `fulfilledByPgId`: Donor pledging the items
   - `fulfilledByPgName`: Donor name

4. **`donations`**:
   - `id`: Donation ID
   - `transactionId`: Unique transaction tracking code
   - `donorName`: Contributor name
   - `amount`: Amount in INR
   - `paymentMethod`: UPI, Card, NetBanking
   - `targetItem`: Specific sponsored item (optional)
   - `status`: `'Completed'`

5. **`contacts`**:
   - Submissions from the "Get in Touch" form with full name, email, subject, and message.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check & MongoDB status |
| `POST` | `/api/auth/register` | Register new PG Owner or NGO |
| `POST` | `/api/auth/login` | Login with JWT token generation |
| `GET` | `/api/auth/me` | Fetch currently logged in user profile |
| `GET` | `/api/listings` | Query surplus listings (supports `status`, `pg_id`, `ngo_id`) |
| `POST` | `/api/listings` | Create new surplus food listing |
| `PUT` | `/api/listings/{id}/claim` | Claim an available surplus food item (NGO) |
| `DELETE` | `/api/listings/{id}` | Delete a food listing |
| `GET` | `/api/requests` | Query supply requests (supports `status`, `ngo_id`, `pg_id`) |
| `POST` | `/api/requests` | Broadcast new supply request (NGO) |
| `PUT` | `/api/requests/{id}/pledge` | Pledge to fulfill supply request (PG Owner) |
| `POST` | `/api/upload` | Upload food photo |
| `POST` | `/api/donations` | Record monetary / item donation |
| `GET` | `/api/donations/summary`| Total funds raised & recent donors |
| `POST` | `/api/contact` | Submit contact form message |
| `GET` | `/api/stats` | Real-time impact metrics from database |
