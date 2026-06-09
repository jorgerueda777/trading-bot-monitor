# 🚀 EJECUTA ESTO - Despliegue Automático

## ¿Qué hace el script?

He creado un script que **automatiza TODO lo que puedo** sin necesitar tus credenciales.

El script:
- ✅ Verifica que Git esté instalado
- ✅ Verifica que todos los archivos existan
- ✅ Inicializa el repositorio Git
- ✅ Hace commit de todo el código
- ✅ Te guía para conectar con GitHub
- ✅ Sube el código automáticamente
- ✅ Te muestra instrucciones claras para Render
- ✅ Lee tu .env y te muestra qué variables configurar

---

## PASO 1: Ejecutar el script

### Abrir PowerShell:
1. Presiona `Windows + X`
2. Selecciona "Windows PowerShell" o "Terminal"
3. Navega a tu carpeta:
   ```powershell
   cd "D:\FUTUROS 2026"
   ```

### Ejecutar:
```powershell
powershell -ExecutionPolicy Bypass -File deploy_automatico.ps1
```

**Eso es todo.** El script te guiará paso a paso.

---

## ¿Qué te pedirá el script?

### 1. Confirmación de repositorio GitHub
- Te dirá que crees un repo en GitHub
- URL: https://github.com/new
- Nombre: `trading-bot-monitor`
- Privado: SÍ

### 2. Tu usuario de GitHub
- Te pedirá tu nombre de usuario
- Ejemplo: `juanperez`

### 3. Credenciales GitHub
- Usuario: tu username
- Password: Personal Access Token
  - Crear en: https://github.com/settings/tokens
  - Marcar: `repo`
  - Copiar y usar como password

### 4. Subir sesión (opcional)
- Te preguntará si quieres subir `session_name.session`
- Responde "S" si quieres (más fácil)
- Responde "N" si prefieres regenerar en servidor

---

## Después del script

El script te mostrará **instrucciones detalladas** para:

1. Crear servicio en Render.com
2. Configurar variables de entorno
3. Hacer deploy

**Todo con valores exactos para copiar y pegar.**

---

## Si no tienes Git instalado

### Instalar Git:
1. Ve a: https://git-scm.com/download/win
2. Descarga e instala
3. Reinicia PowerShell
4. Ejecuta el script

---

## Si algo falla

El script te dirá exactamente qué falló y cómo solucionarlo.

También puedes:
- Revisar `DEPLOY_RENDER_FACIL.md` para guía completa
- Revisar `CHECKLIST_DESPLIEGUE.md` para troubleshooting

---

## ⚡ EJECUCIÓN RÁPIDA (Un solo comando)

Si ya tienes Git instalado y quieres ir directo:

```powershell
cd "D:\FUTUROS 2026"; powershell -ExecutionPolicy Bypass -File deploy_automatico.ps1
```

---

## 🎯 Resultado esperado

Al final del script, verás:

```
✅ Código preparado y subido a GitHub
📋 Sigue las instrucciones para Render
🎉 ¡Casi listo! Solo falta configurar en Render
```

Y tendrás instrucciones exactas para los siguientes pasos.

---

## ⏱️ Tiempo total

- Script: 5 minutos
- Configurar Render: 10 minutos
- **Total: 15 minutos**

---

**¿Listo?** Ejecuta el script y avísame si tienes algún problema.
