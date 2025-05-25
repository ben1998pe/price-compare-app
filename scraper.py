import requests
from bs4 import BeautifulSoup

# -------------------------
# 🔍 MERCADO LIBRE
# -------------------------
def scrape_mercadolibre(query):
    print(f"\n📦 Resultados de MercadoLibre para: {query}")

    url = f"https://listado.mercadolibre.com.pe/{query.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Error al obtener resultados de MercadoLibre")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("li.ui-search-layout__item")

    resultados = []

    for item in items[:10]:  # Máximo 10 productos
        try:
            titulo = item.select_one("a.poly-component__title").get_text(strip=True)
            precio = item.select_one("div.poly-price__current span.andes-money-amount__fraction").get_text(strip=True)
            link = item.select_one("a.poly-component__title")["href"]

            resultados.append({
                "titulo": titulo,
                "precio": f"S/ {precio}",
                "link": link,
                "origen": "MercadoLibre"
            })

            print(f"{titulo}\nS/ {precio} — {link}\n")

        except Exception as e:
            print("⚠️ Producto con error:", e)
            continue

    return resultados

# -------------------------
# 🛍️ FALABELLA (SELENIUM)
# -------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_falabella_selenium(query, max_scrolls=3):
    print(f"\n🛍️ Resultados de Falabella para: {query}")

    options = Options()
    options.add_argument("--headless=new")  # Comenta para ver el navegador
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.falabella.com.pe/falabella-pe/search?Ntt={query.replace(' ', '+')}")
    time.sleep(3)

    for _ in range(max_scrolls):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

    productos = driver.find_elements(By.CSS_SELECTOR, "a.pod-link")
    resultados = []

    for item in productos[:10]:
        try:
            titulo = item.find_element(By.CLASS_NAME, "pod-subTitle").text.strip()
            precio = item.find_element(By.CSS_SELECTOR, "li[data-event-price] span").text.strip()
            link = item.get_attribute("href")

            resultados.append({
                "titulo": titulo,
                "precio": precio,
                "link": link,
                "origen": "Falabella"
            })

            print(f"{titulo}\n{precio} — {link}\n")

        except Exception as e:
            print("⚠️ Producto con error:", e)
            continue

    driver.quit()
    return resultados

# -------------------------
# 🚀 PRUEBA DIRECTA
# -------------------------
if __name__ == "__main__":
    producto = input("🔍 Ingresa el producto a buscar: ")

    # MercadoLibre
    ml_resultados = scrape_mercadolibre(producto)

    # Falabella
    falabella_resultados = scrape_falabella_selenium(producto)

    # Total
    total = len(ml_resultados) + len(falabella_resultados)
    print(f"\n✅ Total encontrados: {total} productos")

    print("\n📦 Productos combinados:\n")
    for r in ml_resultados + falabella_resultados:
        print(f"[{r['origen']}] {r['titulo']}\n{r['precio']} — {r['link']}\n")
