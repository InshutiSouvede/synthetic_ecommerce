db = db.getSiblingDB('ecommerce_db');

db.createUser({
  user: 'ecommerce_user',
  pwd: 'ecommerce_password',
  roles: [
    {
      role: 'readWrite',
      db: 'ecommerce_db'
    }
  ]
});

db.createCollection('customers');
db.customers.createIndex({ "customer_id": 1 }, { unique: true });
db.customers.createIndex({ "email": 1 }, { unique: true });

db.createCollection('products');
db.products.createIndex({ "product_id": 1 }, { unique: true });
db.products.createIndex({ "category": 1 });

db.createCollection('orders');
db.orders.createIndex({ "order_id": 1 }, { unique: true });
db.orders.createIndex({ "customer_id": 1 });

db.createCollection('order_items');
db.order_items.createIndex({ "order_item_id": 1 }, { unique: true });
db.order_items.createIndex({ "order_id": 1 });
db.order_items.createIndex({ "product_id": 1 });

db.createCollection('product_reviews');
db.product_reviews.createIndex({ "review_id": 1 }, { unique: true });
db.product_reviews.createIndex({ "product_id": 1 });
db.product_reviews.createIndex({ "customer_id": 1 });