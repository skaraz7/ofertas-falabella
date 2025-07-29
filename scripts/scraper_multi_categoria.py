from playwright.sync_api import sync_playwright
import time
import json

# Configuración de categorías
CATEGORIAS = {
    "descuentos_cmr": {
        "nombre": "🔥 Descuentos CMR",
        "url": "https://www.falabella.com.pe/falabella-pe/collection/descuentos-cmr",
        "descuento_minimo": 30,  # Solo productos con +30% descuento
        "icono": "fas fa-fire"
    },
    "moda_accesorios": {
        "nombre": "👗 Moda y Accesorios",
        "url": "https://www.falabella.com.pe/falabella-pe/collection/ous-moda-y-accesorios",
        "descuento_minimo": 0,
        "icono": "fas fa-tshirt"
    },
    "moda_mujer": {
        "nombre": "👠 Moda Mujer",
        "url": "https://www.falabella.com.pe/falabella-pe/category/cat4100462/Moda-Mujer",
        "descuento_minimo": 0,
        "icono": "fas fa-female"
    },
    "zapatos_mujer": {
        "nombre": "👡 Zapatos Mujer",
        "url": "https://www.falabella.com.pe/falabella-pe/category/cat1470526/Zapatos-Mujer",
        "descuento_minimo": 0,
        "icono": "fas fa-shoe-prints"
    },
    "joyas_mujer": {
        "nombre": "💎 Joyas Mujer",
        "url": "https://www.falabella.com.pe/falabella-pe/category/cat4350568/Joyas-mujer",
        "descuento_minimo": 0,
        "icono": "fas fa-gem"
    },
    "maquillaje": {
        "nombre": "💄 Maquillaje",
        "url": "https://www.falabella.com.pe/falabella-pe/category/cat560663/Maquillaje",
        "descuento_minimo": 0,
        "icono": "fas fa-palette"
    }
}

def scroll_humano(page):
    """Simula scroll humano rápido para cargar imágenes"""
    print("Realizando scroll humano rápido...")
    
    altura_total = page.evaluate("document.body.scrollHeight")
    altura_ventana = page.evaluate("window.innerHeight")
    
    posicion_actual = 0
    paso_scroll = altura_ventana // 2  # Pasos más grandes
    
    while posicion_actual < altura_total:
        page.evaluate(f"window.scrollTo(0, {posicion_actual})")
        time.sleep(0.4)  # 50% menos tiempo
        posicion_actual += paso_scroll
        
        if posicion_actual % (paso_scroll * 2) == 0:
            time.sleep(0.6)  # 50% menos tiempo
    
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)  # 50% menos tiempo
    
    # Scroll rápido al inicio
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)
    
    print("Scroll completado")

