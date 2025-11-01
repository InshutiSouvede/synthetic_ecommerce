# E-Commerce SQL API Project

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the dataset
```bash
python3 scripts/setup_data.py
```

This downloads ~2GB of CSV files from Google Drive to `./data/csv/`

### 4. Verify setup
Check that `./data/csv/` contains:
- customers.csv (146.3 MB)
- orders.csv (437.7 MB)
- order_items.csv (609 MB)
- products.csv (869 KB)
- product_reviews.csv (388.4 MB)

## Dataset Info
- **Size**: ~2GB (CSV format)
- **Tables**: customers, orders, order_items, products, product_reviews
- **Storage**: Google Drive (shared)