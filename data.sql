CREATE DATABASE IF NOT EXISTS it_inventory_47;
USE it_inventory_47;

-- ВИДАЛЕННЯ ТАБЛИЦЬ У ЗВОРОТНОМУ ПОРЯДКУ (спочатку дочірні, потім батьківські/довідники)
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS employee_offices;
DROP TABLE IF EXISTS employee_details;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS pc_specs;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS offices;

-- СТВОРЕННЯ ТАБЛИЦЬ (ENGINE = INNODB)

-- 1. Довідник офісів
CREATE TABLE offices (
    office_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL
) ENGINE = INNODB;

-- 2. Довідник відділів
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
) ENGINE = INNODB;

-- 3. Довідник посад
CREATE TABLE positions (
    position_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL
) ENGINE = INNODB;

-- 4. Довідник категорій техніки
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT uk_cat_name UNIQUE (name)
) ENGINE = INNODB;

-- 5. Довідник брендів
CREATE TABLE brands (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT uk_brand_name UNIQUE (name)
) ENGINE = INNODB;

-- 6. Довідник характеристик ПК
CREATE TABLE pc_specs (
    spec_id INT AUTO_INCREMENT PRIMARY KEY,
    cpu_model VARCHAR(100) NOT NULL,
    ram_gb INT NOT NULL,
    storage_gb INT NOT NULL
) ENGINE = INNODB;

-- 7. Працівники
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    department_id INT NOT NULL,
    position_id INT NOT NULL,
    CONSTRAINT uk_emp_email UNIQUE (email)
) ENGINE = INNODB;

-- 8. Обладнання / техніка
CREATE TABLE equipment (
    equip_id INT AUTO_INCREMENT PRIMARY KEY,
    serial_number VARCHAR(100) NOT NULL,
    inventory_number VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    brand_id INT NOT NULL,
    spec_id INT,
    CONSTRAINT uk_equip_sn UNIQUE (serial_number),
    CONSTRAINT uk_equip_inv UNIQUE (inventory_number)
) ENGINE = INNODB;

-- 9. Деталі працівника (ЗВ'ЯЗОК 1:1 до employees)
CREATE TABLE employee_details (
    employee_id INT PRIMARY KEY,
    passport_number VARCHAR(20) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    CONSTRAINT uk_passport UNIQUE (passport_number)
) ENGINE = INNODB;

-- 10. Проміжна таблиця (ЗВ'ЯЗОК M:N між employees та offices)
CREATE TABLE employee_offices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    office_id INT NOT NULL,
    room_number VARCHAR(50) NOT NULL
) ENGINE = INNODB;

-- 11. Видача техніки (журнал призначень)
CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    equip_id INT NOT NULL,
    employee_id INT,
    office_id INT,
    issue_date DATE NOT NULL
) ENGINE = INNODB;

-- ДОДАВАННЯ ЗОВНІШНІХ КЛЮЧІВ ЧЕРЕЗ ALTER TABLE ADD CONSTRAINT
ALTER TABLE employees
    ADD CONSTRAINT fk_emp_dept
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    ADD CONSTRAINT fk_emp_pos
    FOREIGN KEY (position_id) REFERENCES positions(position_id);

ALTER TABLE equipment
    ADD CONSTRAINT fk_equip_cat
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    ADD CONSTRAINT fk_equip_brand
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    ADD CONSTRAINT fk_equip_spec
    FOREIGN KEY (spec_id) REFERENCES pc_specs(spec_id);

ALTER TABLE employee_details
    ADD CONSTRAINT fk_details_emp
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE;

ALTER TABLE employee_offices
    ADD CONSTRAINT fk_empoff_emp
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    ADD CONSTRAINT fk_empoff_off
    FOREIGN KEY (office_id) REFERENCES offices(office_id);

ALTER TABLE assignments
    ADD CONSTRAINT fk_assign_equip
    FOREIGN KEY (equip_id) REFERENCES equipment(equip_id),
    ADD CONSTRAINT fk_assign_emp
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    ADD CONSTRAINT fk_assign_off
    FOREIGN KEY (office_id) REFERENCES offices(office_id);

-- ДОДАТКОВІ ІНДЕКСИ (вимога: мінімум 2 індекси на поля без UNIQUE)
CREATE INDEX idx_emp_last_name ON employees(last_name);
CREATE INDEX idx_assign_date ON assignments(issue_date);
CREATE INDEX idx_office_city ON offices(city);

-- ЗАПОВНЕННЯ ТАБЛИЦЬ У ПРАВИЛЬНОМУ ПОРЯДКУ (по 10 записів у кожній)

INSERT INTO offices (city, address) VALUES 
('Kyiv', 'Khreshchatyk 1'), ('Lviv', 'Naukova 7'), ('Odesa', 'Derybasivska 10'), 
('Kharkiv', 'Nauky 15'), ('Dnipro', 'Polia 20'), ('Zaporizhzhia', 'Sobornyi 100'),
('Vinnytsia', 'Soborna 50'), ('Poltava', 'Evropeiska 22'), ('Chernihiv', 'Myru 14'),
('Cherkasy', 'Shevchenka 200');

