# FastAPI E-commerce Backend

A **FastAPI** project implementing full **CRUD operations** for an e-commerce system with the following entities:

- Customers  
- Products  
- Orders  
- Order Items  
- Product Reviews  

The project supports switching between **local PostgreSQL** and a **shared Neon database** connection.

---

## Features

- Full CRUD operations for all entities  
- PostgreSQL database support (local or shared)  
- SQLAlchemy ORM for model management  
- Clean, modular architecture (separated routers, models, schemas, and database)  
- Environment-based configuration using `.env`  
- Automatic table creation on startup  


---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/InshutiSouvede/synthetic_ecommerce.git
cd synthetic_ecommerce
```

### 2. Create a Virtual Environment [optional]
```bash
python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables

### 5. Run the Server
```bash
alembic upgrade head  # needed only if connecting to neon db
uvicorn app.main:app --reload

```
Then open your browser at:

http://127.0.0.1:8000/docs


