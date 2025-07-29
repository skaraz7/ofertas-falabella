import json
import os

def generar_html_premium(datos_categorias):
    """Genera HTML ultra profesional con modo oscuro y paginación"""
    total_productos = sum(len(cat["productos"]) for cat in datos_categorias.values())
    
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Ofertas Premium Falabella Perú</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
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
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: all 0.3s ease;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            padding: 60px 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
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
        
        .nav-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}
        
        .nav-btn {{
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
        
        .nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-medium);
            border-color: var(--primary-color);
        }}
        
        .nav-btn.active {{
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
        
        .main-content {{
            padding: 40px 0;
        }}
        
        .categoria-section {{
            display: none;
        }}
        
        .categoria-section.active {{
            display: block;
        }}
        
        .productos-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 24px;
            margin-bottom: 40px;
        }}
        
        .producto-card {{
            background: var(--bg-card);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: var(--shadow-light);
            border: 1px solid var(--border-color);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            opacity: 0;
            transform: translateY(20px);
        }}
        
        .producto-card.visible {{
            opacity: 1;
            transform: translateY(0);
        }}
        
        .producto-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: var(--shadow-large);
        }}
        
        .imagen-container {{
            position: relative;
            overflow: hidden;
            height: 280px;
        }}
        
        .producto-imagen {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s ease;
        }}
        
        .producto-card:hover .producto-imagen {{
            transform: scale(1.1);
        }}
        
        .descuento-badge {{
            position: absolute;
            top: 16px;
            right: 16px;
            background: linear-gradient(135deg, var(--error-color), #dc2626);
            color: white;
            padding: 8px 14px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.85rem;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        .producto-info {{
            padding: 24px;
        }}
        
        .producto-marca {{
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .producto-nombre {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 16px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .precios {{
            margin-bottom: 20px;
        }}
        
        .precio-oferta {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--error-color);
            display: block;
            margin-bottom: 4px;
        }}
        
        .precio-original {{
            font-size: 1rem;
            color: var(--text-secondary);
            text-decoration: line-through;
            font-weight: 500;
        }}
        
        .producto-link {{
            display: block;
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: white;
            padding: 14px 20px;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }}
        
        .producto-link:hover {{
            background: linear-gradient(135deg, var(--primary-dark), #3730a3);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
        }}
        
        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            margin: 40px 0;
            flex-wrap: wrap;
        }}
        
        .pagination button {{
            background: var(--bg-card);
            border: 2px solid var(--border-color);
            color: var(--text-primary);
            padding: 12px 16px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            min-width: 44px;
        }}
        
        .pagination button:hover:not(:disabled) {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}
        
        .pagination button.active {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}
        
        .pagination button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .pagination-info {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin: 0 16px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2.5rem;
            }}
            
            .controls-grid {{
                grid-template-columns: 1fr;
                gap: 16px;
                text-align: center;
            }}
            
            .nav-buttons {{
                justify-content: center;
            }}
            
            .productos-grid {{
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 20px;
            }}
            
            .producto-info {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="header-content">
                <h1>🔥 Ofertas Premium</h1>
                <p>Las mejores ofertas de Falabella Perú con diseño profesional y navegación avanzada</p>
            </div>
        </div>
    </div>
    
    <div class="controls">
        <div class="container">
            <div class="controls-grid">
                <div class="nav-buttons">
{generar_botones_navegacion(datos_categorias)}
                </div>
                <button class="theme-toggle" onclick="toggleTheme()">
                    <i class="fas fa-moon" id="theme-icon"></i>
                </button>
                <div class="stats">
                    <h3 id="stats-text">
                        <i class="fas fa-fire" style="color: var(--error-color);"></i>
                        <span>{total_productos} Productos Disponibles</span>
                    </h3>
                </div>
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="container">
{generar_secciones_con_paginacion(datos_categorias)}
        </div>
    </div>
    
    <script>
        const PRODUCTOS_POR_PAGINA = 24;
        let currentCategory = Object.keys({dict([(k, v) for k, v in datos_categorias.items()])})[0];
        let currentPages = {{}};
        
        // Inicializar páginas actuales
        {'; '.join([f'currentPages["{k}"] = 1' for k in datos_categorias.keys()])};
        
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
        
        function mostrarCategoria(categoriaId) {{
            currentCategory = categoriaId;
            
            // Ocultar todas las secciones
            document.querySelectorAll('.categoria-section').forEach(section => {{
                section.classList.remove('active');
            }});
            
            // Mostrar sección seleccionada
            document.getElementById(categoriaId).classList.add('active');
            
            // Actualizar botones
            document.querySelectorAll('.nav-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Actualizar estadísticas
            const categorias = {dict([(f'"{k}"', len(v["productos"])) for k, v in datos_categorias.items()])};
            const count = categorias[categoriaId];
            document.getElementById('stats-text').innerHTML = `
                <i class="fas fa-fire" style="color: var(--error-color);"></i>
                <span>${{count}} Productos Disponibles</span>
            `;
            
            // Mostrar página actual
            mostrarPagina(categoriaId, currentPages[categoriaId] || 1);
        }}
        
        function mostrarPagina(categoriaId, pagina) {{
            currentPages[categoriaId] = pagina;
            
            const productos = document.querySelectorAll(`#${{categoriaId}} .producto-card`);
            const totalProductos = productos.length;
            const totalPaginas = Math.ceil(totalProductos / PRODUCTOS_POR_PAGINA);
            
            const inicio = (pagina - 1) * PRODUCTOS_POR_PAGINA;
            const fin = inicio + PRODUCTOS_POR_PAGINA;
            
            // Ocultar todos los productos
            productos.forEach((producto, index) => {{
                if (index >= inicio && index < fin) {{
                    producto.style.display = 'block';
                    setTimeout(() => producto.classList.add('visible'), index * 50);
                }} else {{
                    producto.style.display = 'none';
                    producto.classList.remove('visible');
                }}
            }});
            
            // Actualizar paginación
            actualizarPaginacion(categoriaId, pagina, totalPaginas, totalProductos);
            
            // Scroll suave al inicio
            document.querySelector('.main-content').scrollIntoView({{ behavior: 'smooth' }});
        }}
        
        function actualizarPaginacion(categoriaId, paginaActual, totalPaginas, totalProductos) {{
            const paginationContainer = document.querySelector(`#${{categoriaId}} .pagination`);
            
            const inicio = (paginaActual - 1) * PRODUCTOS_POR_PAGINA + 1;
            const fin = Math.min(paginaActual * PRODUCTOS_POR_PAGINA, totalProductos);
            
            paginationContainer.innerHTML = `
                <button onclick="mostrarPagina('${{categoriaId}}', 1)" ${{paginaActual === 1 ? 'disabled' : ''}}>
                    <i class="fas fa-angle-double-left"></i>
                </button>
                <button onclick="mostrarPagina('${{categoriaId}}', ${{paginaActual - 1}})" ${{paginaActual === 1 ? 'disabled' : ''}}>
                    <i class="fas fa-angle-left"></i>
                </button>
                
                ${{generarBotonesPagina(paginaActual, totalPaginas, categoriaId)}}
                
                <button onclick="mostrarPagina('${{categoriaId}}', ${{paginaActual + 1}})" ${{paginaActual === totalPaginas ? 'disabled' : ''}}>
                    <i class="fas fa-angle-right"></i>
                </button>
                <button onclick="mostrarPagina('${{categoriaId}}', ${{totalPaginas}})" ${{paginaActual === totalPaginas ? 'disabled' : ''}}>
                    <i class="fas fa-angle-double-right"></i>
                </button>
                
                <div class="pagination-info">
                    Mostrando ${{inicio}}-${{fin}} de ${{totalProductos}} productos
                </div>
            `;
        }}
        
        function generarBotonesPagina(actual, total, categoria) {{
            let botones = '';
            let inicio = Math.max(1, actual - 2);
            let fin = Math.min(total, actual + 2);
            
            if (inicio > 1) {{
                botones += `<button onclick="mostrarPagina('${{categoria}}', 1)">1</button>`;
                if (inicio > 2) botones += '<span>...</span>';
            }}
            
            for (let i = inicio; i <= fin; i++) {{
                botones += `<button onclick="mostrarPagina('${{categoria}}', ${{i}})" ${{i === actual ? 'class="active"' : ''}}>${{i}}</button>`;
            }}
            
            if (fin < total) {{
                if (fin < total - 1) botones += '<span>...</span>';
                botones += `<button onclick="mostrarPagina('${{categoria}}', ${{total}})">${{total}}</button>`;
            }}
            
            return botones;
        }}
        
        // Inicializar primera categoría
        document.addEventListener('DOMContentLoaded', () => {{
            mostrarCategoria(currentCategory);
        }});
    </script>
</body>
</html>
"""
    
    return html_content

def generar_botones_navegacion(datos_categorias):
    botones = []
    for i, (categoria_key, categoria_data) in enumerate(datos_categorias.items()):
        info = categoria_data["info"]
        count = len(categoria_data["productos"])
        active_class = "active" if i == 0 else ""
        botones.append(f'<button class="nav-btn {active_class}" onclick="mostrarCategoria(\'{categoria_key}\')"><i class="{info["icono"]}"></i> {info["nombre"]} <span style="opacity: 0.7;">({count})</span></button>')
    return "\n".join(botones)

def generar_secciones_con_paginacion(datos_categorias):
    secciones = []
    for i, (categoria_key, categoria_data) in enumerate(datos_categorias.items()):
        active_class = "active" if i == 0 else ""
        productos = categoria_data["productos"]
        
        seccion = f'<div id="{categoria_key}" class="categoria-section {active_class}">\n'
        seccion += '<div class="productos-grid">\n'
        
        for producto in productos:
            imagen_src = producto["imagen"] if producto["imagen"] else "https://via.placeholder.com/320x280/6366f1/ffffff?text=Sin+Imagen"
            descuento = producto.get("descuento_porcentaje", 0)
            
            boton_link = ''
            if producto["link"] and producto["link"] != "#":
                boton_link = f'<a href="{producto["link"]}" target="_blank" class="producto-link"><i class="fas fa-shopping-cart"></i> Ver Oferta</a>'
            else:
                boton_link = '<span class="producto-link" style="background: #ccc; cursor: not-allowed;"><i class="fas fa-times"></i> Sin enlace</span>'
            
            seccion += f"""
                <div class="producto-card">
                    <div class="imagen-container">
                        <img src="{imagen_src}" alt="{producto['nombre']}" class="producto-imagen" onerror="this.src='https://via.placeholder.com/320x280/6366f1/ffffff?text=Sin+Imagen'">
                        <div class="descuento-badge">-{descuento}%</div>
                    </div>
                    <div class="producto-info">
                        <div class="producto-marca">{producto['marca']}</div>
                        <div class="producto-nombre">{producto['nombre']}</div>
                        <div class="precios">
                            <span class="precio-oferta">{producto['precio_oferta']}</span>
                            <span class="precio-original">{producto['precio_original']}</span>
                        </div>
                        {boton_link}
                    </div>
                </div>
"""
        
        seccion += '</div>\n'
        seccion += '<div class="pagination"></div>\n'
        seccion += '</div>\n'
        secciones.append(seccion)
    
    return "\n".join(secciones)

# Ejecución principal
if __name__ == "__main__":
    print("GENERANDO HTML DESDE JSON")
    
    # Leer JSON
    json_path = "ofertas_falabella_completo.json"
    if not os.path.exists(json_path):
        print(f"Error: No se encontro el archivo {json_path}")
        print("Ejecuta primero scraper_json.py para generar los datos")
        exit(1)
    
    with open(json_path, "r", encoding="utf-8") as f:
        datos_todas_categorias = json.load(f)
    
    # Generar HTML premium
    html_content = generar_html_premium(datos_todas_categorias)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML premium generado: index.html")
    
    total_productos = sum(len(cat["productos"]) for cat in datos_todas_categorias.values())
    print(f"\nHTML GENERADO: {total_productos} productos de {len(datos_todas_categorias)} categorias")
    
    # Resumen por categoría
    print("\nRESUMEN POR CATEGORIA:")
    for categoria_key, categoria_data in datos_todas_categorias.items():
        info = categoria_data["info"]
        count = len(categoria_data["productos"])
        print(f"  {info['nombre']}: {count} productos")