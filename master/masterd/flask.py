app = Flask(__name__)

@app.route("/")
def index():
    return "Nothing here - DNS-manager"
