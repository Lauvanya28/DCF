from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register the webhook route
    from .routes import webhook_bp
    app.register_blueprint(webhook_bp)

    return app

# Add this block to expose the app object directly
app = create_app()

if __name__ == '__main__':
    app.run()
