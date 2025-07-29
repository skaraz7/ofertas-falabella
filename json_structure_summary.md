# Resumen de Estructura JSON - Ofertas Falabella

## Estructura General
```json
{
  "categoria_key": {
    "info": {
      "nombre": "string",
      "url": "string", 
      "descuento_minimo": number,
      "icono": "string"
    },
    "productos": [
      {
        "nombre": "string",
        "marca": "string", 
        "precio_oferta": "string",
        "precio_original": "string",
        "descuento_porcentaje": number,
        "link": "string",
        "imagen": "string"
      }
    ]
  }
}
```

## Categorías Disponibles
1. **descuentos_cmr** - 🔥 Descuentos CMR (fas fa-fire) - ~100+ productos
2. **moda_accesorios** - 👗 Moda y Accesorios (fas fa-tshirt) - ~200+ productos  
3. **moda_mujer** - 👠 Moda Mujer (fas fa-female) - ~50+ productos
4. **zapatos_mujer** - 👡 Zapatos Mujer (fas fa-shoe-prints) - ~30+ productos
5. **calzado_masculino** - 👞 Calzado Masculino (fas fa-shoe-prints) - ~30+ productos

## Total Estimado: ~450+ productos en 5 categorías

## Campos de Producto
- **nombre**: Título del producto
- **marca**: Marca del producto
- **precio_oferta**: Precio con descuento (formato "S/ X,XXX")
- **precio_original**: Precio original (formato "S/ X,XXX") 
- **descuento_porcentaje**: Porcentaje de descuento (number)
- **link**: URL del producto en Falabella
- **imagen**: URL de la imagen del producto