-- creating a users table with a country column that only accepts 'US', 'CO', 'TN' values

CREATE TABLE IF NOT EXISTS USERS (
    id INT AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',
    PRIMARY KEY (id)
);
