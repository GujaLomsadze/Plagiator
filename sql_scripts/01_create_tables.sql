CREATE TABLE public.users
(
    id         SERIAL PRIMARY KEY,
    username   VARCHAR(50) UNIQUE  NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.products
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100)   NOT NULL,
    price       DECIMAL(10, 2) NOT NULL,
    description TEXT
);
