from flask import Blueprint, request, redirect, url_for, flash, session, render_template, jsonify
from . import db
from .models import User, Product
import pandas as pd 
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

main = Blueprint('main', __name__)

# -----------------
# 1. ONE-TIME DATA & MODEL SETUP
# -----------------
try:
    # --- Load your main product dataset ---
    train_data = pd.read_csv('models/products.csv')

    # --- Pre-compute the TF-IDF and Similarity Matrix ---
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    # --- Create a mapping from item name to index ---
    indices = pd.Series(train_data.index, index=train_data['Name']).drop_duplicates()
    
    print("--- Product data and similarity matrix loaded successfully! ---")

except FileNotFoundError:
    print("--- ERROR: Product data file not found! ---")
    train_data = pd.DataFrame() # Create empty dataframe to avoid crashes
    cosine_similarities_content = None
    indices = pd.Series()

def get_recommendations(item_name, top_n=10):
    # Use the pre-computed global variables
    # 1. Check if item exists in our pre-computed index mapping
    if item_name not in indices:
        print(f"Item '{item_name}' not found.")
        return pd.DataFrame() # Return an empty DataFrame

    # 2. Get the index of the item from the mapping
    item_index = indices[item_name]

    # 3. Get the cosine similarity scores for this item
    similar_items = list(enumerate(cosine_similarities_content[item_index]))

    # 4. Sort similar items by similarity score
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)

    # 5. Get the top N most similar items (excluding the item itself at index 0)
    top_similar_items = similar_items[1:top_n+1]

    # 6. Get the indices of the top similar items
    recommended_item_indices = [x[0] for x in top_similar_items]

    # 7. Get the details of the top similar items
    columns_to_return = ['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']
    
    # Check which of the desired columns actually exist in the DataFrame
    available_columns = [col for col in columns_to_return if col in train_data.columns]
    
    recommended_items_details = train_data.iloc[recommended_item_indices][available_columns]

    return recommended_items_details

def search_recommendations(query, top_n=10):
    # Use the pre-computed global variables
    
    # 1. Transform the search query using the fitted vectorizer
    # The [query] makes it a list, which transform() expects
    query_vector = tfidf_vectorizer.transform([query])
    
    # 2. Calculate cosine similarity between the query and all item tags
    #    .flatten() converts the (1, N) matrix into a simple array
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix_content).flatten()
    
    # 3. Get the indices of the top_n most similar items
    #    .argsort() gives indices from smallest to largest score
    #    [-top_n:] gets the N highest scores' indices
    #    [::-1] reverses them to be largest to smallest
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]
    
    # 4. Filter out results with 0.0 similarity (no match)
    top_scores = cosine_similarities[top_indices]
    realistic_indices = [i for i, score in zip(top_indices, top_scores) if score > 0]
    
    # If no items match at all
    if not realistic_indices:
        return pd.DataFrame()

    # 5. Get the details of the top similar items
    columns_to_return = ['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']
    available_columns = [col for col in columns_to_return if col in train_data.columns]
    
    recommended_items_details = train_data.iloc[realistic_indices][available_columns]

    return recommended_items_details

# ----------------- Home Page -----------------
@main.route('/')
def index():
    try:
        # Read the entire CSV
        df_full = pd.read_csv('models/trending_products.csv')

        df = df_full.head(8) 

        image_files = [f'images/p{i+1}.jpeg' for i in range(len(df))]

        trending_products = []
        for i, row in df.iterrows():
            trending_products.append({
                "Name": row['Name'],
                "Brand": row['Brand'],
                "Rating": row['Rating'],
                "ReviewCount": row['ReviewCount'],
                "ImageURL": image_files[i] 
            })
    
    except FileNotFoundError:
        flash('Error: Could not find trending products data file.', 'error')
        trending_products = [] 
    except Exception as e:
        flash(f'An error occurred loading products: {e}', 'error')
        trending_products = [] 
    
    return render_template('index.html', trending_products=trending_products)

@main.route('/api/recommend/<product_name>')
def api_recommend(product_name):
    
    # 1. Get 5 recommendations using your existing function
    recommendations_df = get_recommendations(product_name, top_n=5)
    
    # 2. Convert to a list of dictionaries
    results_list = recommendations_df.to_dict('records')
            
    for product in results_list:
        product['ImageURL_full'] = product.get('ImageURL', 'http://path/to/default.jpg')
    
    # 4. Return the data as JSON
    return jsonify(recommendations=results_list)

@main.route('/app')
def main_app():
    return render_template('app.html') 

# In app/routes.py

@main.route('/recommend', methods=['POST'])
def recommend():
    # Get form data
    product_name_query = request.form['product_name']
    
    try:
        top_n = int(request.form['top_n'])
    except (ValueError, TypeError):
        top_n = 5 # Default
    
    top_n = max(1, min(10, top_n))

    # --- DECISION LOGIC ---
    if product_name_query in indices:
        # Strategy 1: Item-to-Item
        recommendations_df = get_recommendations(product_name_query, top_n)
    else:
        recommendations_df = search_recommendations(product_name_query, top_n)
    
    results_list = []
    if not recommendations_df.empty:
        # Drop duplicates and convert to list
        recommendations_df = recommendations_df.drop_duplicates(subset=['Name'])
        results_list = recommendations_df.to_dict('records')
    
    if results_list:
        # ONLY flash success if we actually have results
        flash(f'Showing {len(results_list)} results for "{product_name_query}"', 'success')
    else:
        # ONLY flash danger if results_list is empty
        flash(f"Sorry, we couldn't find any relevant products for '{product_name_query}'.", 'danger')

    # Render the page
    return render_template('app.html', 
                           results=results_list, 
                           searched_item=product_name_query)

# ---------------- Signup -----------------
@main.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        flash('Email already registered.', 'danger')
        return redirect(url_for('main.index'))

    # Create new user
    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    flash('User registered successfully!', 'success')
    return redirect(url_for('main.index'))

# ----------------- Signin -----------------
@main.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        flash(f'Welcome {user.username}!', 'success')
    else:
        flash('Invalid email or password.', 'danger')

    return redirect(url_for('main.index'))

# ----------------- Logout -----------------
@main.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index'))


# ----------------- Settings -----------------
@main.route('/settings', methods=['POST'])
def settings():
    if 'user_id' not in session:
        flash('Please login to access settings.', 'error')
        return redirect(url_for('main.index'))

    user = User.query.get(session['user_id'])

    # Update user info
    user.username = request.form.get('username', user.username)
    user.email = request.form.get('email', user.email)
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('main.index'))
