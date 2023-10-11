CREATE DATABASE productos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE productos;

CREATE TABLE producto (
    id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    price DECIMAL(10, 2),
    `desc` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    category VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    specifications JSON,
    pictures JSON,
    date DATE,
    PRIMARY KEY(id)
);

GRANT ALL PRIVILEGES ON productos.* TO 'usuario'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE links CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE links;

CREATE TABLE link (
    id INT AUTO_INCREMENT,
    url VARCHAR(2083) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
    PRIMARY KEY(id)
);

GRANT ALL PRIVILEGES ON links.* TO 'usuario'@'%';
FLUSH PRIVILEGES;
