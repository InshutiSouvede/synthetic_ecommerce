from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import pickle
import requests

# Pydantic models for request/response
class PredictionRequest(BaseModel):
    product_id: int = Field(..., description="Numeric product identifier")
    customer_id: int = Field(..., description="Numeric customer identifier")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_id": 1,
                    "customer_id": 1
                }
            ]
        }
    }

class PredictionResponse(BaseModel):
    status: str
    database: str
    product_id: int
    customer_id: int
    product_name: str
    category: str
    price: float
    customer_country: str
    predicted_rating: float
    product_avg_rating: float
    product_review_count: int
    customer_avg_rating: float
    customer_review_count: int

class ErrorResponse(BaseModel):
    error: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    databases: dict

# FastAPI app with built-in OpenAPI/Swagger
app = FastAPI(
    title="E-Commerce Rating Prediction API",
    description="AI-powered API that predicts customer ratings (1-5 stars) for e-commerce products. Supports both SQL and NoSQL databases.",
    version="1.0.0",
    contact={"name": "API Support"}
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Remote API URLs
SQL_API_URL = "https://synthetic-ecommerce.onrender.com"
NOSQL_API_URL = "https://synthetic-ecommerce-a31h.onrender.com"

# Load the model and encoders
print("Loading model...")
with open('model.pkl', 'rb') as f:
    model, encoders = pickle.load(f)
print("Model loaded successfully!")

# ============================================================================
# SQL DATABASE FUNCTIONS (Relational DB)
# ============================================================================

def fetch_product_sql(product_id):
    """Fetch product from SQL API"""
    try:
        response = requests.get(f"{SQL_API_URL}/products/{product_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching product from SQL: {e}")
        return None

def fetch_customer_sql(customer_id):
    """Fetch customer from SQL API"""
    try:
        response = requests.get(f"{SQL_API_URL}/customers/{customer_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching customer from SQL: {e}")
        return None

def fetch_product_reviews_sql(product_id):
    """Fetch all reviews for a product from SQL API"""
    try:
        response = requests.get(f"{SQL_API_URL}/reviews/")
        if response.status_code == 200:
            all_reviews = response.json()
            return [r for r in all_reviews if r['product_id'] == product_id]
        return []
    except Exception as e:
        print(f"Error fetching product reviews from SQL: {e}")
        return []

def fetch_customer_reviews_sql(customer_id):
    """Fetch all reviews by a customer from SQL API"""
    try:
        response = requests.get(f"{SQL_API_URL}/reviews/")
        if response.status_code == 200:
            all_reviews = response.json()
            return [r for r in all_reviews if r['customer_id'] == customer_id]
        return []
    except Exception as e:
        print(f"Error fetching customer reviews from SQL: {e}")
        return []

# ============================================================================
# NOSQL DATABASE FUNCTIONS (MongoDB)
# ============================================================================

def fetch_product_nosql(product_id):
    """Fetch product from NoSQL API using numeric product_id"""
    try:
        response = requests.get(f"{NOSQL_API_URL}/products/by-product-id/{product_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching product from NoSQL: {e}")
        return None

def fetch_customer_nosql(customer_id):
    """Fetch customer from NoSQL API using numeric customer_id"""
    try:
        response = requests.get(f"{NOSQL_API_URL}/customers/by-customer-id/{customer_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching customer from NoSQL: {e}")
        return None

def fetch_product_reviews_nosql(product_id):
    """Fetch all reviews for a product from NoSQL API"""
    try:
        response = requests.get(f"{NOSQL_API_URL}/product-reviews/product/{product_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching product reviews from NoSQL: {e}")
        return []

def fetch_customer_reviews_nosql(customer_id):
    """Fetch all reviews by a customer from NoSQL API"""
    try:
        response = requests.get(f"{NOSQL_API_URL}/product-reviews/customer/{customer_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching customer reviews from NoSQL: {e}")
        return []

# ============================================================================
# SHARED PREDICTION LOGIC
# ============================================================================

def make_prediction(product, customer, product_reviews, customer_reviews, db_type):
    """Shared prediction logic for both SQL and NoSQL"""

    # Calculate product statistics
    if product_reviews:
        product_ratings = [r['rating'] for r in product_reviews]
        mean_product_avg = sum(product_ratings) / len(product_ratings)
        count_product_avg = len(product_ratings)
    else:
        mean_product_avg = 3.0  # Default
        count_product_avg = 0

    # Calculate customer statistics
    if customer_reviews:
        customer_ratings = [r['rating'] for r in customer_reviews]
        mean_customer_avg = sum(customer_ratings) / len(customer_ratings)
        count_customer_avg = len(customer_ratings)
    else:
        mean_customer_avg = 3.0  # Default
        count_customer_avg = 0

    # Prepare input data for prediction
    input_data = {
        'price': product.get('price', 0.0),
        'category': product.get('category', ''),
        'brand': product.get('brand', ''),
        'gender': customer.get('gender', ''),
        'country': customer.get('country', ''),
        'mean_product_avg': mean_product_avg,
        'count_product_avg': count_product_avg,
        'mean_customer_avg': mean_customer_avg,
        'count_customer_avg': count_customer_avg
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Encode categorical columns
    categorical_mappings = {
        'category': encoders['category'],
        'brand': encoders['brand'],
        'gender': encoders['gender'],
        'country': encoders['country']
    }

    for col, encoder in categorical_mappings.items():
        if input_df[col].iloc[0] != '' and input_df[col].iloc[0] is not None:
            try:
                input_df[f'{col}_encoded'] = encoder.transform(input_df[col])
            except ValueError:
                input_df[f'{col}_encoded'] = 0
        else:
            input_df[f'{col}_encoded'] = 0

    # Prepare features in the same order as training
    features = ['price', 'category_encoded', 'brand_encoded', 'gender_encoded',
               'country_encoded', 'mean_product_avg', 'count_product_avg',
               'mean_customer_avg', 'count_customer_avg']

    # Make prediction
    prediction = model.predict(input_df[features])
    predicted_rating = float(prediction[0])

    # Clamp between 1 and 5
    predicted_rating = max(1.0, min(5.0, predicted_rating))

    return {
        'status': 'success',
        'database': db_type,
        'product_id': product.get('product_id'),
        'customer_id': customer.get('customer_id'),
        'product_name': product.get('product_name'),
        'category': product.get('category'),
        'price': product.get('price'),
        'customer_country': customer.get('country'),
        'predicted_rating': round(predicted_rating, 2),
        'product_avg_rating': round(mean_product_avg, 2),
        'product_review_count': count_product_avg,
        'customer_avg_rating': round(mean_customer_avg, 2),
        'customer_review_count': count_customer_avg
    }

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get(
    "/",
    tags=["Health"],
    summary="API Overview",
    description="Get API information and available endpoints"
)
def home():
    return {
        'message': 'E-Commerce Rating Prediction API (Unified)',
        'endpoints': {
            '/sql/predict': {
                'method': 'POST',
                'description': 'Predict rating using SQL database API',
                'database': 'Relational Database',
                'api_url': SQL_API_URL,
                'required_fields': ['product_id', 'customer_id'],
                'example': {
                    'product_id': 1,
                    'customer_id': 1
                }
            },
            '/nosql/predict': {
                'method': 'POST',
                'description': 'Predict rating using NoSQL database API',
                'database': 'MongoDB',
                'api_url': NOSQL_API_URL,
                'required_fields': ['product_id', 'customer_id'],
                'example': {
                    'product_id': 1,
                    'customer_id': 1
                }
            },
            '/health': {
                'method': 'GET',
                'description': 'Check API health'
            }
        }
    }

@app.get(
    "/health",
    tags=["Health"],
    response_model=HealthResponse,
    summary="Health Check",
    description="Check API health status"
)
def health():
    return {
        'status': 'healthy',
        'model_loaded': True,
        'databases': {
            'sql': SQL_API_URL,
            'nosql': NOSQL_API_URL
        }
    }

@app.post(
    "/sql/predict",
    tags=["Predictions"],
    response_model=PredictionResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Product or customer not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Predict Rating (SQL Database)",
    description="Predict product rating using SQL database API. Fetches product and customer data from relational database."
)
def predict_sql(request: PredictionRequest):
    try:
        product_id = request.product_id
        customer_id = request.customer_id

        # Fetch data from SQL API
        print(f"[SQL] Fetching data for product_id={product_id}, customer_id={customer_id}")

        product = fetch_product_sql(product_id)
        customer = fetch_customer_sql(customer_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f'Product {product_id} not found in SQL database'
            )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f'Customer {customer_id} not found in SQL database'
            )

        product_reviews = fetch_product_reviews_sql(product_id)
        customer_reviews = fetch_customer_reviews_sql(customer_id)

        # Make prediction
        result = make_prediction(product, customer, product_reviews, customer_reviews, 'SQL')
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/nosql/predict",
    tags=["Predictions"],
    response_model=PredictionResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Product or customer not found"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Predict Rating (NoSQL Database)",
    description="Predict product rating using NoSQL database API. Fetches product and customer data from MongoDB."
)
def predict_nosql(request: PredictionRequest):
    try:
        product_id = request.product_id
        customer_id = request.customer_id

        # Fetch data from NoSQL API
        print(f"[NoSQL] Fetching data for product_id={product_id}, customer_id={customer_id}")

        product = fetch_product_nosql(product_id)
        customer = fetch_customer_nosql(customer_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f'Product {product_id} not found in NoSQL database'
            )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f'Customer {customer_id} not found in NoSQL database'
            )

        product_reviews = fetch_product_reviews_nosql(product_id)
        customer_reviews = fetch_customer_reviews_nosql(customer_id)

        # Make prediction
        result = make_prediction(product, customer, product_reviews, customer_reviews, 'NoSQL')
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn

    print("\n" + "="*70)
    print("E-COMMERCE RATING PREDICTION API (UNIFIED)")
    print("="*70)
    print("Endpoints:")
    print("  - GET  /              : API overview")
    print("  - GET  /health        : Health check")
    print("  - GET  /docs          : Swagger documentation (Interactive)")
    print("  - GET  /redoc         : ReDoc documentation (Alternative)")
    print("  - POST /sql/predict   : Predict rating (SQL database)")
    print("  - POST /nosql/predict : Predict rating (NoSQL database)")
    print("="*70)
    print(f"\nSQL Database:   {SQL_API_URL}")
    print(f"NoSQL Database: {NOSQL_API_URL}")
    print("\nStarting server on http://localhost:8000")
    print("Swagger UI available at http://localhost:8000/docs")
    print("ReDoc available at http://localhost:8000/redoc")
    print("="*70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
