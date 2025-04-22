from app import create_app

app = create_app()  # Usado pelo Gunicorn

if __name__ == '__main__':
    app.run(debug=True)