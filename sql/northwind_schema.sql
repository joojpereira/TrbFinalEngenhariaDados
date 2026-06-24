

-- ==========================
-- CATEGORIES
-- ==========================

CREATE TABLE public.categories (
    category_id INT4 NOT NULL,
    category_name VARCHAR(100),
    CONSTRAINT categories_pkey PRIMARY KEY (category_id)
);

-- ==========================
-- CUSTOMERS
-- ==========================

CREATE TABLE public.customers (
    customer_id INT4 NOT NULL,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(10),
    created_at DATE,
    CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
);

-- ==========================
-- EMPLOYEES
-- ==========================

CREATE TABLE public.employees (
    employee_id INT4 NOT NULL,
    employee_name VARCHAR(255),
    hire_date DATE,
    CONSTRAINT employees_pkey PRIMARY KEY (employee_id)
);

-- ==========================
-- PRODUCTS
-- ==========================

CREATE TABLE public.products (
    product_id INT4 NOT NULL,
    product_name VARCHAR(255),
    unit_price NUMERIC(10,2),
    CONSTRAINT products_pkey PRIMARY KEY (product_id)
);

-- ==========================
-- SUPPLIERS
-- ==========================

CREATE TABLE public.suppliers (
    supplier_id INT4 NOT NULL,
    supplier_name VARCHAR(255),
    city VARCHAR(100),
    CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id)
);

-- ==========================
-- SHIPPERS
-- ==========================

CREATE TABLE public.shippers (
    shipper_id INT4 NOT NULL,
    company_name VARCHAR(255),
    CONSTRAINT shippers_pkey PRIMARY KEY (shipper_id)
);

-- ==========================
-- REGIONS
-- ==========================

CREATE TABLE public.regions (
    region_id INT4 NOT NULL,
    region_name VARCHAR(100),
    CONSTRAINT regions_pkey PRIMARY KEY (region_id)
);

-- ==========================
-- TERRITORIES
-- ==========================

CREATE TABLE public.territories (
    territory_id INT4 NOT NULL,
    region_id INT4,
    territory_name VARCHAR(255),

    CONSTRAINT territories_pkey
        PRIMARY KEY (territory_id),

    CONSTRAINT territories_region_id_fkey
        FOREIGN KEY (region_id)
        REFERENCES public.regions(region_id)
);

-- ==========================
-- ORDERS
-- ==========================

CREATE TABLE public.orders (
    order_id INT4 NOT NULL,
    customer_id INT4,
    employee_id INT4,
    order_date DATE,
    freight NUMERIC(10,2),

    CONSTRAINT orders_pkey
        PRIMARY KEY (order_id),

    CONSTRAINT orders_customer_id_fkey
        FOREIGN KEY (customer_id)
        REFERENCES public.customers(customer_id),

    CONSTRAINT orders_employee_id_fkey
        FOREIGN KEY (employee_id)
        REFERENCES public.employees(employee_id)
);

-- ==========================
-- ORDER DETAILS
-- ==========================

CREATE TABLE public.order_details (
    order_detail_id SERIAL,

    order_id INT4,
    product_id INT4,
    quantity INT4,
    unit_price NUMERIC(10,2),
    total NUMERIC(10,2),

    CONSTRAINT order_details_pkey
        PRIMARY KEY (order_detail_id),

    CONSTRAINT order_details_order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES public.orders(order_id),

    CONSTRAINT order_details_product_id_fkey
        FOREIGN KEY (product_id)
        REFERENCES public.products(product_id)
);