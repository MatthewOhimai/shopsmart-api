# ShopSmartAPI E-Commerce Website

## Overview
ShopSmartAPI is an E-Commerce website that allows users to browse products, register, and make purchases. It includes RESTful API endpoints for user authentication, product management, and database integration.

## Features
- **User Authentication**: Register and login functionality.
- **RESTful API**: API routes for users, products, orders, and carts.
- **Product Management**: Create, retrieve, update, and delete products.
- **Cart and Order Management**: Add products to the cart, view the cart, and place orders.
- **Database Integration**: SQLite database for data persistence.
- **Swagger Documentation**: API documentation via Swagger UI.

## Requirements
- **Python 3.x**: Ensure that Python 3.x is installed on your machine.
- **pip**: Python package installer (usually comes with Python).

## Installation

1. **Clone the Repository**
   Clone the repository to your local machine using the following command:
   ```bash
   git clone https://github.com/MatthewOhimai/shopsmart.git
   ```

2. **Navigate to the project directory**
   Move into the project directory:
   ```bash
   cd shopsmart
   ```

3. **Create and Activate Virtual Environment**
   It’s recommended to use a virtual environment to manage dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. **Install the required dependencies**
   Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configuration**
   Copy `.flaskenv` to `.env`:
   ```bash
   cp .flaskenv .env
   ```
   Define the necessary environment variables in the `.env` file, such as `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, etc. Example for SQLite:
   ```env
   SQLALCHEMY_DATABASE_URI=sqlite:///database.db
   ```

6. **Database Migration Commands**
   - Initialize migration:
     ```bash
     flask db init
     ```
   - Generate a migration version:
     ```bash
     flask db migrate -m 'Initial migration'
     ```
   - Upgrade to apply the migrations to the database:
     ```bash
     flask db upgrade
     ```

7. **Running The Application**
   To run the application, use the following command:
   ```bash
   flask run
   ```
   This will start the server at `http://127.0.0.1:5000/`.

8. **Swagger API Docs**
   To access the Swagger API documentation, navigate to the following URL:
   - **Localhost example**: `http://127.0.0.1:5000/apidocs/`
   This will give you access to the documentation for all the API endpoints, including authentication, product, cart, and order management.

9. **Product Management**
   The application includes API routes for managing products. You can use the following endpoints:
   - **GET** `/api/v1/products`: Get all products.
   - **POST** `/api/v1/products`: Create a new product.
   - **GET** `/api/v1/products/{product_id}`: Get a product by its ID.
   - **PUT** `/api/v1/products/{product_id}`: Update a product's information.
   - **DELETE** `/api/v1/products/{product_id}`: Delete a product.
   
10. **Cart and Order Management**
    The application also supports cart and order management. Endpoints include:
    - **POST** `/api/v1/cart`: Add a product to the cart.
    - **GET** `/api/v1/cart`: View all items in the cart.
    - **DELETE** `/api/v1/cart/{product_id}`: Remove a product from the cart.
    - **POST** `/api/v1/orders`: Place an order for the items in the cart.
    - **GET** `/api/v1/orders`: View all orders for the authenticated user.

11. **Contributing**
    If you would like to contribute to this project, please follow these steps:
    1. Fork the repository.
    2. Create a new branch (`git checkout -b feature-branch`).
    3. Make your changes and commit them (`git commit -m 'Add some feature'`).
    4. Push to the branch (`git push origin feature-branch`).
    5. Create a new Pull Request.
    6. Remember to always sync your forked repo with the `dev` branch.

## Acknowledgments

- Special thanks to ALX, ALX9Ja Community, Julien Barbier, and Fred Swaniker for giving me the scholarship opportunity.
- This project was developed solely by me, and I am grateful for the support and resources provided by the ALX program.