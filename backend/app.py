import asyncio
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from .scraper import main
from .scraper import select_product
from .fetchDatabase import fetch_dbProduct


app = Flask(__name__, template_folder="../frontend/templates", static_url_path="/static", static_folder="../frontend/static")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape_amazon", methods=["POST"])
def scrape_amazon():
    data = request.get_json()
    amazon_website = data.get("amazon_website")
    product_name = data.get("product_name")
    # Call the main function from scraper.py
    product_data = asyncio.run(main(amazon_website, product_name))
    return jsonify({"products": product_data})

@app.route("/scrape_amazon_product", methods=["POST"])
def scrape_amazon_product():
    # Call the scrape product function from scraper.py
    data = request.get_json()
    data_asin = data.get("data_asin")
    product_page_url = f"https://www.amazon.com/dp/{data_asin}"
    asyncio.run(select_product(product_page_url))
    return jsonify("The request was successful")
    
@app.route("/fetch_product_history", methods=["GET"])
def fetch_product_history():
    product_ASIN = request.args.get("product_ASIN")
    search_result = fetch_dbProduct(product_ASIN)
    
    return jsonify(search_result)
    
    
if "__name__" == "__main__":
    app.run(debug=True)