# 🔐 Configurar UserBot para Leer Grupos Privados

## 🎯 Objetivo

Configurar un UserBot que:
1. Inicie sesión con TU cuenta de Telegram
2. Liste TODOS tus grupos (incluidos privados)
3. Lea el grupo de señales privado
4. Clasifique los eventos automáticamente
5. Envíe los resúmenes a @JR79_BOT

---

## 📋 Paso 1: Instalar Dependencias

```bash
pip install telethon
```

O actualizar todo:
```bash
pip install -r requirements.txt
```

---

## 🔑 Paso 2: Obtener Credenciales de Telegram

Para leer grupos con tu cuenta, necesitas credenciales de API.

### 2.1 Ve a my.telegram.org

1. **Abre tu navegador**
2. **Ve a:** https://my.telegram.org
3. **Inicia sesión** con tu número de teléfono de Telegram
4. **Ingresa el código** que recibes por Telegram

### 2.2 Crear una Aplicación

1. **Click en:** "API Development Tools"
2. **Rellena el formulario:**
   - App title: `Event Classifier`
   - Short name: `classifier`
   - Platform: `Desktop`
   - Description: `Bot clasificador de eventos`

3. **Click en "Create application"**

### 2.3 Copiar Credenciales

Verás algo como:
```
App api_id: 1234567
App api_hash: 1234567890abcdef1234567890abcdef
```

**¡IMPORTANTE! Copia estos valores.**

---

## ⚙️ Paso 3: Configurar .env

Abre el archivo `.env` y añade:

```bash
# Credenciales de Telegram API
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=1234567890abcdef1234567890abcdef
TELEGRAM_PHONE=+521234567890
```

**Reemplaza con tus datos:**
- `TELEGRAM_API_ID` → El número que copiaste (sin comillas)
- `TELEGRAM_API_HASH` → El hash que copiaste (sin comillas)
- `TELEGRAM_PHONE` → Tu número con código de país (+52 para México, +34 para España, etc.)

---

## 🚀 Paso 4: Ejecutar el Script

```bash
python telegram_user_client.py
```

### Primera vez:

Te pedirá:
1. **Código de verificación** (te llega por Telegram)
2. **Contraseña de 2FA** (si la tienes configurada)

Esto solo pasa la primera vez. Se guarda la sesión en `session_name.session`

---

## 📋 Paso 5: Listar tus Grupos

Cuando ejecutes el script, verás un menú:

```
============================================================
MENÚ - ¿Qué quieres hacer?
============================================================
1. Listar todos mis grupos y canales
2. Monitorear un grupo específico (leer eventos)
3. Salir
============================================================
```

**Elige opción 1** para ver todos tus grupos.

Verás algo como:
```
🔹 GRUPOS:
------------------------------------------------------------
1. Amigos
   ID: 1234567890
   Username: Sin username
   Tipo: Supergrupo

2. Señales Crypto VIP 🔒
   ID: 1987654321
   Username: Sin username
   Tipo: Supergrupo

3. Trading Avanzado
   ID: 1122334455
   Username: @trading_avanzado
   Tipo: Supergrupo
```

**Se guardará en:** `mis_grupos_telegram.txt`

---

## 🎯 Paso 6: Identificar tu Grupo de Señales

En el archivo `mis_grupos_telegram.txt` o en la terminal, busca el nombre de tu grupo de señales privado.

**Copia el ID** (el número).

Ejemplo:
```
Nombre: Señales Crypto VIP 🔒
ID: 1987654321    ← Este número
Tipo: Supergrupo
```

---

## ⚙️ Paso 7: Configurar el Grupo

### Opción A: En el menú

Cuando elijas la opción 2, te pedirá el ID:
```
Ingresa el ID del grupo (número): 1987654321
```

### Opción B: En .env (recomendado)

Edita `.env` y añade:
```bash
SOURCE_GROUP_ID=1987654321
```

Así no tendrás que escribirlo cada vez.

---

## 🔄 Paso 8: Iniciar Monitoreo

1. **Ejecuta:** `python telegram_user_client.py`
2. **Elige opción 2**
3. **Ingresa el ID** del grupo (o usa el de `.env`)

Verás:
```
============================================================
👁️ MONITOREANDO GRUPO ID: 1987654321
============================================================

📱 Grupo: Señales Crypto VIP 🔒
✅ Conexión establecida
🔍 Esperando eventos...
```

**¡Listo!** Ahora el bot está leyendo el grupo privado.

---

## 🎯 Funcionamiento

Cuando llegue un evento al grupo privado:

```
1. UserBot detecta el mensaje
   ↓
2. Verifica que sea un evento válido
   ↓
3. Clasifica con el motor
   ↓
4. Envía resumen a @JR79_BOT
```

