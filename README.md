# 🛍️ E-Commerce Product Recommendation System (Flask & Content-Based Filtering)

## Project Overview

This is a **full-stack e-commerce demonstration application** built using **Python/Flask** that implements a robust **Content-Based Recommendation System**. The project showcases proficiency in web development, database integration, and machine learning model deployment, handling data persistence and complex feature engineering.

## ✨ Live Demo & Status

The application is fully deployed and operational, connecting the web service to a dedicated external database.

➡️ **Live URL:** [https://e-com-app-6h4m.onrender.com/](https://e-com-app-6h4m.onrender.com/)

### Demo Video

Watch a quick video showcasing the search, recommendation engine, and dynamic theming features:

[![Watch the Demo Video](https://img.youtube.com/vi/HWaRKIvUmsQ/0.jpg)](https://youtu.be/HWaRKIvUmsQ)

---

## 💻 Technical Features

| Feature | Description | Core Technology |
| :--- | :--- | :--- |
| **Content-Based Engine** | Uses **TF-IDF Vectorization** and **Cosine Similarity** (`scikit-learn`) to calculate product similarity based on item tags and descriptions. | **Scikit-learn / Pandas** |
| **Optimized Model Loading** | **The ML matrix is pre-loaded once from the database** on application startup, minimizing latency for sub-second search responses. | **Python (In-Memory)** |
| **Dual Search Strategy** | Supports both general queries (Query-to-Item) and exact name matches (Item-to-Item) to maximize relevance. | **Flask/Python Logic** |
| **Quick Recommendation View** | A homepage modal instantly loads 5 related product recommendations without a page refresh. | **JavaScript/Fetch API** |
| **Secure Authentication** | User registration and login functionality is secure and persistent. | **Flask-SQLAlchemy & werkzeug.security** |
| **Dynamic Theming** | Users can toggle and save their preference for **dark mode**. | **JavaScript `localStorage`** |

---

## 🛠️ Tech Stack & Deployment

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Core Framework** | **Python (Flask) & Gunicorn** | Flask handles the API and routing; Gunicorn handles production serving. |
| **Database** | **PostgreSQL (Neon)** | Primary production database source for reliability and persistence. |
| **Data & ML** | **Pandas, Scikit-learn** | Used for data cleaning, transformation, and model generation. |
| **ORM** | **Flask-SQLAlchemy** | Manages `User`, `Product`, and `Interactions` tables. |
| **Frontend** | **Bootstrap 5, Jinja2, JavaScript** | Responsive UI and dynamic client-side interactions. |

---

## 💡 Future Enhancements

These features are planned to expand the project's complexity and business value:

* **Collaborative Filtering Integration:** Implement a second recommendation engine (e.g., using SVD or KNN) based on actual user **ratings and implicit interactions**. This would transition the system from content-based to personalized recommendations.
* **User Profile Customization:** Allow logged-in users to update their profile details and view their history.
* **Logging and Metrics:** Implement system logging to track model performance, cold start times, and user search queries.

---

## ⚙️ Local Setup and Installation

Follow these steps to set up the project locally (assumes local PostgreSQL is running).

### Steps

1.  **Clone & Setup Environment:**
    ```bash
    git clone [https://github.com/sh-kartik18/E-Commerce-Recommendation-System](https://github.com/sh-kartik18/E-Commerce-Recommendation-System)
    cd Ecom-Recommendation-System
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Configure Local DB:** Create a file named **`.env`** and add your local PostgreSQL connection string.

    ```dotenv
    # .env file
    DATABASE_URL=postgresql://myuser:mypassword@localhost/ecom
    ```

3.  **Initialize and Populate Database:**
    ```bash
    flask init-db    # Creates all tables
    flask populate-db # Loads data from CSVs
    ```

4.  **Run the Application:**
    ```bash
    python run.py
    ```

---

## 🧑‍💻 Custom CLI Commands

| Command | Description |
| :--- | :--- |
| `flask init-db` | Drops and recreates all SQL database tables. |
| `flask populate-db` | Reads product data from CSVs and inserts it into the `product` table. |

---

## 🔗 Contact

* **GitHub:** [https://github.com/sh-kartik18](https://github.com/sh-kartik18)
* **LinkedIn:** [https://www.linkedin.com/in/sh-kartik](https://www.linkedin.com/in/sh-kartik)
* **Kaggle:** [https://kaggle.com/kartikksh](https://kaggle.com/kartikksh)
