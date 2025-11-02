# E-Commerce Rating Prediction Model

AI-powered model that predicts customer ratings (1-5 stars) for e-commerce products.

## 📋 Overview

This project provides:
- **Trained ML Model** - Predicts product ratings based on customer/product features
- **Dual Database Support** - Single API server with endpoints for both SQL and NoSQL databases
- **Unified Flask API** - One server with two endpoints (/sql/predict and /nosql/predict)

**Model Performance:**
- R² Score: 0.40
- RMSE: 1.10
- Average Error: 0.78 stars
- Training Data: 50,000 reviews

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip3 install pandas numpy scikit-learn fastapi uvicorn requests
```

### 2. Train the Model
```bash
python3 train_model_sampled.py
```
**Output:** `model.pkl` (trained model)

### 3. Start Prediction API Server
```bash
python3 api.py
```
**Runs on:** http://localhost:5000

**Endpoints:**
- `POST /sql/predict` - SQL database predictions
- `POST /nosql/predict` - MongoDB predictions
- `GET /docs` - Interactive Swagger documentation
- `GET /redoc` - ReDoc documentation (alternative)

---

## 📁 Project Files

```
temp-test/
├── dataset/                       # CSV data (4M reviews, 2M customers, 20K products)
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── product_reviews.csv
│
├── train_model_sampled.py         # Train the model (uses 50K samples)
├── api.py                         # Unified Flask API server (port 5000)
├── model.pkl                      # Trained model (generated)
└── README.md                      # This file
```

---

## 🎯 How to Train the Model

### Step 1: Prepare Data
Your CSV files should be in the `dataset/` folder with these columns:

**customers.csv:**
- customer_id, name, email, gender, signup_date, country

**products.csv:**
- product_id, product_name, category, price, stock_quantity, brand

**product_reviews.csv:**
- review_id, product_id, customer_id, rating, review_text, review_date

### Step 2: Run Training
```bash
python3 train_model_sampled.py
```

**What it does:**
1. Loads CSV files from `dataset/`
2. Samples 50,000 reviews (for speed)
3. Creates features:
   - Product averages (mean_product_avg, count_product_avg)
   - Customer averages (mean_customer_avg, count_customer_avg)
   - Encodes categorical variables (category, brand, gender, country)
4. Trains Random Forest model (100 estimators)
5. Saves `model.pkl`

**Expected Output:**
```
Final dataset shape: (50000, 20)
Training set: 40000
Test set: 10000

MODEL PERFORMANCE
Mean Squared Error: 1.2149
R² Score: 0.4018
Root Mean Squared Error: 1.1022

Model and encoders saved to model.pkl
```

### Step 3: Verify Model
The model file `model.pkl` contains:
- Trained Random Forest model
- Label encoders for: category, brand, gender, country

---

## 🔌 API Server Usage

### Unified API Server

This project provides a **single API server** with two endpoints for different data sources:

**Start Server:**
```bash
python3 api.py
```

Server runs on: **http://localhost:5000**

**Interactive Documentation:**
Access Swagger UI at **http://localhost:5000/docs** for interactive API documentation and testing.
Alternatively, access ReDoc at **http://localhost:5000/redoc** for a different documentation style.

**Available Endpoints:**

1. **POST /sql/predict** - SQL Database (Relational)
   - Data Source: https://synthetic-ecommerce.onrender.com
   - Uses sequential IDs

2. **POST /nosql/predict** - NoSQL Database (MongoDB)
   - Data Source: https://synthetic-ecommerce-a31h.onrender.com
   - Uses by-field-id endpoints

3. **GET /docs** - Swagger UI (Interactive documentation)

4. **GET /redoc** - ReDoc (Alternative documentation)

5. **GET /** - API overview

6. **GET /health** - Health check

### Make Prediction Request

Both endpoints use the same simple interface - just provide product_id and customer_id:

**Request to SQL Database:**
```bash
curl -X POST http://localhost:5000/sql/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "customer_id": 1
  }'
```

**Request to NoSQL Database:**
```bash
curl -X POST http://localhost:5000/nosql/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "customer_id": 1
  }'
