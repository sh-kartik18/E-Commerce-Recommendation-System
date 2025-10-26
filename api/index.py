from app import create_app

# Create your Flask app
app = create_app()

# For local testing (optional)
if __name__ == "__main__":
    app.run(debug=True)

# Vercel handler (for deployment)
def handler(event, context):
    return app(event, context)
