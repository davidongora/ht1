-- Create the database
CREATE DATABASE HelloTractorECommerce;
USE HelloTractorECommerce;

-- Table: Tractors
CREATE TABLE Tractors (
    TractorID INT AUTO_INCREMENT PRIMARY KEY,
    Price DECIMAL(10, 2) NOT NULL,
    HpPower INT NOT NULL,
    CcPower INT NOT NULL,
    Favorite BOOLEAN DEFAULT FALSE,
    Image VARCHAR(255),
    Description TEXT,
    ReviewsAndRatings TEXT,
    Category VARCHAR(50),
    Stock INT NOT NULL
);

-- Table: UsedTractors
CREATE TABLE UsedTractors (
    TractorID INT AUTO_INCREMENT PRIMARY KEY,
    Price DECIMAL(10, 2) NOT NULL,
    HpPower INT NOT NULL,
    CcPower INT NOT NULL,
    SellerID INT,
    Favorite BOOLEAN DEFAULT FALSE,
    Image VARCHAR(255),
    HoursUsed INT NOT NULL,
    Location VARCHAR(255),
    Description TEXT,
    ReviewsAndRatings TEXT,
    Category VARCHAR(50),
    Stock INT NOT NULL,
    FOREIGN KEY (SellerID) REFERENCES Sellers(SellerID)
);

-- Table: Implements
CREATE TABLE Implements (
    ImplementID INT AUTO_INCREMENT PRIMARY KEY,
    Image VARCHAR(255),
    Price DECIMAL(10, 2) NOT NULL,
    Power INT NOT NULL,
    Category VARCHAR(50),
    DealerID INT,
    ReviewsAndRatings TEXT,
    FOREIGN KEY (DealerID) REFERENCES Dealers(DealerID)
);

-- Table: Dealers
CREATE TABLE Dealers (
    DealerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Contact VARCHAR(50) NOT NULL,
    Image VARCHAR(255),
    Location VARCHAR(255),
    ReviewsAndRatings TEXT
);

-- Table: Buyers
CREATE TABLE Buyers (
    BuyerID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Phone VARCHAR(20) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
);

-- Table: Sellers
CREATE TABLE Sellers (
    SellerID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Phone VARCHAR(20) UNIQUE NOT NULL,
    ReviewsAndRatings TEXT,
    CompanyDetails TEXT,
    username VARCHAR(100) NOT NULL UNIQUE,
    Logo VARCHAR(255),
    Description TEXT
    password VARCHAR(255) NOT NULL,

);

-- Table: CartItems
CREATE TABLE CartItems (
    CartItemID INT AUTO_INCREMENT PRIMARY KEY,
    BuyerID INT,
    Quantity INT NOT NULL,
    ItemID INT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    TotalPrice DECIMAL(10, 2) AS (Quantity * Price) STORED,
    FOREIGN KEY (BuyerID) REFERENCES Buyers(BuyerID)
);


-- Insert records into the 'dealers' table
INSERT INTO dealers (id, name, contact, image, location, reviews_ratings)
VALUES 
(1, 'CMC', '722283433', 'https://cmc.com/logo.png', 'Nairobi, Lusaka Rd', 4.5),
(2, 'Mascor', '254720935034', 'https://mascor.com/logo.png', 'Narok', 4.2),
(3, 'FMD Marsay', '722205538', 'https://fmdmarsay.com/logo.png', 'Nakuru, Biashara George Morara Ave', 4.8),
(4, 'CFAO Motors', '207604121', 'https://cfaomotors.com/logo.png', 'Nakuru, Town East, George Morara Rd', 4.6),
(5, 'Terranova Automotive', '254777222239', 'https://terranova.com/logo.png', 'Bungoma, Webuye Malaba Rd', 4.3);

-- Insert records into the 'tractors' table
INSERT INTO tractors (id, price, hp_power, cc_power, favorite, image, description, reviews_ratings, category, stock)
VALUES
(1, 12000, 35, 2000, FALSE, 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/DI-35-removebg-preview.png', 'Sonalika DI-35 with 35 HP.', 4.5, 'New', 10),
(2, 25000, 95, 4800, TRUE, 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/6095B-removebg-preview.png', 'John Deere 6095B for large scale farming.', 4.7, 'New', 8),
(3, 18000, 75, 3800, FALSE, 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/DI-75-removebg-preview.png', 'Sonalika DI-75 with 75 HP.', 4.4, 'New', 5),
(4, 21000, 85, 4000, TRUE, 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/MB-removebg-preview.png', 'McCormick MB85 versatile tractor.', 4.3, 'New', 6),
(5, 30000, 125, 5500, FALSE, 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/TS6-125.png', 'New Holland TS6.125 for high performance.', 4.8, 'New', 4);

-- Insert records into the 'sellers' table
INSERT INTO sellers (id, email, phone, reviews_ratings, company_details, logos, descriptions, password)
VALUES
(1, 'seller1@example.com', '1234567890', 4.6, 'ABC Tractors', 'https://seller1logo.com', 'Authorized dealer of Sonalika tractors.', 'seller1pass'),
(2, 'seller2@example.com', '9876543210', 4.5, 'DEF Implements', 'https://seller2logo.com', 'Specialized in farming implements.', 'seller2pass'),
(3, 'seller3@example.com', '4567891230', 4.3, 'GHI Machinery', 'https://seller3logo.com', 'Certified dealer of New Holland tractors.', 'seller3pass'),
(4, 'seller4@example.com', '7891234560', 4.7, 'JKL Equipment', 'https://seller4logo.com', 'Authorized Case IH distributor.', 'seller4pass'),
(5, 'seller5@example.com', '3216549870', 4.4, 'MNO AgriCo', 'https://seller5logo.com', 'Expert in second-hand tractors.', 'seller5pass');

-- Insert records into the 'buyers' table
INSERT INTO buyers (id, email, phone, password)
VALUES
(1, 'buyer1@example.com', '1234567891', 'buyer1pass'),
(2, 'buyer2@example.com', '9876543212', 'buyer2pass'),
(3, 'buyer3@example.com', '4567891233', 'buyer3pass'),
(4, 'buyer4@example.com', '7891234564', 'buyer4pass'),
(5, 'buyer5@example.com', '3216549875', 'buyer5pass');

-- Insert records into the 'implements' table
INSERT INTO implements (id, image, price, power, category, dealerid, reviews_ratings)
VALUES
(1, 'https://implements.com/plow.png', 1500, 10, 'Plowing', 1, 4.5),
(2, 'https://implements.com/harrow.png', 2000, 15, 'Harrowing', 2, 4.7),
(3, 'https://implements.com/seeder.png', 1800, 12, 'Seeding', 3, 4.4),
(4, 'https://implements.com/sprayer.png', 2200, 18, 'Spraying', 4, 4.6),
(5, 'https://implements.com/harvester.png', 5000, 100, 'Harvesting', 5, 4.8);