**Ejemplo de salida:**
```
============================================================
🔍 EVENTO DETECTADO!
============================================================
Mensaje:
#BTCUSDT
SESGO ALCISTA
ORIGEN: FIBO 4H
...

⚙️ Clasificando evento...
✅ Clasificado: 94.4/100 - ALTA PRIORIDAD
📤 Enviando a @JR79_BOT...
✅ Mensaje enviado a @JR79_BOT
============================================================
```

---

## 📱 Ver Resultados

Abre Telegram y busca a **@JR79_BOT**. Verás los mensajes que el UserBot le envía:

```
🔥 EVENTO CLASIFICADO

Símbolo: BTCUSDT
Sesgo: BULLISH
Origen: FIBO_4H

Score: 94.4/100
Prioridad: ALTA PRIORIDAD

Top 3 Factores:
1. Open Interest: OI increasing (peso: 23.9)
2. CVD: divergencia detectada (peso: 18.0)
3. Delta: dominancia compradora (peso: 15.0)
```

---

## 🔒 Seguridad

### ⚠️ IMPORTANTE:

1. **Tu API_ID y API_HASH son sensibles**
   - No los compartas con nadie
   - No los subas a Git (ya están en `.gitignore`)

2. **La sesión es tu cuenta**
   - El archivo `session_name.session` es tu sesión activa
   - No lo compartas

3. **El UserBot usa tu cuenta**
   - Solo hace lo que está programado (leer y reenviar)
   - No envía mensajes a otros
   - No modifica nada

4. **Permisos**
   - Solo lee grupos donde YA estás
   - No se une a grupos automáticamente

---

## 🛠️ Solución de Problemas

### ❌ "Invalid API_ID or API_HASH"

**Solución:**
- Verifica que copiaste bien de https://my.telegram.org
- El API_ID es solo números (sin comillas en .env)
- El API_HASH es largo (32 caracteres)

### ❌ "Could not find the input entity"

**Solución:**
- El ID del grupo es incorrecto
- Verifica que estés en ese grupo
- Lista tus grupos de nuevo (opción 1)

### ❌ "Phone number is already registered"

**Solución:**
- Esto es normal
- Te pedirá el código de verificación
- Revisa tu Telegram (te llega un mensaje)

### ⚠️ "You are trying to send this request too many times"

**Solución:**
- Telegram te limitó temporalmente
- Espera 10-15 minutos
- Vuelve a intentar

---

## 📊 Estructura de Archivos

```
D:\FUTUROS 2026\
├── .env                          ← Credenciales aquí
├── telegram_user_client.py       ← Script principal
├── session_name.session          ← Tu sesión (se crea automáticamente)
├── mis_grupos_telegram.txt       ← Lista de tus grupos
└── data/
    └── classifications/          ← Histórico de clasificaciones
```

---

## 🎮 Comandos de Referencia

```bash
# Instalar dependencias
pip install telethon

# Listar grupos y elegir cuál monitorear
python telegram_user_client.py

# Ver histórico de clasificaciones
cat data/classifications/*.jsonl
```

---

## 🔄 Flujo Completo

### Configuración (una sola vez):

1. ✅ Obtener API_ID y API_HASH de https://my.telegram.org
2. ✅ Añadirlos a `.env`
3. ✅ Ejecutar script y autenticarse
4. ✅ Listar grupos y copiar ID
5. ✅ Configurar SOURCE_GROUP_ID en `.env`

### Uso diario:

1. Ejecutar: `python telegram_user_client.py`
2. Elegir opción 2 (monitorear)
3. Dejar corriendo 24/7
4. Ver resultados en @JR79_BOT

---

## 📝 Ejemplo de .env Completo

```bash
# Bot oficial
TELEGRAM_BOT_TOKEN=8919647640:AAGG9arpCo0tye070aMYNvLGwV3aPULfXn8

# UserBot (tu cuenta)
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=1234567890abcdef1234567890abcdef
TELEGRAM_PHONE=+521234567890

# Grupo de señales (donde leer)
SOURCE_GROUP_ID=1987654321
```

---

## ✅ Checklist

- [ ] Obtuve API_ID y API_HASH de my.telegram.org
- [ ] Los añadí a .env
- [ ] Instalé telethon: `pip install telethon`
- [ ] Ejecuté: `python telegram_user_client.py`
- [ ] Me autentiqué con el código de Telegram
- [ ] Listé mis grupos (opción 1)
- [ ] Identifiqué mi grupo de señales
- [ ] Copié el ID del grupo
- [ ] Lo añadí a .env como SOURCE_GROUP_ID
- [ ] Inicié el monitoreo (opción 2)
- [ ] Verifiqué que @JR79_BOT recibe los mensajes

---

## 🎉 ¡Listo!

Tu sistema ahora:
- ✅ Lee grupos PRIVADOS con tu cuenta
- ✅ Clasifica eventos automáticamente
- ✅ Envía resúmenes a @JR79_BOT
- ✅ Guarda histórico para análisis

---

**Siguiente paso:** Ejecuta `python telegram_user_client.py` y sigue el menú 🚀
