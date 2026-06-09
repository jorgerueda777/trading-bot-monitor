# 📱 Cómo Ver tus Grupos y Configurar el Bot

## 🎯 Objetivo

Necesitas saber qué grupo tiene los eventos para que el bot lo lea.

---

## ✅ MÉTODO SIMPLE (Recomendado)

### Paso 1: Añade el bot a TODOS tus grupos

No importa si no sabes cuál es el grupo correcto. Añade el bot a todos:

1. **Abre Telegram**
2. **Ve a cada grupo** que pueda tener eventos
3. **En cada grupo:**
   - Click en el nombre del grupo (arriba)
   - Click en "Añadir miembros"
   - Busca: `@JR79_BOT`
   - Añádelo

### Paso 2: Identifica el grupo correcto

En cada grupo donde añadiste el bot, envía:
```
/getid
```

El bot responderá con algo como:
```
📋 INFORMACIÓN DEL CHAT

Chat ID: -1001234567890
Tipo: supergroup
Título: Mi Grupo de Trading  ← Este es el nombre del grupo

User ID: 123456789
Usuario: @tu_usuario
```

**Mira el "Título"** - ahí sabrás qué grupo es.

### Paso 3: Configura el bot con el grupo correcto

Una vez que identifiques el grupo que tiene los eventos:

1. **Copia el Chat ID** de ese grupo (ej: `-1001234567890`)

2. **Edita el archivo `.env`**

3. **Busca esta línea:**
   ```
   TELEGRAM_GROUP_ID=your_group_id_here
   ```

4. **Reemplázala con tu Chat ID:**
   ```
   TELEGRAM_GROUP_ID=-1001234567890
   ```

5. **Guarda el archivo**

6. **Reinicia el bot:**
   - Detén el bot actual (Ctrl+C en la ventana donde corre)
   - Inicia de nuevo: `python telegram_integration.py`

---

## 📋 MÉTODO ALTERNATIVO: Ver todos los chats del bot

### Opción A: Desde cualquier chat con el bot

1. **Abre Telegram**
2. **Busca tu bot:** `@JR79_BOT`
3. **Inicia un chat privado** con el bot
4. **Envía:**
   ```
   /listchats
   ```

El bot te mostrará el chat actual (el privado contigo).

### Opción B: Desde cada grupo

En cada grupo donde añadiste el bot:
```
/getid
```

Verás el ID y nombre de ese grupo específico.

---

## 🔍 ¿Cómo saber qué grupo tiene los eventos?

### Método 1: Por el nombre
Cuando envíes `/getid` en cada grupo, verás el **Título** del grupo. Reconocerás cuál es tu grupo de trading/señales.

### Método 2: Por la actividad
- Revisa tus grupos en Telegram
- Identifica cuál tiene mensajes como:
  ```
  #BTCUSDT
  SESGO ALCISTA
  ORIGEN: FIBO 4H
  ```

### Método 3: Pregunta en el grupo
Si no estás seguro, pregunta en el grupo:
```
¿Este es el grupo de señales de trading?
```

---

## 🎯 Ejemplo Completo

### Escenario: Tienes 3 grupos

**Grupo 1: "Amigos"**
- Añades el bot
- Envías `/getid`
- Ves: `Título: Amigos` ❌ No es este

**Grupo 2: "Señales Crypto VIP"**
- Añades el bot
- Envías `/getid`
- Ves: `Título: Señales Crypto VIP` ✅ ¡Este es!
- Copias el Chat ID: `-1001234567890`

**Grupo 3: "Noticias"**
- Añades el bot
- Envías `/getid`
- Ves: `Título: Noticias` ❌ No es este

### Configuración final:

Editas `.env`:
```bash
TELEGRAM_GROUP_ID=-1001234567890
```

Reinicias el bot y ¡listo!

---

## 🤖 Comandos Útiles

| Comando | Qué hace | Dónde usarlo |
|---------|----------|--------------|
| `/start` | Info del bot | Cualquier chat |
| `/getid` | Ver ID y nombre del chat actual | En cada grupo |
| `/listchats` | Ver info del chat actual | Cualquier chat |

---

## 🆘 Preguntas Frecuentes

### ¿El bot puede leer mis mensajes privados?
No. El bot solo lee mensajes de los grupos donde está añadido.

### ¿Puedo añadir el bot a múltiples grupos?
Sí, pero solo clasificará eventos del grupo configurado en `TELEGRAM_GROUP_ID`.

### ¿Cómo cambio de grupo?
1. Cambia el `TELEGRAM_GROUP_ID` en `.env`
2. Reinicia el bot

### ¿El bot clasifica automáticamente?
Sí, una vez configurado, detecta y clasifica eventos automáticamente sin que hagas nada.

---

## ✅ Checklist Rápido

- [ ] Abre Telegram
- [ ] Identifica tu grupo de señales (por el nombre)
- [ ] Añade `@JR79_BOT` a ese grupo
- [ ] En ese grupo, envía `/getid`
- [ ] Copia el Chat ID
- [ ] Edita `.env` con ese ID
- [ ] Reinicia el bot
- [ ] Prueba con un evento

---

## 🎯 Lo Más Simple

**Si solo tienes UN grupo de trading:**

1. Ve a ese grupo
2. Añade `@JR79_BOT`
3. Envía `/getid`
4. Copia el número (Chat ID)
5. Ponlo en `.env`
6. Reinicia el bot
7. ¡Listo!

---

## 📞 Comandos de Referencia

```bash
# Ver info del bot
python test_telegram_config.py

# Reiniciar bot (después de cambiar .env)
# 1. Detener: Ctrl+C
# 2. Iniciar:
python telegram_integration.py
```

---

**¿Listo?** Ve a Telegram, identifica tu grupo, y configúralo. ¡El bot está esperando! 🚀