def scrape_categoria(categoria_key, categoria_info):
    print(f"\n{'='*60}")
    print(f"SCRAPING: {categoria_info['nombre']}")
    print(f"URL: {categoria_info['url']}")
    print(f"Descuento mínimo: {categoria_info['descuento_minimo']}%")
    print(f"{'='*60}")
    
    base_url = categoria_info['url']
    descuento_minimo = categoria_info['descuento_minimo']
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Configurar user agent para evitar detección
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        productos_por_pagina = {}  # {pagina: [productos]}
        
        # FASE 1: Cargar todas las páginas con espera larga
        print("\n=== FASE 1: Carga inicial de páginas ===")
        for pagina in range(1, 6):  # 5 páginas
            if pagina == 1:
                url = base_url
            else:
                url = f"{base_url}?page={pagina}"
            
            print(f"\n--- Procesando página {pagina} ---")
            print(f"URL: {url}")
            
            try:
                page.goto(url, timeout=30000)  # 50% menos timeout
                print(f"Esperando carga inicial...")
                time.sleep(3)  # 50% menos tiempo
                
                scroll_humano(page)
                
                print(f"Esperando 15 segundos adicionales...")
                time.sleep(15)  # 50% menos tiempo
                
                # Esperar a que carguen los productos
                productos_cargados = False
                selectores = [
                    '[data-testid="pod-card"]',
                    '.pod',
                    'div[class*="pod"]',
                    '.search-results-4-grid',
                    '.grid-pod'
                ]
                
                for selector in selectores:
                    try:
                        page.wait_for_selector(selector, timeout=15000)
                        print(f"Productos encontrados con selector: {selector}")
                        productos_cargados = True
                        break
                    except:
                        continue
                
                if not productos_cargados:
                    print(f"No se pudieron cargar productos en página {pagina}, saltando...")
                    continue

                # Scroll humano adicional
                scroll_humano(page)

                # Buscar productos
                productos = []
                selectores_productos = [
                    '[data-testid="pod-card"]',
                    '.pod',
                    'div[class*="pod"]',
                    '.search-results-4-grid > div',
                    '.grid-pod',
                    'article',
                    'div[data-automation-id*="product"]'
                ]
                
                for selector in selectores_productos:
                    productos = page.query_selector_all(selector)
                    if productos:
                        print(f"Usando selector: {selector}")
                        break

                print(f"Encontrados {len(productos)} productos en página {pagina}")
                productos_por_pagina[pagina] = []
                
                # Procesar productos de esta página
                for i, producto in enumerate(productos):
                    try:
                        # Extraer marca
                        marca_elem = producto.query_selector('.pod-title') or producto.query_selector('b.title-rebrand') or producto.query_selector('[data-testid="pod-title"]')
                        marca = marca_elem.inner_text().strip() if marca_elem else "Sin marca"
                        
                        # Extraer nombre del producto
                        nombre_elem = producto.query_selector('.pod-subTitle') or producto.query_selector('b.subTitle-rebrand') or producto.query_selector('[id*="pod-displaySubTitle"]')
                        nombre = nombre_elem.inner_text().strip() if nombre_elem else "Sin nombre"
                        
                        # Extraer precio de oferta (clase high)
                        precio_oferta_elem = producto.query_selector('.copy10.high') or producto.query_selector('span.copy10:first-child') or producto.query_selector('.copy10')
                        precio_oferta = precio_oferta_elem.inner_text().strip() if precio_oferta_elem else "Sin precio"
                        
                        # Extraer precio original/normal (clase medium)
                        precio_original_elem = producto.query_selector('.copy10.medium') or producto.query_selector('li.prices-1 span.copy10') or producto.query_selector('.pod-price-regular')
                        precio_original = precio_original_elem.inner_text().strip() if precio_original_elem else None
                        
                        # Extraer link - buscar el elemento a que contiene el producto
                        link_elem = producto.query_selector('a.pod-link') or producto.query_selector('a[data-pod]') or producto.query_selector('a')
                        href = None
                        
                        # Si el producto mismo es un elemento a
                        try:
                            tag_name = producto.evaluate('el => el.tagName.toLowerCase()')
                            if tag_name == 'a':
                                href = producto.get_attribute('href')
                        except:
                            pass
                        
                        # Si no encontró href, buscar en elementos hijos
                        if not href and link_elem:
                            href = link_elem.get_attribute('href')
                        
                        link = None
                        if href and href != '#' and 'javascript:' not in href:
                            if href.startswith('http'):
                                link = href
                            elif href.startswith('/'):
                                link = "https://www.falabella.com.pe" + href
                        
                        # Extraer imagen siguiendo la estructura de Falabella
                        imagen = None
                        
                        # Buscar en section > picture > img
                        section_elem = producto.query_selector('section.layout_grid-view')
                        if section_elem:
                            picture_elem = section_elem.query_selector('picture')
                            if picture_elem:
                                img_elem = picture_elem.query_selector('img')
                                if img_elem:
                                    imagen = img_elem.get_attribute('src')
                        
                        # Si no encontró, buscar directamente
                        if not imagen:
                            img_elem = (producto.query_selector('picture img') or 
                                       producto.query_selector('img[id*="testId-pod-image"]') or 
                                       producto.query_selector('img[src*="falabella"]') or 
                                       producto.query_selector('img'))
                            
                            if img_elem:
                                imagen = img_elem.get_attribute('src')
                        
                        # Validar y limpiar la URL de imagen
                        if imagen and imagen.startswith('http') and 'falabella' in imagen:
                            # La imagen ya es válida
                            pass
                        else:
                            imagen = None

                        # Solo agregar productos EN OFERTA
                        if nombre != "Sin nombre" and precio_oferta != "Sin precio":
                            # Extraer valores numéricos de precios
                            try:
                                precio_oferta_num = float(precio_oferta.replace('S/', '').replace(',', '').strip())
                                precio_original_num = None
                                descuento_porcentaje = 0
                                
                                if precio_original:
                                    precio_original_num = float(precio_original.replace('S/', '').replace(',', '').strip())
                                    
                                    # Solo agregar si hay descuento real
                                    if precio_original_num > precio_oferta_num:
                                        descuento_porcentaje = round(((precio_original_num - precio_oferta_num) / precio_original_num) * 100)
                                        
                                        # Filtro especial para descuentos CMR (solo +30%)
                                        if descuento_porcentaje < descuento_minimo:
                                            continue
                                    else:
                                        # No hay oferta real, saltar producto
                                        continue
                                else:
                                    # Sin precio original, saltar
                                    continue
                                
                                producto_data = {
                                    "nombre": nombre,
                                    "marca": marca,
                                    "precio_oferta": precio_oferta,
                                    "precio_original": precio_original,
                                    "descuento_porcentaje": descuento_porcentaje,
                                    "link": link,
                                    "imagen": imagen,
                                    "categoria": categoria_key,
                                    "pagina": pagina,
                                    "indice": i
                                }
                                productos_por_pagina[pagina].append(producto_data)
                                print(f"Página {pagina} - Producto {i+1}: {marca} - {nombre[:30]}... [IMG: {'Sí' if imagen else 'No'}] [DESC: {descuento_porcentaje}%]")
                                
                            except ValueError:
                                # Error al convertir precios, saltar
                                continue
                            
                    except Exception as e:
                        print(f"Error procesando producto {i+1} en página {pagina}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error procesando página {pagina}: {str(e)}")
                continue
        
        # FASE 2: Reintento para productos sin imagen
        print("\n=== FASE 2: Reintento para productos sin imagen ===")
        max_reintentos = 2
        
        for intento in range(max_reintentos):
            productos_sin_imagen = []
            
            # Identificar productos sin imagen
            for pagina, productos in productos_por_pagina.items():
                for producto in productos:
                    if not producto['imagen']:
                        productos_sin_imagen.append(producto)
            
            if not productos_sin_imagen:
                print("✅ Todos los productos tienen imagen")
                break
                
            print(f"\nIntento {intento + 1}: {len(productos_sin_imagen)} productos sin imagen")
            
            # Agrupar por página
            paginas_a_revisar = {}
            for producto in productos_sin_imagen:
                pagina = producto['pagina']
                if pagina not in paginas_a_revisar:
                    paginas_a_revisar[pagina] = []
                paginas_a_revisar[pagina].append(producto)
            
            # Revisar cada página
            for pagina, productos_faltantes in paginas_a_revisar.items():
                if pagina == 1:
                    url = base_url
                else:
                    url = f"{base_url}?page={pagina}"
                
                print(f"\nRevisando página {pagina} - {len(productos_faltantes)} productos sin imagen")
                
                try:
                    page.goto(url, timeout=30000)  # 50% menos timeout
                    print(f"Esperando carga inicial...")
                    time.sleep(3)  # 50% menos tiempo
                    
                    scroll_humano(page)
                    
                    print(f"Esperando 15 segundos adicionales...")
                    time.sleep(15)  # 50% menos tiempo
                    
                    # Buscar productos nuevamente
                    for selector in selectores_productos:
                        productos_actuales = page.query_selector_all(selector)
                        if productos_actuales:
                            break
                    
                    # Actualizar productos sin imagen
                    for producto_faltante in productos_faltantes:
                        indice = producto_faltante['indice']
                        if indice < len(productos_actuales):
                            producto_actual = productos_actuales[indice]
                            
                            # Extraer imagen nuevamente
                            imagen = None
                            section_elem = producto_actual.query_selector('section.layout_grid-view')
                            if section_elem:
                                picture_elem = section_elem.query_selector('picture')
                                if picture_elem:
                                    img_elem = picture_elem.query_selector('img')
                                    if img_elem:
                                        imagen = img_elem.get_attribute('src')
                            
                            if not imagen:
                                img_elem = (producto_actual.query_selector('picture img') or 
                                           producto_actual.query_selector('img[id*="testId-pod-image"]') or 
                                           producto_actual.query_selector('img[src*="falabella"]') or 
                                           producto_actual.query_selector('img'))
                                if img_elem:
                                    imagen = img_elem.get_attribute('src')
                            
                            if imagen and imagen.startswith('http') and 'falabella' in imagen:
                                producto_faltante['imagen'] = imagen
                                print(f"✅ Imagen encontrada para: {producto_faltante['nombre'][:30]}")
                            else:
                                print(f"❌ Sin imagen: {producto_faltante['nombre'][:30]}")
                                
                except Exception as e:
                    print(f"Error en reintento página {pagina}: {str(e)}")
        
        # Consolidar resultados finales
        todos_los_resultados = []
        for pagina, productos in productos_por_pagina.items():
            for producto in productos:
                # Remover campos auxiliares
                resultado = {
                    "nombre": producto["nombre"],
                    "marca": producto["marca"],
                    "precio_oferta": producto["precio_oferta"],
                    "precio_original": producto["precio_original"],
                    "descuento_porcentaje": producto["descuento_porcentaje"],
                    "link": producto["link"],
                    "imagen": producto["imagen"]
                }
                todos_los_resultados.append(resultado)
        
        # Estadísticas finales
        con_imagen = sum(1 for p in todos_los_resultados if p['imagen'])
        sin_imagen = len(todos_los_resultados) - con_imagen
        
        browser.close()
        print(f"\n=== RESUMEN {categoria_info['nombre']} ===")
        print(f"Total productos: {len(todos_los_resultados)}")
        print(f"Con imagen: {con_imagen}")
        print(f"Sin imagen: {sin_imagen}")
        return todos_los_resultados