INSERT INTO departments (name) VALUES 
('IT'), ('HR'), ('Sales'), ('Marketing'), ('Management'),
('Finance'), ('Legal'), ('Customer Support'), ('Logistics'), ('R&D');

INSERT INTO positions (title) VALUES 
('Developer'), ('SysAdmin'), ('Manager'), ('Designer'), ('QA'),
('Accountant'), ('Lawyer'), ('Support Agent'), ('Data Analyst'), ('DevOps');

INSERT INTO categories (name) VALUES 
('Laptop'), ('Monitor'), ('IP Phone'), ('Router'), ('Printer'),
('Server'), ('Switch'), ('Tablet'), ('Projector'), ('UPS');

INSERT INTO brands (name) VALUES 
('Dell'), ('HP'), ('Apple'), ('Cisco'), ('MikroTik'),
('Samsung'), ('Lenovo'), ('Asus'), ('APC'), ('Sony');

INSERT INTO pc_specs (cpu_model, ram_gb, storage_gb) VALUES 
('Intel Core i7', 16, 512), ('Apple M1', 16, 512), ('AMD Ryzen 5', 8, 256), 
('Intel Core i5', 16, 512), ('Apple M2', 32, 1024), ('Intel Core i9', 64, 2048),
('AMD Ryzen 9', 32, 1024), ('Apple M3 Pro', 36, 1024), ('Intel Xeon', 128, 4096),
('Intel Core i3', 8, 256);

INSERT INTO employees (first_name, last_name, email, department_id, position_id) VALUES 
('Ivan', 'Ivanov', 'ivan@test.com', 1, 1), ('Petro', 'Petrov', 'petro@test.com', 1, 2),
('Anna', 'Boyko', 'anna@test.com', 2, 3), ('Olena', 'Tymkiv', 'olena@test.com', 4, 4),
('Maksym', 'Koval', 'maks@test.com', 1, 5), ('Serhiy', 'Melnyk', 'serhiy@test.com', 6, 6),
('Yulia', 'Shevchuk', 'yulia@test.com', 7, 7), ('Andriy', 'Bondar', 'andriy@test.com', 8, 8),
('Natalia', 'Kravets', 'natalia@test.com', 10, 9), ('Taras', 'Moroz', 'taras@test.com', 1, 10);

INSERT INTO equipment (serial_number, inventory_number, category_id, brand_id, spec_id) VALUES 
('SN1001', 'INV1', 1, 3, 2), ('SN1002', 'INV2', 1, 1, 1), ('SN1003', 'INV3', 2, 1, NULL), 
('SN1004', 'INV4', 2, 1, NULL), ('SN1005', 'INV5', 3, 4, NULL), ('SN1006', 'INV6', 4, 5, NULL),
('SN1007', 'INV7', 5, 2, NULL), ('SN1008', 'INV8', 1, 7, 7), ('SN1009', 'INV9', 8, 6, NULL),
('SN1010', 'INV10', 6, 1, 9);

INSERT INTO employee_details (employee_id, passport_number, phone_number, birth_date) VALUES 
(1, 'KX123456', '+380501112233', '1990-05-15'), (2, 'KX234567', '+380672223344', '1988-11-20'),
(3, 'ME345678', '+380633334455', '1995-02-10'), (4, 'ME456789', '+380974445566', '1992-08-05'),
(5, 'TT567890', '+380505556677', '1994-12-30'), (6, 'TT678901', '+380676667788', '1985-04-25'),
(7, 'AB789012', '+380637778899', '1991-09-14'), (8, 'AB890123', '+380978889900', '1989-07-07'),
(9, 'CD901234', '+380509990011', '1996-03-22'), (10, 'CD012345', '+380670001122', '1993-01-18');

INSERT INTO employee_offices (employee_id, office_id, room_number) VALUES 
(1, 1, '101'), (1, 2, '205'), (2, 1, '102'), (3, 2, '201'), (4, 3, '301'), 
(5, 1, '101'), (6, 4, '404'), (7, 5, '501'), (8, 1, '105'), (10, 2, '206');

INSERT INTO assignments (equip_id, employee_id, office_id, issue_date) VALUES 
(1, 1, NULL, '2023-01-10'), (2, 2, NULL, '2023-01-15'), (3, 1, 1, '2023-01-10'), 
(4, 1, 1, '2023-01-10'), (5, 3, 2, '2023-02-01'), (6, NULL, 1, '2022-12-01'), 
(7, NULL, 2, '2022-12-05'), (8, 10, NULL, '2023-03-20'), (9, 8, NULL, '2023-04-12'),
(10, NULL, 1, '2023-05-01');
