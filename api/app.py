import logging
import os

from apiflask import APIFlask
from flask_cors import CORS
from routes import v1

# Set logging level to INFO
logging.getLogger().setLevel(logging.INFO)

# Create an instance of APIFlask
app = APIFlask(
    __name__,
    title="Aldus API",
    version="1.0",
    spec_path="/openapi.yml",
    docs_ui="swagger-ui",
)

# Configure APIFlask to sync the local OpenAPI specification
app.servers = [{"url": "https://aldus-api.alleslabs.dev"}]
app.config["SYNC_LOCAL_SPEC"] = True
app.config["LOCAL_SPEC_PATH"] = os.path.join(app.root_path, "openapi.json")

# Register the v1 blueprint with the app
app.register_blueprint(v1.v1_bp, url_prefix="/v1")

# Enable CORS for the app
CORS(app)

if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG", True),
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", 8080)),
    )
