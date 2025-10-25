import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
# Create the database instance
db = SQLAlchemy()

def create_app():
    # Point Flask to the templates folder outside 'app'
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_path = os.path.join(base_dir, "templates")
    static_path = os.path.join(base_dir, "static")

    app = Flask(__name__, template_folder=template_path, static_folder=static_path)
    
    # Secret key for sessions
    app.secret_key = os.environ.get('FLASK_SECRET', 'supersecretkey')

    # --- Database Configuration ---
    
    # 1. Check for the production (PostgreSQL) URL
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        print("--- Production environment detected: Connecting to PostgreSQL ---")
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # We are in development (local)
        print("--- Local environment detected: Connecting to MySQL ---")
        
        # 2. Fall back to the local MySQL setup
        db_password = os.environ.get('DB_PASSWORD', '')
        if not db_password:
            print("Warning: 'DB_PASSWORD' environment variable is not set for local MySQL.")
            
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{db_password}@localhost/ecom'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with app
    db.init_app(app)

    app.app_context().push()

    from . import models 

    @app.cli.command("init-db")
    def init_db_command():
        """Creates the database tables."""
        with app.app_context():
            db.create_all()
        print("Tables created successfully!")

    @app.cli.command("populate-db")
    def populate_db_command():
        """Reads CSVs and populates the Product table."""
        with app.app_context():
            # Check if products already exist
            if models.Product.query.first():
                print("Product table already populated.")
                print("To re-populate, first clear the 'product' table.")
                return

            # Read your CSV
            csv_path = 'models/products.csv' 
            try:
                df = pd.read_csv(csv_path)
            except FileNotFoundError:
                print(f"Error: Could not find {csv_path}")
                return

            # --- THIS IS THE FIX ---
            # Replace all Pandas NaN/NaT values with Python's None
            # SQLAlchemy translates None to NULL.
            df = df.where(pd.notna(df), None)
            # --- END OF FIX ---

            # Loop and add to session
            for _, row in df.iterrows():
                
                # Prepare the ImageURL
                all_urls = row.get('ImageURL')
                first_url = None 
                if isinstance(all_urls, str):
                    first_url = all_urls.split(' | ')[0].strip()
                
                # Now, create the product
                # This is safer because 'nan' is now 'None'
                product = models.Product(
                    Name=row.get('Name'),
                    Brand=row.get('Brand'),   # This will be None if missing
                    Tags=row.get('Tags'),     # This will be None if missing
                    ImageURL=first_url,
                    Rating=row.get('Rating') or 0.0,      # Use 0.0 as default
                    ReviewCount=row.get('ReviewCount') or 0  # Use 0 as default
                )
                db.session.add(product)

            # Commit to database
            try:
                db.session.commit()
                print("Product table populated successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"An error occurred: {e}")
    # --- END OF SECTION ---

    # Import and register Blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app