def scrape_todas_categorias():
    print("🚀 INICIANDO SCRAPING MASIVO DE FALABELLA")
    print(f"Categorías a procesar: {len(CATEGORIAS)}")
    
    todos_los_productos = {}
    
    for categoria_key, categoria_info in CATEGORIAS.items():
        try:
            productos = scrape_categoria(categoria_key, categoria_info)
            todos_los_productos[categoria_key] = {
                "info": categoria_info,
                "productos": productos
            }
            print(f"✅ {categoria_info['nombre']}: {len(productos)} productos")
        except Exception as e:
            print(f"❌ Error en {categoria_info['nombre']}: {str(e)}")
            todos_los_productos[categoria_key] = {
                "info": categoria_info,
                "productos": []
            }
    
    return todos_los_productos

def generar_botones_navegacion(datos_categorias):
    botones = []
    for i, (categoria_key, categoria_data) in enumerate(datos_categorias.items()):
        info = categoria_data["info"]
        count = len(categoria_data["productos"])
        active_class = "active" if i == 0 else ""
        botones.append(f'<button class="nav-btn {active_class}" onclick="mostrarCategoria(\'{categoria_key}\')"><i class="{info["icono"]}"></i> {info["nombre"]} ({count})</button>')
    return "\n".join(botones)

