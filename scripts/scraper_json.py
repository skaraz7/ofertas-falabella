from playwright.sync_api import sync_playwright
import time
import json
import os

# Configuración de categorías
CATEGORIAS = {
    "descuentos_cmr": {
        "nombre": "🔥 Descuentos CMR",
        "url": "https://www.falabella.com.pe/falabella-pe/collection/descuentos-cmr",
        "descuento_minimo": 30,
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
        time.sleep(0.35)
        posicion_actual += paso_scroll
        
        if posicion_actual % (paso_scroll * 2) == 0:
            time.sleep(0.5)
    
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(0.9)
    
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.4)
    
    print("Scroll completado")

def scrape_categoria(categoria_key, categoria_info):
    print(f"\n{'='*60}")
    print(f"SCRAPING: {categoria_info['nombre']}")
    print(f"URL: {categoria_info['url']}")
    print(f"Descuento mínimo: {categoria_info['descuento_minimo']}%")
    print(f"{'='*60}")
    
    base_url = categoria_info['url']
    descuento_minimo = categoria_info['descuento_minimo']
    
    # Detectar si estamos en un entorno CI/CD
    is_ci = any([
        os.getenv('CI'),
        os.getenv('GITHUB_ACTIONS'),
        os.getenv('GITLAB_CI'),
        os.getenv('TRAVIS'),
        os.getenv('JENKINS_URL'),
        os.getenv('CIRCLECI'),
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
                page.goto(url, timeout=27000)
                print(f"Esperando carga inicial...")
                time.sleep(2.7)
                
                scroll_humano(page)
                
                print(f"Esperando 13.5 segundos adicionales...")
                time.sleep(13.5)
                
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
                        page.wait_for_selector(selector, timeout=13500)
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
                        
                        # Extraer precios usando data-internet-price y data-normal-price
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
                                        
                                        # Solo aplicar filtro de 30% a descuentos_cmr
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

# Ejecución principal
if __name__ == "__main__":
    print("🚀 INICIANDO SCRAPING DE FALABELLA - SOLO JSON")
    datos_todas_categorias = scrape_todas_categorias()
    
    # Guardar JSON unificado
    with open("ofertas_falabella_completo.json", "w", encoding="utf-8") as f:
        json.dump(datos_todas_categorias, f, ensure_ascii=False, indent=4)
    print(f"✓ JSON unificado guardado: ofertas_falabella_completo.json")
    
    total_productos = sum(len(cat["productos"]) for cat in datos_todas_categorias.values())
    print(f"\n🎉 PROCESO COMPLETADO: {total_productos} productos extraídos de {len(CATEGORIAS)} categorías")
    
    # Resumen por categoría
    print("\n📊 RESUMEN POR CATEGORÍA:")
    for categoria_key, categoria_data in datos_todas_categorias.items():
        info = categoria_data["info"]
        count = len(categoria_data["productos"])
        print(f"  {info['icono']} {info['nombre']}: {count} productos")