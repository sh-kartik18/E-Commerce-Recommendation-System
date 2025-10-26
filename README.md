# 🛍️ E-Commerce Product Recommendation System (Flask & Content-Based Filtering)

## Project Overview

This is a **full-stack e-commerce demonstration application** built using **Python Flask** that implements a robust **Content-Based Recommendation System**. The application is designed to showcase proficiency in web development, database integration, and machine learning model deployment.

The system allows users to search the product catalog and receive personalized, relevant recommendations based on product characteristics.

## ✨ Website Features

| Feature | Description | Technical Implementation |
| :--- | :--- | :--- |
| **Content-Based Recommendations** | Uses the pre-trained model to find the most similar products based on the search query or a clicked item. | **TF-IDF Vectorization** & **Cosine Similarity** (computed using `scikit-learn`). |
| **Search Functionality** | Allows users to input partial names (e.g., "blue polish") or exact product names to retrieve results. | **Dual Strategy** (Query-to-Item Search and Item-to-Item Lookup). |
| **Dynamic Product Cards** | Displays product details pulled from the database, ensuring clean formatting. | Jinja2 templating, custom filters to display **only the first word of the Brand** (capitalized), and safe handling of missing/zero **Ratings** and **Review Counts**. |
| **Authentication System** | Secure user registration and login functionality. | **Flask-SQLAlchemy** (`User` model) with **`werkzeug.security`** for password hashing. |
| **Quick Recommendation View** | When a user clicks a product on the homepage, a modal instantly loads 5 related product recommendations via a live API call. | **JavaScript/Fetch API** calls a dedicated Flask route (`/api/recommend`). |
| **Theming** | Allows users to switch between light (default) and **dark mode**. | **JavaScript `localStorage`** saves the user preference, persisting the theme across sessions and page reloads. |

## 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3 | Core programming language. |
| **Web Framework** | **Flask** | Routing, request handling, and custom CLI management. |
| **Database** | **PostgreSQL** | Primary production database (connected via `DATABASE_URL`). |
| **Database (Dev/Fallback)** | MySQL | Local development environment fallback. |
| **ORM** | **Flask-SQLAlchemy** | Model definition (`User`, `Product`, `Interactions`) and database management. |
| **ML & Data** | **Pandas, scikit-learn** | Data handling, TF-IDF model creation, and similarity calculation. |
| **Frontend** | **Jinja2, Bootstrap 5** | Responsive design, modern UI, and dynamic templating. |

## 🚀 Deployment

The final application is designed for reliable, scalable hosting.

1.  **Compute/Web App:** Not deployed yet.
2.  **Database:** Hosted on **Neon** (serverless PostgreSQL).

The application uses the `DATABASE_URL` environment variable for seamless connection to the live database in production.

## 🎬 Live Demo

Watch a quick 60-second video demonstrating the search, recommendation engine, and dynamic theming.

[![Watch the Demo Video](https://img.youtube.com/vi/HWaRKIvUmsQ/0.jpg)](https://youtu.be/HWaRKIvUmsQ)

## ⚙️ Local Setup and Installation

Follow these steps to set up the project on your local machine using your PostgreSQL installation.

### Prerequisites

* Python 3.8+
* PostgreSQL installed locally and running.
* You must have created the `ecom` database and a user (`myuser`) in your local PostgreSQL.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/sh-kartik18/E-Commerce-Recommendation-System
    cd Ecom-Recommendation-System
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure PostgreSQL Connection:**
    Create a file named **`.env`** in the project root and add your local PostgreSQL connection string.

    ```dotenv
    # .env file
    DATABASE_URL=postgresql://myuser:mypassword@localhost/ecom
    ```
    *(Replace username, password, and database name as necessary).*

5.  **Initialize and Populate the Database:**
    These commands use the custom CLI tools defined in `app/__init__.py`.

    ```bash
    # 1. Create tables (User, Product, Interactions)
    flask init-db

    # 2. Populate product table from CSVs
    flask populate-db
    ```

6.  **Run the Application:**
    ```bash
    python run.py
    ```
    The application will be accessible at `http://127.0.0.1:5000/`.

## 🧑‍💻 Custom CLI Commands

The project uses Flask's CLI for database maintenance:

| Command | Description |
| :--- | :--- |
| `flask init-db` | Drops and recreates all SQL database tables based on `app/models.py`. |
| `flask populate-db` | Reads product data from CSVs and inserts it into the `product` table. |

## 🔗 Contact

* **GitHub:** [https://github.com/sh-kartik18]
* **LinkedIn:** [https://www.linkedin.com/in/sh-kartik]
* **Kaggle:** [https://kaggle.com/kartikksh]

Feel free to connect!
