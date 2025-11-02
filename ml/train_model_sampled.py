import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Set sample size for faster training
SAMPLE_SIZE = 50000  # Use 50k reviews for training

print("Loading datasets...")
# Load all datasets
customers_df = pd.read_csv('dataset/customers.csv')
products_df = pd.read_csv('dataset/products.csv')
orders_df = pd.read_csv('dataset/orders.csv')
order_items_df = pd.read_csv('dataset/order_items.csv')
reviews_df = pd.read_csv('dataset/product_reviews.csv')

print(f"Total reviews: {len(reviews_df)}")
print(f"Sampling {SAMPLE_SIZE} reviews for training...")

# Sample the reviews for faster training
reviews_df_sample = reviews_df.sample(n=min(SAMPLE_SIZE, len(reviews_df)), random_state=42)

# Merge relevant data
product_reviews = reviews_df_sample.merge(products_df, on='product_id')
product_reviews = product_reviews.merge(customers_df, on='customer_id')

# Calculate additional features (using full dataset for better statistics)
product_avg_ratings = reviews_df.groupby('product_id')['rating'].agg(['mean', 'count']).reset_index()
product_avg_ratings = product_avg_ratings.rename(columns={'mean': 'mean_product_avg', 'count': 'count_product_avg'})

customer_avg_ratings = reviews_df.groupby('customer_id')['rating'].agg(['mean', 'count']).reset_index()
customer_avg_ratings = customer_avg_ratings.rename(columns={'mean': 'mean_customer_avg', 'count': 'count_customer_avg'})

# Prepare final dataset
final_df = product_reviews.merge(product_avg_ratings, on='product_id')
final_df = final_df.merge(customer_avg_ratings, on='customer_id')

print(f"Final dataset shape after sampling and merging: {final_df.shape}")

# Feature engineering - Create separate encoder for each categorical column
le_category = LabelEncoder()
le_brand = LabelEncoder()
le_gender = LabelEncoder()
le_country = LabelEncoder()

final_df['category_encoded'] = le_category.fit_transform(final_df['category'])
final_df['brand_encoded'] = le_brand.fit_transform(final_df['brand'])
final_df['gender_encoded'] = le_gender.fit_transform(final_df['gender'])
final_df['country_encoded'] = le_country.fit_transform(final_df['country'])

# Select features for model
features = ['price', 'category_encoded', 'brand_encoded', 'gender_encoded',
            'country_encoded', 'mean_product_avg', 'count_product_avg',
            'mean_customer_avg', 'count_customer_avg']

X = final_df[features]
y = final_df['rating']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# Initialize and train the model
print("\nTraining Random Forest model...")
model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Make predictions on test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'\n{"="*50}')
print(f'MODEL PERFORMANCE')
print(f'{"="*50}')
print(f'Mean Squared Error: {mse:.4f}')
print(f'R² Score: {r2:.4f}')
print(f'Root Mean Squared Error: {np.sqrt(mse):.4f}')
print(f'{"="*50}')

# Save encoders and model - each encoder is separate
encoders = {
    'category': le_category,
    'brand': le_brand,
    'gender': le_gender,
    'country': le_country
}

joblib.dump((model, encoders), 'model.pkl', compress=3)

print('\nModel and encoders saved to model.pkl (with compression)')
print(f'\nEncoder details:')
print(f'- Categories: {len(le_category.classes_)} unique values')
print(f'- Brands: {len(le_brand.classes_)} unique values')
print(f'- Genders: {len(le_gender.classes_)} unique values')
print(f'- Countries: {len(le_country.classes_)} unique values')

# Print sample predictions
print(f'\n{"="*50}')
print('SAMPLE PREDICTIONS')
print(f'{"="*50}')
sample_indices = np.random.choice(len(X_test), 5, replace=False)
for idx in sample_indices:
    actual = y_test.iloc[idx]
    predicted = y_pred[idx]
    print(f'Actual: {actual:.2f} | Predicted: {predicted:.2f} | Difference: {abs(actual - predicted):.2f}')