def generar_secciones_categorias(datos_categorias):
    secciones = []
    for i, (categoria_key, categoria_data) in enumerate(datos_categorias.items()):
        active_class = "active" if i == 0 else ""
        productos = categoria_data["productos"]
        
        seccion = f'<div id="{categoria_key}" class="categoria-section {active_class}">\n<div class="productos-grid">\n'
        
        for producto in productos:
            imagen_src = producto["imagen"] if producto["imagen"] else "https://via.placeholder.com/320x280/667eea/ffffff?text=Sin+Imagen"
            descuento = producto.get("descuento_porcentaje", 0)
            
            boton_link = ''
            if producto["link"] and producto["link"] != "#":
                boton_link = f'<a href="{producto["link"]}" target="_blank" class="producto-link"><i class="fas fa-shopping-cart"></i>Ver Oferta en Falabella</a>'
            else:
                boton_link = '<span class="producto-link" style="background: #ccc; cursor: not-allowed;"><i class="fas fa-times"></i>Sin enlace disponible</span>'
            
            seccion += f"""
                <div class="producto-card">
                    <div class="imagen-container">
                        <img src="{imagen_src}" alt="{producto['nombre']}" class="producto-imagen" onerror="this.src='https://via.placeholder.com/320x280/667eea/ffffff?text=Sin+Imagen'">
                        <div class="descuento-badge">-{descuento}%</div>
                    </div>
                    <div class="producto-info">
                        <div class="producto-marca">{producto['marca']}</div>
                        <div class="producto-nombre">{producto['nombre']}</div>
                        <div class="precios">
                            <div class="precio-container">
                                <span class="precio-oferta">{producto['precio_oferta']}</span>
                            </div>
                            <div class="precio-original">{producto['precio_original']}</div>
                        </div>
                        {boton_link}
                    </div>
                </div>
"""
        
        seccion += '</div>\n</div>\n'
        secciones.append(seccion)
    
    return "\n".join(secciones)

