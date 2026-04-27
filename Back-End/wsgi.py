from app.factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
else:
    # For Gunicorn production deployment
    application = app
