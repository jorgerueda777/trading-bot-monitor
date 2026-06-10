# 🔧 CAMBIAR A BACKGROUND WORKER EN RENDER

## ⚠️ PROBLEMA ACTUAL

Web Service requiere puerto HTTP abierto en 90 segundos o se detiene.
El bot funciona pero Render lo mata por timeout.

## ✅ SOLUCIÓN: BACKGROUND WORKER

Background Workers son PERFECTOS para bots:
- ✅ Sin requisito de puerto HTTP
- ✅ Corren 24/7 sin interrupciones
- ✅ Completamente GRATIS
- ✅ No hay timeouts

## 📋 PASOS PARA CAMBIAR

### 1. Ir a Render Dashboard
https://dashboard.render.com/

### 2. ELIMINAR el Web Service actual
- Click en tu servicio "trading-bot-monitor"
- Settings → Delete Service

### 3. CREAR nuevo Background Worker

Click "New +" → "Background Worker"

**Configuración:**
- **Name:** trading-bot-monitor
- **Environment:** Python 3
- **Region:** Frankfurt (EU Central)
- **Branch:** main
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python monitor_grupos.py`

### 4. Agregar Variables de Entorno

En "Environment" agrega TODAS estas:

```
TELEGRAM_API_ID
33557793

TELEGRAM_API_HASH
2abb35b6a48c69a31b974399c8109e68

TELEGRAM_PHONE
+33776209496

TELEGRAM_SESSION_STRING
1BJWap1wBu0Edq64hBPnn7WGc6f71izUuY0kSBrKkdhPpCXoipN3VTGMOdstCCvDu8stB5Kj1_38pZMtLAP9kQgDer21pjJZ0l_ssHmxUXIfJ9pSI_C7xbqwDzU7dms2nzO0WUrRS6uiDummhD_XjG7QpQCzaLkNWCBx2DJOtxeepMyTaxf0yfvVPcdy2EYSGM1GeGMiIvLHNbMkstbUvzWbYJ_6gWbExOMAROwNB5h4ntjJf6fomc0O_C6OS2cxZh-2995RorTBo9Atxhc-1ra1-tffQDvHo-d7BN40pRW82KYVRWD8dlebxqAugrbM2oPTmx_M46137zCsCDPIZWIl8SU79Ubs=

SOURCE_GROUP_IDS
5002799975,1959577386,2398253860

DEST_CHANNEL_ID
3415985578

BINANCE_API_KEY
lIwlU2Ds7nkacTvDnXVWopqM08xnnLllrxLmCHOC1YidCGri2zP40geLkKtjr4pk

BINANCE_API_SECRET
sznTO5LYWYfmobcqIhuMf5synK5fT9gNLjv3e2EWONdeTe1fghvOSdnapW3ZfLKO
```

### 5. Click "Create Background Worker"

¡Listo! El bot correrá sin problemas 24/7.

## 🎯 DIFERENCIAS

**Web Service (PROBLEMA):**
- ❌ Requiere puerto HTTP en 90 segundos
- ❌ Se detiene si no detecta puerto
- ❌ Timeouts constantes

**Background Worker (SOLUCIÓN):**
- ✅ No necesita puerto HTTP
- ✅ Corre indefinidamente
- ✅ Sin timeouts
- ✅ Perfecto para bots

## ⏱️ TIEMPO ESTIMADO

5 minutos para hacer el cambio completo.

## 📝 NOTA

Los Background Workers son EXACTAMENTE para casos como este: procesos que corren en segundo plano sin necesidad de HTTP.