def generar_html_multi_categoria(datos_categorias):
    """Genera HTML profesional con múltiples categorías y navegación"""
    total_productos = sum(len(cat["productos"]) for cat in datos_categorias.values())
    
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Ofertas Falabella Perú - Todas las Categorías</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }}
        
        .header h1 {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
            font-weight: 300;
        }}
        
        .nav-panel {{
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .nav-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }}
        
        .nav-btn {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .nav-btn:hover, .nav-btn.active {{
            background: linear-gradient(135deg, #5a67d8, #6b46c1);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }}
        
        .stats {{
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 40px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .stats h3 {{
            color: #2d3748;
            font-size: 1.5rem;
            font-weight: 600;
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
            gap: 25px;
        }}
        
        .producto-card {{
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255,255,255,0.2);
            position: relative;
        }}
        
        .producto-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }}
        
        .imagen-container {{
            position: relative;
            overflow: hidden;
        }}
        
        .producto-imagen {{
            width: 100%;
            height: 280px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .producto-card:hover .producto-imagen {{
            transform: scale(1.05);
        }}
        
        .descuento-badge {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(135deg, #ff416c, #ff4757);
            color: white;
            padding: 8px 12px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.9rem;
            box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        .producto-info {{
            padding: 25px;
        }}
        
        .producto-marca {{
            color: #718096;
            font-size: 0.9rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .producto-nombre {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 15px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .precios {{
            margin-bottom: 20px;
        }}
        
        .precio-container {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }}
        
        .precio-oferta {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #e53e3e;
        }}
        
        .precio-original {{
            font-size: 1.1rem;
            color: #a0aec0;
            text-decoration: line-through;
            font-weight: 500;
        }}
        
        .producto-link {{
            display: block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 12px 20px;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .producto-link:hover {{
            background: linear-gradient(135deg, #5a67d8, #6b46c1);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        
        .producto-link i {{
            margin-right: 8px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
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
    <div class="container">
        <div class="header">
            <h1>🔥 Ofertas Falabella Perú</h1>
            <p>Las mejores ofertas en todas las categorías - Actualizadas en tiempo real</p>
        </div>
        
        <div class="nav-panel">
            <div class="nav-buttons">
{generar_botones_navegacion(datos_categorias)}
            </div>
        </div>
        
        <div class="stats">
            <h3 id="stats-text"><i class="fas fa-fire" style="color: #e53e3e; margin-right: 10px;"></i>{total_productos} Productos en Oferta Disponibles</h3>
        </div>
        
{generar_secciones_categorias(datos_categorias)}
    </div>
    
    <script>
        // Navegación entre categorías
        function mostrarCategoria(categoriaId) {{
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
            const categorias = {dict([(k, len(v["productos"])) for k, v in datos_categorias.items()])};
            const count = categorias[categoriaId];
            document.getElementById('stats-text').innerHTML = `<i class="fas fa-fire" style="color: #e53e3e; margin-right: 10px;"></i>${{count}} Productos en Oferta Disponibles`;
            
            // Re-animar cards
            setTimeout(() => {{
                initCardAnimations();
            }}, 100);
        }}
        
        // Animación de entrada para las cards
        function initCardAnimations() {{
            const cards = document.querySelectorAll('.categoria-section.active .producto-card');
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }});
            
            cards.forEach(card => {{
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(card);
            }});
        }}
        
        // Inicializar animaciones al cargar
        document.addEventListener('DOMContentLoaded', initCardAnimations);
    </script>
</body>
</html>
"""
    
    return html_content

# Ejecución principal
if __name__ == "__main__":
    import webbrowser
    import os
    
    print("🚀 INICIANDO SCRAPING MASIVO DE FALABELLA")
    datos_todas_categorias = scrape_todas_categorias()
    
    # Guardar JSON unificado
    with open("ofertas_falabella_completo.json", "w", encoding="utf-8") as f:
        json.dump(datos_todas_categorias, f, ensure_ascii=False, indent=4)
    print(f"✓ JSON unificado guardado: ofertas_falabella_completo.json")
    
    # Generar HTML multi-categoría
    html_content = generar_html_multi_categoria(datos_todas_categorias)
    with open("ofertas_falabella.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✓ HTML multi-categoría generado: ofertas_falabella.html")
    
    # Abrir en navegador
    html_path = os.path.abspath("ofertas_falabella.html")
    webbrowser.open(f"file://{html_path}")
    print("✓ Abriendo en navegador...")
    
    total_productos = sum(len(cat["productos"]) for cat in datos_todas_categorias.values())
    print(f"\n🎉 PROCESO COMPLETADO: {total_productos} productos extraídos de {len(CATEGORIAS)} categorías")
    
    # Resumen por categoría
    print("\n📊 RESUMEN POR CATEGORÍA:")
    for categoria_key, categoria_data in datos_todas_categorias.items():
        info = categoria_data["info"]
        count = len(categoria_data["productos"])
        print(f"  {info['icono']} {info['nombre']}: {count} productos")