CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio NUMERIC(10,2),
    stock INTEGER
);

INSERT INTO productos (nombre, precio, stock) VALUES
('Laptop', 850.00, 10),
('Mouse', 25.50, 50),
('Teclado', 40.00, 30),
('Monitor', 220.00, 15),
('Impresora', 180.00, 8);