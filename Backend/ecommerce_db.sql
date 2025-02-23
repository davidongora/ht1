-- Create the eCommerce database
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Add additional columns for user profile
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    address TEXT
);

-- Create products table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    gender ENUM('Male', 'Female', 'Unisex'),
    size VARCHAR(50),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Add stock quantity for inventory management
    stock_quantity INT NOT NULL DEFAULT 0
);

-- Create shopping_cart table
CREATE TABLE shopping_cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    total_price DECIMAL(10, 2) NOT NULL,
    status ENUM('Pending', 'Shipped', 'Delivered') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create order_items table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create product_filters table for filtering options
CREATE TABLE product_filters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    filter_type ENUM('price', 'gender', 'size'),
    filter_value VARCHAR(50),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create coupons table for discount codes
CREATE TABLE coupons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    discount_amount DECIMAL(10, 2) NOT NULL,
    expiration_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create user_wishlist table for user wishlists
CREATE TABLE user_wishlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create product_reviews table for product reviews and ratings
CREATE TABLE product_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    user_id INT,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create email_notifications table for tracking notifications sent
CREATE TABLE email_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    notification_type ENUM('Order Confirmation', 'Shipping Update', 'Promotional'),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create loyalty_programs table for tracking user rewards
CREATE TABLE loyalty_programs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    points INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create blogs table for content management
CREATE TABLE blogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INT,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- Create product_recommendations table for personalized suggestions
CREATE TABLE product_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    recommendation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO products (name, description, price, category, gender, size, image_url, stock_quantity)
VALUES
-- Clothing (Men)
('Men\'s T-shirt', 'Comfortable cotton T-shirt', 15.99, 'Clothing', 'Male', 'M', 'image1.jpg', 50),
('Men\'s Jeans', 'Classic blue jeans', 39.99, 'Clothing', 'Male', 'L', 'image2.jpg', 30),
('Men\'s Jacket', 'Waterproof sports jacket', 59.99, 'Clothing', 'Male', 'XL', 'image3.jpg', 20),
('Men\'s Shorts', 'Casual summer shorts', 24.99, 'Clothing', 'Male', 'M', 'image4.jpg', 25),
('Men\'s Sweater', 'Woolen winter sweater', 45.99, 'Clothing', 'Male', 'L', 'image5.jpg', 15),

-- Clothing (Women)
('Women\'s Dress', 'Elegant evening dress', 69.99, 'Clothing', 'Female', 'S', 'image6.jpg', 10),
('Women\'s T-shirt', 'Soft cotton T-shirt', 18.99, 'Clothing', 'Female', 'M', 'image7.jpg', 40),
('Women\'s Jeans', 'Skinny blue jeans', 42.99, 'Clothing', 'Female', 'L', 'image8.jpg', 35),
('Women\'s Skirt', 'Floral print skirt', 34.99, 'Clothing', 'Female', 'M', 'image9.jpg', 20),
('Women\'s Jacket', 'Faux leather jacket', 55.99, 'Clothing', 'Female', 'XL', 'image10.jpg', 12),

-- Clothing (Unisex)
('Unisex Hoodie', 'Comfortable hoodie for men and women', 49.99, 'Clothing', 'Unisex', 'L', 'image11.jpg', 45),
('Unisex Tracksuit', 'Stylish tracksuit', 75.99, 'Clothing', 'Unisex', 'M', 'image12.jpg', 25),
('Unisex Socks', 'Cotton socks pack', 9.99, 'Clothing', 'Unisex', 'L', 'image13.jpg', 100),
('Unisex Cap', 'Adjustable sports cap', 19.99, 'Clothing', 'Unisex', 'One Size', 'image14.jpg', 60),
('Unisex Scarf', 'Winter scarf', 14.99, 'Clothing', 'Unisex', 'One Size', 'image15.jpg', 80),

-- Footwear (Men)
('Men\'s Running Shoes', 'Lightweight running shoes', 85.99, 'Footwear', 'Male', '10', 'image16.jpg', 25),
('Men\'s Formal Shoes', 'Leather formal shoes', 95.99, 'Footwear', 'Male', '9', 'image17.jpg', 15),
('Men\'s Sandals', 'Comfortable summer sandals', 25.99, 'Footwear', 'Male', '11', 'image18.jpg', 30),

-- Footwear (Women)
('Women\'s High Heels', 'Elegant high heels', 89.99, 'Footwear', 'Female', '7', 'image19.jpg', 18),
('Women\'s Sneakers', 'Casual sneakers', 49.99, 'Footwear', 'Female', '8', 'image20.jpg', 20),
('Women\'s Boots', 'Stylish leather boots', 110.99, 'Footwear', 'Female', '9', 'image21.jpg', 12),

-- Accessories (Men)
('Men\'s Wallet', 'Leather bi-fold wallet', 19.99, 'Accessories', 'Male', 'One Size', 'image22.jpg', 70),
('Men\'s Belt', 'Genuine leather belt', 24.99, 'Accessories', 'Male', 'One Size', 'image23.jpg', 40),

-- Accessories (Women)
('Women\'s Handbag', 'Luxury leather handbag', 129.99, 'Accessories', 'Female', 'One Size', 'image24.jpg', 10),
('Women\'s Sunglasses', 'Fashionable sunglasses', 49.99, 'Accessories', 'Female', 'One Size', 'image25.jpg', 30),

-- Accessories (Unisex)
('Unisex Watch', 'Waterproof digital watch', 79.99, 'Accessories', 'Unisex', 'One Size', 'image26.jpg', 20),
('Unisex Backpack', 'Durable travel backpack', 55.99, 'Accessories', 'Unisex', 'One Size', 'image27.jpg', 40),
('Unisex Belt', 'Canvas belt with adjustable buckle', 14.99, 'Accessories', 'Unisex', 'One Size', 'image28.jpg', 50),
('Unisex Gloves', 'Winter thermal gloves', 19.99, 'Accessories', 'Unisex', 'M', 'image29.jpg', 60),
('Unisex Sunglasses', 'Polarized sunglasses', 29.99, 'Accessories', 'Unisex', 'One Size', 'image30.jpg', 35);



-- coupons, Order History
-- Reports and Analytics: Generate reports on sales, customer behavior, inventory levels, and other key metrics.
-- Email Notifications: Send order confirmations, shipping updates, and promotional emails.
-- Loyalty Programs: Implement a rewards program to encourage repeat purchases.
-- Blog/Content Management: Include a blog or content section to engage users with relevant articles, news, and promotions.
-- Inventory Management: Track stock levels and manage inventory to avoid overselling.
-- Search and Filters: Allow users to search for products and filter results by various criteria such as price range, category, gender, size, and ratings.
-- Product Reviews and Ratings: Let users leave reviews and rate products. This helps other customers make informed decisions.
-- Wishlist: Enable users to save products they’re interested in for future reference.
-- Product Recommendations: Provide personalized product suggestions based on browsing history, previous purchases, or popular products.
-- User Profiles: Allow users to manage their profiles, view order history, and track current orders.
-- Product Comparison: Enable users to compare multiple products side-by-side.
