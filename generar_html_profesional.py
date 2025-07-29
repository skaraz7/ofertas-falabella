#!/usr/bin/env python3
"""
Generador HTML Profesional para Ofertas Falabella
Arquitectura separada: Python + Jinja2 Template + CSS + JS
"""

import json
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class GeneradorHTMLProfesional:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.templates_dir = self.base_dir / "templates"
        self.output_file = self.base_dir / "index.html"
        
        # Configurar Jinja2
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=True
        )
        
    def cargar_datos(self):
        """Carga los datos del archivo JSON"""
        json_path = self.data_dir / "ofertas_falabella_completo.json"
        
        if not json_path.exists():
            raise FileNotFoundError(f"No se encontro el archivo: {json_path}")
            
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def calcular_estadisticas(self, datos):
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
    
    def cargar_template(self):
        """Carga la plantilla Jinja2"""
        try:
            return self.jinja_env.get_template('ofertas.html')
        except Exception as e:
            raise FileNotFoundError(f"No se encontro la plantilla ofertas.html: {e}")
    
    def generar_html(self):
        """Metodo principal que genera el HTML completo usando Jinja2"""
        print("Iniciando generacion HTML profesional con Jinja2...")
        
        # Cargar datos
        print("Cargando datos...")
        datos = self.cargar_datos()
        
        # Calcular estadisticas
        stats = self.calcular_estadisticas(datos)
        print(f"Estadisticas: {stats['total_productos']} productos en {stats['total_categorias']} categorias")
        
        # Cargar plantilla Jinja2
        print("Cargando plantilla Jinja2...")
        template = self.cargar_template()
        
        # Renderizar con Jinja2
        print("Renderizando con Jinja2...")
        html_final = template.render(
            datos=datos,
            stats=stats,
            total_productos=stats['total_productos'],
            total_categorias=stats['total_categorias'],
            max_descuento=stats['max_descuento']
        )
        
        # Guardar archivo
        print("Guardando archivo HTML...")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_final)
        
        print(f"HTML generado exitosamente: {self.output_file}")
        print(f"Productos procesados: {stats['total_productos']}")
        print(f"Categorias: {stats['total_categorias']}")
        print(f"Descuento maximo: {stats['max_descuento']}%")
        
        return str(self.output_file)

def main():
    """Funcion principal"""
    try:
        generador = GeneradorHTMLProfesional()
        archivo_generado = generador.generar_html()
        
        # Preguntar si abrir en navegador
        respuesta = input("\nAbrir en navegador? (s/n): ").lower().strip()
        if respuesta in ['s', 'si', 'y', 'yes']:
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(archivo_generado)}")
            print("Abriendo en navegador...")
        
        print("\nGeneracion completada exitosamente!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())