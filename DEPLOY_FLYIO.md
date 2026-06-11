# 🚀 Deployment en Fly.io

## ¿Por qué Fly.io?

Fly.io es mejor para tu bot porque:
- ✅ Máquinas virtuales dedicadas (no contenedores compartidos)
- ✅ Mejor soporte para procesos de larga duración
- ✅ No tiene el problema de "sleep mode" de Render
- ✅ Tier gratuito generoso
- ✅ IPs más estables

## 📋 Requisitos

1. Tener cuenta en Fly.io: https://fly.io/app/sign-up
2. Instalar Fly CLI en Windows:

```powershell
# Con PowerShell como Admin
iwr https://fly.io/install.ps1 -useb | iex
```

3. Reinicia la terminal después de instalar

## 🔐 Paso 1: Login en Fly.io

```bash
fly auth login
```

Se abrirá tu navegador para autenticarte.

## 📦 Paso 2: Crear la aplicación

```bash
fly apps create trading-bot-monitor-v2
```

## 🔧 Paso 3: Configurar variables de entorno

```bash
fly secrets set TELEGRAM_API_ID=33557793
fly secrets set TELEGRAM_API_HASH=2abb35b6a48c69a31b974399c8109e68
fly secrets set TELEGRAM_PHONE=+33753973592
fly secrets set TELEGRAM_SESSION_STRING="1BJWap1wBu1qsjEFf3zpZVrr6lwTM4eTYvQz-fKc9EBpr4Mx9vN7RORH6XwW8NAyRrJBBLbiHSIGzB4MZJT_agXvJyn6U8EioGZdcVJa8FBGPfQ3QJZcLMInhqT43WOzO7WD9JDfidRHcrlp5MwqWiyj6zlRdLtVYtjgfTwcy8yaet1Bnl9_unFFlzqeNx9e_9lwHoPLI2JXNvmfV-hj2IbU5nTy3HkvhsPxNa5WVaK1lX_wPnYz-e2HQWBZx-1W4dR5QlhCDyRPhWRUMXOk3bZUGrrPyp7U_1G7QMiB0LC-f-BO2WUS_Sgy52PYL4rZQ-i6Eogo9NJx5eXCt8gSUyynZw3NTM5A="
fly secrets set SOURCE_GROUP_IDS=5002799975,1959577386,2398253860
fly secrets set DEST_CHANNEL_ID=3415985578
fly secrets set BINANCE_API_KEY=lIwlU2Ds7nkacTvDnXVWopqM08xnnLllrxLmCHOC1YidCGri2zP40geLkKtjr4pk
fly secrets set BINANCE_API_SECRET=sznTO5LYWYfmobcqIhuMf5synK5fT9gNLjv3e2EWONdeTe1fghvOSdnapW3ZfLKO
```

## 🚀 Paso 4: Deploy

```bash
fly deploy
```

El primer deploy tomará 3-5 minutos.

## 📊 Paso 5: Verificar que está corriendo

```bash
# Ver logs en tiempo real
fly logs

# Ver status
fly status

# Abrir en el navegador
fly open
```

## 🔍 Monitorear el bot

```bash
# Logs en vivo
fly logs -a trading-bot-monitor-v2

# Ver métricas
fly dashboard
```

## 🛠️ Comandos útiles

```bash
# Reiniciar
fly apps restart trading-bot-monitor-v2

# Escalar (cambiar recursos)
fly scale count 1

# Ver secrets configurados
fly secrets list

# SSH a la máquina
fly ssh console

# Destruir app (cuidado!)
fly apps destroy trading-bot-monitor-v2
```

## ⚠️ Troubleshooting

### Si el bot no se conecta a Telegram:

1. Verifica logs:
```bash
fly logs
```

2. Verifica que la session string sea correcta:
```bash
fly secrets list
```

3. Regenera la session si es necesario y actualiza:
```bash
fly secrets set TELEGRAM_SESSION_STRING="<nueva_session>"
```

### Si el health check falla:

El health check está en `/health`. Verifica que el servidor HTTP esté corriendo en puerto 10000.

## 💰 Costos

Fly.io tiene tier gratuito que incluye:
- 3 máquinas compartidas (256MB RAM)
- 160GB bandwidth/mes
- Suficiente para este bot

## 🔄 Actualizar el bot

Cada vez que hagas cambios en el código:

```bash
git add .
git commit -m "descripción de cambios"
git push origin main

# Deploy nuevo código
fly deploy
```

## 📝 Notas importantes

1. **La máquina NO se apaga** (configurado con `auto_stop_machines = false`)
2. **Health check activo** cada 30 segundos
3. **Logs persistentes** - puedes ver el historial
4. **Mejor para userbots** que Render

## 🎯 Ventajas vs Render

| Característica | Render | Fly.io |
|----------------|--------|--------|
| Sleep mode | ❌ Sí (15 min) | ✅ No |
| IPs estables | ❌ No | ✅ Sí |
| SSH access | ❌ No | ✅ Sí |
| Logs | ✅ Sí | ✅ Mejor |
| Health checks | ✅ Sí | ✅ Mejor |
| Para userbots | ⚠️ Problemas | ✅ Funciona |

