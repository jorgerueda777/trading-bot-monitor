# Despliegue SIN GitHub - PythonAnywhere

**Tiempo**: 20 minutos  
**Dificultad**: ⭐⭐ (sin comandos, todo visual)  
**Costo**: $0 gratis

---

## ✅ Lo que voy a hacer por ti

Voy a preparar un archivo ZIP con todo tu código listo para subir.

---

## 📦 PASO 1: Preparar el código (YO LO HAGO)

Voy a crear un ZIP con todo.

## 🌐 PASO 2: Crear cuenta en PythonAnywhere (TÚ)

1. Ve a: https://www.pythonanywhere.com/registration/register/beginner/
2. Llena el formulario:
   - Username: elige uno (ej: `jorgerueda777`)
   - Email: tu email
   - Password: crea una
3. Verifica tu email
4. Login en: https://www.pythonanywhere.com/login/

## 📤 PASO 3: Subir archivos (TÚ)

1. En PythonAnywhere, ve a "Files"
2. Crea carpeta: `trading-bot`
3. Entra a la carpeta
4. Sube el ZIP que te voy a crear
5. Clic derecho → Extract

## ⚙️ PASO 4: Instalar dependencias (TÚ)

1. Ve a "Consoles" → "Bash"
2. Ejecuta:
```bash
cd trading-bot
pip install --user -r requirements.txt
```

## 🔑 PASO 5: Configurar variables

1. En la consola Bash:
```bash
nano .env
```

2. Pega tus variables:
```
TELEGRAM_API_ID=tu_valor
TELEGRAM_API_HASH=tu_valor
TELEGRAM_PHONE=tu_valor
SOURCE_GROUP_IDS=tu_valor
DEST_CHANNEL_ID=tu_valor
BINANCE_API_KEY=tu_valor
BINANCE_API_SECRET=tu_valor
```

3. Guardar: `Ctrl+X` → `Y` → `Enter`

## 🚀 PASO 6: Ejecutar bot

En la consola Bash:
```bash
python monitor_grupos.py
```

---

## ⚠️ LIMITACIONES de PythonAnywhere Free:

- Se suspende después de 3 meses
- No corre 24/7 (necesitas "Always-on task" = $5/mes)
- Necesitas mantener la consola abierta

---

## 🎯 MEJOR ALTERNATIVA

Honestamente, **GitHub + Render es MÁS FÁCIL** que PythonAnywhere.

Solo necesitas:
1. Crear repositorio en GitHub (2 clics)
2. Obtener token (3 clics)
3. Ejecutar 3 comandos que YO YA PREPARÉ

**¿Quieres que te guíe con GitHub?** Es más rápido y funciona mejor.