```

**Response (both endpoints):**
```json
{
  "status": "success",
  "database": "MongoDB",
  "product_id": 1,
  "customer_id": 1,
  "product_name": "Example Product",
  "category": "Electronics",
  "price": 450.0,
  "customer_country": "Turkey",
  "predicted_rating": 4.23,
  "product_avg_rating": 4.5,
  "product_review_count": 200,
  "customer_avg_rating": 4.2,
  "customer_review_count": 30
}
```

### Required Input Fields

Both APIs automatically fetch all product and customer data - you only need to provide:

- **product_id**: Numeric product identifier (int)
- **customer_id**: Numeric customer identifier (int)

The APIs will automatically:
1. Fetch product details (name, category, brand, price)
2. Fetch customer details (gender, country)
3. Calculate product average ratings and review counts
4. Calculate customer average ratings and review counts
5. Make the prediction using the trained model

### Example Use Cases

**1. Predict if customer will like a product (SQL):**
```python
import requests

# Using SQL database endpoint
response = requests.post('http://localhost:5000/sql/predict', json={
    "product_id": 1,
    "customer_id": 1
})

result = response.json()
prediction = result['predicted_rating']

if prediction >= 4.0:
    print(f"Recommend {result['product_name']}!")
else:
    print("Don't recommend")
```

**2. Test multiple product-customer pairs (NoSQL):**
```python
# Using NoSQL database endpoint
pairs = [
    {"product_id": 1, "customer_id": 1},
    {"product_id": 2, "customer_id": 1},
    {"product_id": 3, "customer_id": 2},
]

for pair in pairs:
    response = requests.post('http://localhost:5000/nosql/predict', json=pair)
    result = response.json()
    print(f"Product {pair['product_id']} for Customer {pair['customer_id']}: {result['predicted_rating']} stars")
```

**3. Test with curl:**
```bash
# Test SQL endpoint
curl -X POST http://localhost:5000/sql/predict \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "customer_id": 1}'

# Test NoSQL endpoint
curl -X POST http://localhost:5000/nosql/predict \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "customer_id": 1}'
```

---

## 📊 Understanding Predictions

### What the Model Predicts
**Input:** Product and customer features
**Output:** Predicted rating (1.0 - 5.0)

### Accuracy
- **Average error:** 0.78 stars
- **Best predictions:** 0.0 error (perfect!)
- **Typical range:** 0.3 - 1.5 stars error

### Example Interpretation

```
Predicted: 4.5/5.0 → Excellent match, highly recommend
Predicted: 3.8/5.0 → Good match, likely satisfied
Predicted: 3.0/5.0 → Average, mixed results expected
Predicted: 2.2/5.0 → Poor match, don't recommend
```

---

## 🔧 Troubleshooting

### Model file not found
```bash
# Retrain the model
python3 train_model_sampled.py
```

### API not responding
```bash
# Check if port 5000 is in use
lsof -ti:5000

# Kill existing process
kill -9 $(lsof -ti:5000)

# Restart
python3 api.py
```

### Unknown category/brand error
- Check valid values in the "Required Fields" section above
- Model uses default encoding (0) for unknown values

### Fetch from API fails
- **Relational DB API**: Check online at https://synthetic-ecommerce.onrender.com/docs
- **MongoDB API**: Check online at https://synthetic-ecommerce-a31h.onrender.com/docs
- Verify APIs have data (customers, products, reviews)

---

## 📈 Advanced: Retrain with More Data

**Current:** 50,000 reviews (fast, R² = 0.40)

**To use more data**, edit `train_model_sampled.py`:

```python
# Change this line:
SAMPLE_SIZE = 50000  # Current

# To:
SAMPLE_SIZE = 200000  # Better accuracy, slower training
```

**Trade-offs:**
| Sample Size | Training Time | Expected R² |
|-------------|--------------|-------------|
| 50,000 | ~2 min | 0.40 |
| 200,000 | ~10 min | 0.43-0.45 |
| 1,000,000 | ~60 min | 0.45-0.48 |
| 4,000,000 (full) | ~2-3 hours | 0.48-0.50 |

---

## 📦 Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
fastapi>=0.100.0
uvicorn>=0.23.0
requests>=2.31.0
```

Install all:
```bash
pip3 install pandas numpy scikit-learn fastapi uvicorn requests
```

---

**Happy Predicting! 🚀**

For questions or issues, check the troubleshooting section above.