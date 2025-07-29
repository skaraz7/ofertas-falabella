from flask import Flask, render_template
import json
import os
from pathlib import Path

app = Flask(__name__)

def calcular_estadisticas(datos):
    """Calcula estadisticas de los datos"""
    total_productos = sum(len(cat["productos"]) for cat in datos.values())
    total_categorias = len(datos)
    
    max_descuento = 0
    for categoria in datos.values():
        for producto in categoria["productos"]:
            descuento = producto.get("descuento_porcentaje", 0)
            if descuento > max_descuento:
                max_descuento = descuento
    
    return {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'max_descuento': max_descuento
    }

@app.route("/")
def home():
    json_path = os.path.join("data", "ofertas_falabella_completo.json")
    with open(json_path, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    stats = calcular_estadisticas(datos)
    
    return render_template("ofertas.html", 
                         datos=datos,
                         stats=stats,
                         total_productos=stats['total_productos'],
                         total_categorias=stats['total_categorias'],
                         max_descuento=stats['max_descuento'])

def generar_html_estatico():
    """Genera HTML estático para GitHub Pages"""
    json_path = os.path.join("data", "ofertas_falabella_completo.json")
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"No se encontro el archivo: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    stats = calcular_estadisticas(datos)
    
    with app.app_context():
        html_content = render_template('ofertas.html',
                                     datos=datos,
                                     stats=stats,
                                     total_productos=stats['total_productos'],
                                     total_categorias=stats['total_categorias'],
                                     max_descuento=stats['max_descuento'])
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML estático generado: index.html")
    print(f"Productos: {stats['total_productos']} | Categorías: {stats['total_categorias']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        generar_html_estatico()
    else:
        app.run(host="0.0.0.0", port=5000)
