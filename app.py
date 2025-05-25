from flask import Flask, render_template, request
from scraper import scrape_mercadolibre, scrape_falabella_selenium

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query")
    resultados = []

    if query:
        resultados = scrape_mercadolibre(query) + scrape_falabella_selenium(query)

    return render_template("index.html", query=query, resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
