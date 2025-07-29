import json
import os

def cargar_json():
    with open('scripts/ofertas_falabella_completo.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generar_html():
    datos = cargar_json()
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Ofertas Falabella Perú</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary-color: #6366f1;
            --primary-dark: #4f46e5;
            --secondary-color: #ec4899;
            --accent-color: #06b6d4;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --shadow-light: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --shadow-medium: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-large: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }}
        
        [data-theme="dark"] {{
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --border-color: #475569;
            --shadow-light: 0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px 0 rgba(0, 0, 0, 0.2);
            --shadow-medium: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            --shadow-large: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.6;
            transition: all 0.3s ease;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            padding: 60px 0;
            text-align: center;
            position: relative;
            overflow: hidden;
            margin-bottom: 0;
        }}
        
        .header-content {{
            position: relative;
            z-index: 2;
        }}

        .header h1 {{
            font-size: 3.5rem;
            font-weight: 800;
            color: white;
            margin-bottom: 15px;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            letter-spacing: -0.02em;
        }}

        .header p {{
            font-size: 1.3rem;
            color: rgba(255,255,255,0.9);
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }}

        .controls {{
            background: var(--bg-secondary);
            padding: 30px 0;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }}
        
        .controls-grid {{
            display: grid;
            grid-template-columns: 1fr auto auto;
            gap: 20px;
            align-items: center;
        }}
        
        .filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .filter-btn {{
            background: var(--bg-card);
            color: var(--text-primary);
            border: 2px solid var(--border-color);
            padding: 12px 20px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: var(--shadow-light);
        }}

        .filter-btn:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-medium);
            border-color: var(--primary-color);
        }}
        
        .filter-btn.active {{
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: white;
            border-color: var(--primary-color);
            box-shadow: var(--shadow-medium);
        }}
        
        .theme-toggle {{
            background: var(--bg-card);
            border: 2px solid var(--border-color);
            color: var(--text-primary);
            padding: 12px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1.1rem;
            box-shadow: var(--shadow-light);
        }}
        
        .theme-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-medium);
        }}

        .category-section {{
            margin-bottom: 40px;
            background: var(--bg-card);
            border-radius: 20px;
            padding: 30px;
            box-shadow: var(--shadow-light);
            border: 1px solid var(--border-color);
        }}

        .category-header {{
            display: flex;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--border-color);
        }}

        .category-header i {{
            font-size: 2rem;
            margin-right: 15px;
            color: var(--primary-color);
        }}

        .category-header h2 {{
            font-size: 1.8rem;
            color: var(--text-primary);
        }}

        .products-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
            margin-bottom: 40px;
        }}
        
        .products-container {{
            position: relative;
        }}
        
        .product-page {{
            display: none;
        }}
        
        .product-page.active {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
        }}

        .product-card {{
            background: var(--bg-card);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--shadow-light);
            border: 1px solid var(--border-color);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}

        .product-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--shadow-large);
        }}

        .product-image {{
            width: 100%;
            height: 280px;
            object-fit: contain;
            background: #ffffff;
            padding: 15px;
            border-bottom: 1px solid #f1f5f9;
            transition: transform 0.3s ease;
        }}
        
        .product-card:hover .product-image {{
            transform: scale(1.05);
        }}

        .product-info {{
            padding: 20px;
        }}

        .product-brand {{
            font-size: 0.8rem;
            color: #666;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .product-name {{
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 15px;
            line-height: 1.4;
            color: #333;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .product-prices {{
            margin-bottom: 15px;
        }}

        .price-current {{
            font-size: 1.3rem;
            font-weight: bold;
            color: #ff6b6b;
        }}

        .price-original {{
            font-size: 0.9rem;
            color: #999;
            text-decoration: line-through;
            margin-left: 8px;
        }}

        .discount-badge {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: 800;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
            z-index: 10;
        }}

        .product-link {{
            display: inline-block;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            text-align: center;
            width: 100%;
        }}

        .product-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .stats {{
            background: var(--bg-card);
            padding: 25px;
            border-radius: 16px;
            text-align: center;
            box-shadow: var(--shadow-light);
            border: 1px solid var(--border-color);
        }}

        .stats h3 {{
            color: var(--text-primary);
            font-size: 1.4rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}

        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #ff6b6b;
        }}

        .stat-label {{
            font-size: 0.9rem;
            color: #666;
            margin-top: 5px;
        }}

        .hidden {{
            display: none;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}

            .header h1 {{
                font-size: 2rem;
            }}

            .products-grid {{
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
            }}

            .filters {{
                gap: 10px;
            }}

            .filter-btn {{
                padding: 10px 16px;
                font-size: 0.9rem;
            }}

            .stats {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="header-content">
                <h1>🔥 Ofertas Premium</h1>
                <p>Las mejores ofertas de Falabella Perú con diseño profesional</p>
            </div>
        </div>
    </div>
    
    <div class="controls">
        <div class="container">
            <div class="controls-grid">
                <div class="filters">
                    <button class="filter-btn active" data-category="all">
                        <i class="fas fa-th"></i> Todas las Categorías
                    </button>
{generar_filtros(datos)}
                </div>
                <button class="theme-toggle" onclick="toggleTheme()">
                    <i class="fas fa-moon" id="theme-icon"></i>
                </button>
                <div class="stats">
                    <h3>
                        <i class="fas fa-fire" style="color: var(--error-color);"></i>
                        <span>{sum(len(cat["productos"]) for cat in datos.values())} Productos Disponibles</span>
                    </h3>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div id="categories-container">
{generar_categorias(datos)}
        </div>
    </div>

    <script>
        let currentFilter = 'all';

        function toggleTheme() {{
            const body = document.body;
            const icon = document.getElementById('theme-icon');
            
            if (body.getAttribute('data-theme') === 'dark') {{
                body.removeAttribute('data-theme');
                icon.className = 'fas fa-moon';
                localStorage.setItem('theme', 'light');
            }} else {{
                body.setAttribute('data-theme', 'dark');
                icon.className = 'fas fa-sun';
                localStorage.setItem('theme', 'dark');
            }}
        }}
        
        // Cargar tema guardado
        if (localStorage.getItem('theme') === 'dark') {{
            document.body.setAttribute('data-theme', 'dark');
            document.getElementById('theme-icon').className = 'fas fa-sun';
        }}

        function filterByCategory(category) {{
            currentFilter = category;
            
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            document.querySelector(`[data-category="${{category}}"]`).classList.add('active');

            document.querySelectorAll('.category-section').forEach(section => {{
                if (category === 'all') {{
                    section.classList.remove('hidden');
                }} else {{
                    const sectionCategory = section.getAttribute('data-category');
                    if (sectionCategory === category) {{
                        section.classList.remove('hidden');
                    }} else {{
                        section.classList.add('hidden');
                    }}
                }}
            }});
        }}
        
        // Animaciones de entrada
        document.addEventListener('DOMContentLoaded', () => {{
            const cards = document.querySelectorAll('.product-card');
            cards.forEach((card, index) => {{
                setTimeout(() => {{
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }}, index * 50);
            }});
        }});
    </script>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def generar_filtros(datos):
    filtros = []
    for key, cat in datos.items():
        filtros.append(f'            <button class="filter-btn" data-category="{key}" onclick="filterByCategory(\'{key}\')">' + 
                      f'<i class="{cat["info"]["icono"]}"></i> {cat["info"]["nombre"]}</button>')
    return '\\n'.join(filtros) 

def generar_categorias(datos):
    categorias = []
    for key, cat in datos.items():
        productos_html = []
        for prod in cat["productos"]:
            img = prod["imagen"] or "https://via.placeholder.com/240x240?text=Sin+Imagen"
            productos_html.append(f'''            <div class="product-card">
                <div class="discount-badge">{prod["descuento_porcentaje"]}% OFF</div>
                <img src="{img}" alt="{prod["nombre"]}" class="product-image" onerror="this.src='https://via.placeholder.com/240x240?text=Sin+Imagen'">
                <div class="product-info">
                    <div class="product-brand">{prod["marca"]}</div>
                    <div class="product-name">{prod["nombre"]}</div>
                    <div class="product-prices">
                        <span class="price-current">{prod["precio_oferta"]}</span>
                        <span class="price-original">{prod["precio_original"]}</span>
                    </div>
                    <a href="{prod["link"]}" target="_blank" class="product-link">
                        <i class="fas fa-shopping-cart"></i> Ver Oferta
                    </a>
                </div>
            </div>''')
        
        categorias.append(f'''        <div class="category-section" data-category="{key}">
            <div class="category-header">
                <i class="{cat["info"]["icono"]}"></i>
                <h2>{cat["info"]["nombre"]}</h2>
            </div>
            <div class="products-grid">
{chr(10).join(productos_html)}
            </div>
        </div>''')
    
    return '\\n'.join(categorias)

if __name__ == "__main__":
    generar_html()
    print("HTML generado: index.html")