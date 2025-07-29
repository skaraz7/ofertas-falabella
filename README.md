# 🔥 Ofertas Falabella Perú

¡Las mejores ofertas de Falabella Perú actualizadas automáticamente!

## 📋 Estructura del Proyecto

El proyecto está dividido en dos partes principales:

### 1. 📊 Generación de Datos (JSON)
- **Archivo**: `scripts/scraper_json.py`
- **Función**: Extrae datos de productos de Falabella y los guarda en JSON
- **Ejecución**: Una vez al día via GitHub Actions
- **Salida**: `scripts/ofertas_falabella_completo.json`

### 2. 🎨 Generación de HTML
- **Archivo**: `scripts/generar_html.py`
- **Función**: Lee el JSON y genera el HTML con diseño premium
- **Ejecución**: Después del scraping, también via GitHub Actions
- **Salida**: `index.html` (compatible con GitHub Pages)

## 🚀 Uso

### Para Desarrollo Local

1. **Generar datos JSON**:
   ```bash
   cd scripts
   python scraper_json.py
   ```

2. **Generar HTML desde JSON**:
   ```bash
   cd scripts
   python generar_html_local.py
   ```
   (Este script también abre automáticamente el navegador)

### Para Producción (GitHub Actions)

El workflow se ejecuta automáticamente todos los días a las 6 AM UTC y:
1. Ejecuta el scraper para obtener datos frescos
2. Genera el HTML actualizado
3. Hace commit de ambos archivos
4. GitHub Pages sirve automáticamente el `index.html`

## 🌟 Características

- ✅ **Separación de responsabilidades**: Datos y presentación separados
- ✅ **GitHub Pages compatible**: HTML estático optimizado
- ✅ **Actualización automática**: Una vez al día sin intervención manual
- ✅ **Diseño responsive**: Funciona en móviles y desktop
- ✅ **Modo oscuro**: Toggle entre tema claro y oscuro
- ✅ **Paginación avanzada**: Navegación fluida entre productos
- ✅ **Filtros por categoría**: 6 categorías diferentes
- ✅ **Animaciones suaves**: Experiencia de usuario premium

## 📁 Archivos Principales

```
├── scripts/
│   ├── scraper_json.py          # Extrae datos y genera JSON
│   ├── generar_html.py          # Genera HTML desde JSON (CI/CD)
│   ├── generar_html_local.py    # Genera HTML y abre navegador (local)
│   └── ofertas_falabella_completo.json  # Datos de productos
├── .github/workflows/
│   └── auto-update.yml          # Workflow de GitHub Actions
├── index.html                   # Página web generada
└── README.md                    # Este archivo
```

## 🔧 Configuración

El proyecto no requiere configuración adicional. GitHub Actions maneja todo automáticamente.

## 📱 Acceso

La página está disponible en: [GitHub Pages URL]

---

**Desarrollado con ❤️ para encontrar las mejores ofertas de Falabella Perú**
