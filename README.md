# Vaitengewon Validator - Diagnóstico de Integración WordPress

## Problemas Identificados y Soluciones

### 1. Error en requirements.txt
- **Problema**: `Flask-Corss` (error tipográfico)
- **Solución**: Corregido a `Flask-Cors`

### 2. Logging Mejorado
- Agregado logging detallado para diagnosticar problemas de comunicación
- Timestamps en todas las operaciones
- Logging de headers, IPs y datos recibidos

### 3. CORS Mejorado
- Configuración más permisiva para debugging (`Access-Control-Allow-Origin: *`)
- Manejo mejorado de preflight OPTIONS requests
- Headers CORS más completos

## Endpoints Disponibles

### Producción
- `GET /` - Página de inicio
- `POST /analizar-idea` - Endpoint principal para WordPress

### Diagnóstico
- `GET /health` - Verificación de salud del servicio
- `GET|POST /test-cors` - Prueba de CORS
- `POST /test-post` - Prueba de envío de datos POST

## Cómo Diagnosticar el Problema

### 1. Verificar que el servicio esté funcionando
```bash
curl https://tu-app.onrender.com/health
```

### 2. Probar CORS desde WordPress
```bash
curl -X OPTIONS https://tu-app.onrender.com/test-cors \
  -H "Origin: https://vaitengewon.club" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
```

### 3. Probar envío de datos POST
```bash
curl -X POST https://tu-app.onrender.com/test-post \
  -H "Content-Type: application/json" \
  -H "Origin: https://vaitengewon.club" \
  -d '{"wp_user_id": "123", "test": "data"}'
```

## Configuración WordPress

### JavaScript para probar desde WordPress
```javascript
// Prueba básica de conectividad
fetch('https://tu-app.onrender.com/health')
  .then(response => response.json())
  .then(data => console.log('Health check:', data))
  .catch(error => console.error('Error:', error));

// Prueba de CORS
fetch('https://tu-app.onrender.com/test-cors', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({test: 'data'})
})
.then(response => response.json())
.then(data => console.log('CORS test:', data))
.catch(error => console.error('CORS Error:', error));

// Prueba del endpoint real
fetch('https://tu-app.onrender.com/analizar-idea', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    wp_user_id: '123',
    idea: 'Mi idea de prueba'
  })
})
.then(response => response.json())
.then(data => console.log('Analizar idea:', data))
.catch(error => console.error('Analizar Error:', error));
```

## Posibles Problemas y Soluciones

### 1. Error de CORS
- **Síntoma**: Error en consola del navegador sobre CORS
- **Solución**: Verificar que WordPress esté enviando desde el dominio correcto

### 2. Error 404
- **Síntoma**: No se encuentra el endpoint
- **Solución**: Verificar la URL del servicio en Render

### 3. Error 500
- **Síntoma**: Error interno del servidor
- **Solución**: Revisar logs en Render Dashboard

### 4. Timeout
- **Síntoma**: La solicitud no responde
- **Solución**: Render gratuito tiene timeouts, considerar upgrade

## Próximos Pasos

1. Desplegar la versión actualizada en Render
2. Probar los endpoints de diagnóstico
3. Verificar logs en Render Dashboard
4. Probar desde WordPress con el código JavaScript proporcionado
5. Si persiste el problema, revisar configuración específica de WordPress

## Logs Importantes

Los logs ahora incluyen:
- Timestamp de cada solicitud
- Método HTTP utilizado
- Headers recibidos
- IP del cliente
- Datos recibidos (si los hay)
- Errores detallados
