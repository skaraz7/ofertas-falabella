from flask import Flask, render_template
import json
import os

app = Flask(__name__)

def cargar_datos():
    """Carga datos con múltiples rutas de fallback para Render.com"""
    rutas_posibles = [
        "data/ofertas_falabella_completo.json",
        "ofertas_falabella_completo.json",
        "scripts/ofertas_falabella_completo.json"
    ]
    
    for ruta in rutas_posibles:
        try:
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
            continue
    
    # Datos de ejemplo para Render.com si no hay JSON
    return {
        "ejemplo": {
            "info": {
                "nombre": "🔥 Ofertas de Ejemplo",
                "icono": "fas fa-fire"
            },
            "productos": [
                {
                    "nombre": "Producto de Ejemplo",
                    "marca": "EJEMPLO",
                    "precio_oferta": "S/ 99.90",
                    "precio_original": "S/ 199.90",
                    "descuento_porcentaje": 50,
                    "link": "#",
                    "imagen": None
                }
            ]
        }
    }

def calcular_estadisticas(datos):
    """Calcula estadisticas de los datos"""
    if not datos:
        return {'total_productos': 0, 'total_categorias': 0, 'max_descuento': 0}
    
    total_productos = sum(len(cat.get("productos", [])) for cat in datos.values())
    total_categorias = len(datos)
    
    max_descuento = 0
    for categoria in datos.values():
        for producto in categoria.get("productos", []):
            descuento = producto.get("descuento_porcentaje", 0)
            if descuento > max_descuento:
                max_descuento = descuento
    
    return {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'max_descuento': max_descuento
    }

@app.route("/")
def index():
    """Ruta principal optimizada para Render.com"""
    datos = cargar_datos()
    stats = calcular_estadisticas(datos)
    
    return render_template("ofertas.html", 
                         datos=datos,
                         stats=stats,
                         total_productos=stats['total_productos'],
                         total_categorias=stats['total_categorias'],
                         max_descuento=stats['max_descuento'])

def generar_html_estatico():
    """Genera HTML estático para GitHub Pages (compatible con Render.com)"""
    datos = cargar_datos()
    stats = calcular_estadisticas(datos)
    
    # Configurar Flask para generación estática solo si es necesario
    try:
        app.config['SERVER_NAME'] = 'localhost'
    except:
        pass
    
    try:
        with app.app_context():
            with app.test_request_context():
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
    except Exception as e:
        print(f"Error generando HTML estático: {e}")
        print("Continuando sin generar archivo estático...")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        generar_html_estatico()
    else:
        # Configuración optimizada para Render.com
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=False)
