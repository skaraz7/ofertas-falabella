from playwright.sync_api import sync_playwright
import time
import json
import math
import os

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
    """Simula scroll humano ultra rápido"""
    print("Scroll ultra rápido...")
    
    altura_total = page.evaluate("document.body.scrollHeight")
    altura_ventana = page.evaluate("window.innerHeight")
    
    posicion_actual = 0
    paso_scroll = altura_ventana // 2
    
    while posicion_actual < altura_total:
        page.evaluate(f"window.scrollTo(0, {posicion_actual})")
        time.sleep(0.35)  # 10% menos tiempo
        posicion_actual += paso_scroll
        
        if posicion_actual % (paso_scroll * 2) == 0:
            time.sleep(0.5)  # 10% menos tiempo
    
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(0.9)  # 10% menos tiempo
    
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.4)  # 10% menos tiempo
    
    print("Scroll completado")

def scrape_categoria(categoria_key, categoria_info):
    print(f"\n{'='*60}")
    print(f"SCRAPING: {categoria_info['nombre']}")
    print(f"URL: {categoria_info['url']}")
    print(f"Descuento mínimo: {categoria_info['descuento_minimo']}%")
    print(f"{'='*60}")
    
    base_url = categoria_info['url']
    descuento_minimo = categoria_info['descuento_minimo']
    
    # Detectar si estamos en un entorno CI/CD (GitHub Actions, etc.)
    is_ci = any([
        os.getenv('CI'),  # Variable común en CI/CD
        os.getenv('GITHUB_ACTIONS'),  # GitHub Actions específico
        os.getenv('GITLAB_CI'),  # GitLab CI
        os.getenv('TRAVIS'),  # Travis CI
        os.getenv('JENKINS_URL'),  # Jenkins
        os.getenv('CIRCLECI'),  # CircleCI
    ])
    
    headless_mode = is_ci
    if headless_mode:
        print("🤖 Modo headless detectado (CI/CD)")
    else:
        print("🖥️ Modo con ventana (desarrollo local)")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless_mode)
        page = browser.new_page()
        
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        productos_por_pagina = {}
        
        print("\n=== FASE 1: Carga inicial de páginas ===")
        for pagina in range(1, 6):
            if pagina == 1:
                url = base_url
            else:
                url = f"{base_url}?page={pagina}"
            
            print(f"\n--- Procesando página {pagina} ---")
            
            try:
                page.goto(url, timeout=27000)  # 10% menos timeout
                print(f"Esperando carga inicial...")
                time.sleep(2.7)  # 10% menos tiempo
                
                scroll_humano(page)
                
                print(f"Esperando 13.5 segundos adicionales...")
                time.sleep(13.5)  # 10% menos tiempo
                
                selectores = [
                    '[data-testid="pod-card"]',
                    '.pod',
                    'div[class*="pod"]',
                    '.search-results-4-grid',
                    '.grid-pod'
                ]
                
                productos_cargados = False
                for selector in selectores:
                    try:
                        page.wait_for_selector(selector, timeout=13500)  # 10% menos
                        print(f"Productos encontrados con selector: {selector}")
                        productos_cargados = True
                        break
                    except:
                        continue
                
                if not productos_cargados:
                    print(f"No se pudieron cargar productos en página {pagina}, saltando...")
                    continue

                scroll_humano(page)

                selectores_productos = [
                    '[data-testid="pod-card"]',
                    '.pod',
                    'div[class*="pod"]',
                    '.search-results-4-grid > div',
                    '.grid-pod',
                    'article',
                    'div[data-automation-id*="product"]'
                ]
                
                productos = []
                for selector in selectores_productos:
                    productos = page.query_selector_all(selector)
                    if productos:
                        print(f"Usando selector: {selector}")
                        break

                print(f"Encontrados {len(productos)} productos en página {pagina}")
                productos_por_pagina[pagina] = []
                
                for i, producto in enumerate(productos):
                    try:
                        # Extraer marca
                        marca_elem = producto.query_selector('.pod-title') or producto.query_selector('b.title-rebrand') or producto.query_selector('[data-testid="pod-title"]')
                        marca = marca_elem.inner_text().strip() if marca_elem else "Sin marca"
                        
                        # Extraer nombre del producto
                        nombre_elem = producto.query_selector('.pod-subTitle') or producto.query_selector('b.subTitle-rebrand') or producto.query_selector('[id*="pod-displaySubTitle"]')
                        nombre = nombre_elem.inner_text().strip() if nombre_elem else "Sin nombre"
                        
                        # NUEVO: Extraer precios usando data-internet-price y data-normal-price
                        precio_oferta = None
                        precio_original = None
                        
                        # Buscar precio de oferta (data-internet-price)
                        precio_oferta_elem = producto.query_selector('li[data-internet-price]')
                        if precio_oferta_elem:
                            precio_oferta_value = precio_oferta_elem.get_attribute('data-internet-price')
                            if precio_oferta_value:
                                precio_oferta = f"S/ {precio_oferta_value}"
                        
                        # Si no encuentra data-internet-price, usar método anterior
                        if not precio_oferta:
                            precio_oferta_elem = producto.query_selector('.copy10.high') or producto.query_selector('span.copy10:first-child') or producto.query_selector('.copy10')
                            precio_oferta = precio_oferta_elem.inner_text().strip() if precio_oferta_elem else "Sin precio"
                        
                        # Buscar precio original (data-normal-price)
                        precio_original_elem = producto.query_selector('li[data-normal-price]')
                        if precio_original_elem:
                            precio_original_value = precio_original_elem.get_attribute('data-normal-price')
                            if precio_original_value:
                                precio_original = f"S/ {precio_original_value}"
                        
                        # Si no encuentra data-normal-price, usar método anterior
                        if not precio_original:
                            precio_original_elem = producto.query_selector('.copy10.medium') or producto.query_selector('li.prices-1 span.copy10') or producto.query_selector('.pod-price-regular')
                            precio_original = precio_original_elem.inner_text().strip() if precio_original_elem else None
                        
                        # Extraer link
                        link_elem = producto.query_selector('a.pod-link') or producto.query_selector('a[data-pod]') or producto.query_selector('a')
                        href = None
                        
                        try:
                            tag_name = producto.evaluate('el => el.tagName.toLowerCase()')
                            if tag_name == 'a':
                                href = producto.get_attribute('href')
                        except:
                            pass
                        
                        if not href and link_elem:
                            href = link_elem.get_attribute('href')
                        
                        link = None
                        if href and href != '#' and 'javascript:' not in href:
                            if href.startswith('http'):
                                link = href
                            elif href.startswith('/'):
                                link = "https://www.falabella.com.pe" + href
                        
                        # Extraer imagen
                        imagen = None
                        section_elem = producto.query_selector('section.layout_grid-view')
                        if section_elem:
                            picture_elem = section_elem.query_selector('picture')
                            if picture_elem:
                                img_elem = picture_elem.query_selector('img')
                                if img_elem:
                                    imagen = img_elem.get_attribute('src')
                        
                        if not imagen:
                            img_elem = (producto.query_selector('picture img') or 
                                       producto.query_selector('img[id*="testId-pod-image"]') or 
                                       producto.query_selector('img[src*="falabella"]') or 
                                       producto.query_selector('img'))
                            
                            if img_elem:
                                imagen = img_elem.get_attribute('src')
                        
                        if imagen and imagen.startswith('http') and 'falabella' in imagen:
                            pass
                        else:
                            imagen = None

                        # Solo agregar productos EN OFERTA
                        if nombre != "Sin nombre" and precio_oferta != "Sin precio" and precio_oferta:
                            try:
                                precio_oferta_num = float(precio_oferta.replace('S/', '').replace(',', '').strip())
                                precio_original_num = None
                                descuento_porcentaje = 0
                                
                                if precio_original:
                                    precio_original_num = float(precio_original.replace('S/', '').replace(',', '').strip())
                                    
                                    if precio_original_num > precio_oferta_num:
                                        descuento_porcentaje = round(((precio_original_num - precio_oferta_num) / precio_original_num) * 100)
                                        
                                        # CORREGIDO: Solo aplicar filtro de 30% a descuentos_cmr
                                        if categoria_key == "descuentos_cmr" and descuento_porcentaje < descuento_minimo:
                                            continue
                                    else:
                                        continue
                                else:
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
                                continue
                            
                    except Exception as e:
                        print(f"Error procesando producto {i+1} en página {pagina}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error procesando página {pagina}: {str(e)}")
                continue
        
        # FASE 2: Reintento para productos sin imagen (tiempo reducido)
        print("\n=== FASE 2: Reintento para productos sin imagen ===")
        max_reintentos = 2
        
        for intento in range(max_reintentos):
            productos_sin_imagen = []
            
            for pagina, productos in productos_por_pagina.items():
                for producto in productos:
                    if not producto['imagen']:
                        productos_sin_imagen.append(producto)
            
            if not productos_sin_imagen:
                print("✅ Todos los productos tienen imagen")
                break
                
            print(f"\nIntento {intento + 1}: {len(productos_sin_imagen)} productos sin imagen")
            
            paginas_a_revisar = {}
            for producto in productos_sin_imagen:
                pagina = producto['pagina']
                if pagina not in paginas_a_revisar:
                    paginas_a_revisar[pagina] = []
                paginas_a_revisar[pagina].append(producto)
            
            for pagina, productos_faltantes in paginas_a_revisar.items():
                if pagina == 1:
                    url = base_url
                else:
                    url = f"{base_url}?page={pagina}"
                
                print(f"\nRevisando página {pagina} - {len(productos_faltantes)} productos sin imagen")
                
                try:
                    page.goto(url, timeout=27000)
                    time.sleep(2.7)
                    scroll_humano(page)
                    time.sleep(13.5)
                    
                    for selector in selectores_productos:
                        productos_actuales = page.query_selector_all(selector)
                        if productos_actuales:
                            break
                    
                    for producto_faltante in productos_faltantes:
                        indice = producto_faltante['indice']
                        if indice < len(productos_actuales):
                            producto_actual = productos_actuales[indice]
                            
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
    import webbrowser
    import os
    
    print("🚀 INICIANDO SCRAPING ULTRA RÁPIDO DE FALABELLA")
    datos_todas_categorias = scrape_todas_categorias()
    
    # Guardar JSON unificado
    with open("ofertas_falabella_completo.json", "w", encoding="utf-8") as f:
        json.dump(datos_todas_categorias, f, ensure_ascii=False, indent=4)
    print(f"✓ JSON unificado guardado: ofertas_falabella_completo.json")
    
    # Generar HTML premium
    html_content = generar_html_premium(datos_todas_categorias)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✓ HTML premium generado: index.html")
    
    # Solo abrir navegador en entorno local
    is_ci = any([
        os.getenv('CI'),
        os.getenv('GITHUB_ACTIONS'),
        os.getenv('GITLAB_CI'),
        os.getenv('TRAVIS'),
        os.getenv('JENKINS_URL'),
        os.getenv('CIRCLECI'),
    ])
    
    if not is_ci:
        try:
            html_path = os.path.abspath("index.html")
            webbrowser.open(f"file://{html_path}")
            print("✓ Abriendo en navegador...")
        except Exception as e:
            print(f"⚠️ No se pudo abrir el navegador: {e}")
    else:
        print("ℹ️ Navegador omitido en entorno CI/CD")
    
    total_productos = sum(len(cat["productos"]) for cat in datos_todas_categorias.values())
    print(f"\n🎉 PROCESO COMPLETADO: {total_productos} productos extraídos de {len(CATEGORIAS)} categorías")
    
    # Resumen por categoría
    print("\n📊 RESUMEN POR CATEGORÍA:")
    for categoria_key, categoria_data in datos_todas_categorias.items():
        info = categoria_data["info"]
        count = len(categoria_data["productos"])
        print(f"  {info['icono']} {info['nombre']}: {count} productos")