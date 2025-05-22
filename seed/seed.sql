-- seed/seed.sql
CREATE TABLE IF NOT EXISTS bulletins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    location VARCHAR(255) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO
    bulletins (title, price, location)
VALUES
    ('Angus steer', 1800, 'TX'),
    ('Hereford heifer', 1500, 'OK'),
    ('Charolais bull', 2500, 'KS'),
    ('Brahman cow', 1600, 'TX'),
    ('Simmental heifer', 1550, 'NE'),
    ('Limousin steer', 1700, 'MO'),
    ('Red Angus cow-calf pair', 3200, 'SD'),
    ('Gelbvieh bull', 2400, 'CO'),
    ('Brangus bred heifer', 1900, 'TX'),
    ('Longhorn yearling', 1200, 'TX');
