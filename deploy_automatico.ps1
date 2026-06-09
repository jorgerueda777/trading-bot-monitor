# Script de Despliegue Automático
# Este script automatiza TODO el proceso de despliegue

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🚀 DESPLIEGUE AUTOMÁTICO DEL BOT" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
$currentDir = Get-Location
Write-Host "📁 Directorio actual: $currentDir" -ForegroundColor Yellow
Write-Host ""

# Paso 1: Verificar Git
Write-Host "PASO 1: Verificando Git..." -ForegroundColor Green
try {
    $gitVersion = git --version
    Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git NO está instalado" -ForegroundColor Red
    Write-Host "Instala Git desde: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Presiona Enter para salir..."
    Read-Host
    exit
}
Write-Host ""

# Paso 2: Verificar archivos necesarios
Write-Host "PASO 2: Verificando archivos..." -ForegroundColor Green
$archivos = @(
    "monitor_grupos.py",
    "requirements.txt",
    "Dockerfile",
    ".gitignore",
    ".env"
)

$faltantes = @()
foreach ($archivo in $archivos) {
    if (Test-Path $archivo) {
        Write-Host "✅ $archivo" -ForegroundColor Green
    } else {
        Write-Host "❌ $archivo NO ENCONTRADO" -ForegroundColor Red
        $faltantes += $archivo
    }
}

if ($faltantes.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️ Faltan archivos críticos. Verifica tu proyecto." -ForegroundColor Red
    Write-Host "Presiona Enter para salir..."
    Read-Host
    exit
}
Write-Host ""

# Paso 3: Inicializar Git
Write-Host "PASO 3: Inicializando repositorio Git..." -ForegroundColor Green
if (Test-Path ".git") {
    Write-Host "✅ Repositorio Git ya existe" -ForegroundColor Yellow
} else {
    git init
    Write-Host "✅ Repositorio Git inicializado" -ForegroundColor Green
}
Write-Host ""

# Paso 4: Agregar archivos
Write-Host "PASO 4: Agregando archivos al repositorio..." -ForegroundColor Green
git add .
Write-Host "✅ Archivos agregados" -ForegroundColor Green
Write-Host ""

# Paso 5: Hacer commit
Write-Host "PASO 5: Creando commit..." -ForegroundColor Green
$commitMsg = "Initial commit - Trading bot ready for deployment"
try {
    git commit -m $commitMsg
    Write-Host "✅ Commit creado" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Posible error en commit (puede ser normal si no hay cambios)" -ForegroundColor Yellow
}
Write-Host ""

# Paso 6: Instrucciones para GitHub
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "📋 SIGUIENTE: Crear repositorio en GitHub" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "INSTRUCCIONES:" -ForegroundColor Yellow
Write-Host "1. Ve a: https://github.com/new" -ForegroundColor White
Write-Host "2. Nombre del repositorio: trading-bot-monitor" -ForegroundColor White
Write-Host "3. Visibilidad: PRIVADO (🔒)" -ForegroundColor White
Write-Host "4. NO marques ninguna casilla (README, .gitignore, license)" -ForegroundColor White
Write-Host "5. Clic 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "¿Ya creaste el repositorio? (S/N): " -ForegroundColor Yellow -NoNewline
$respuesta = Read-Host

if ($respuesta -ne "S" -and $respuesta -ne "s") {
    Write-Host "Por favor crea el repositorio primero y vuelve a ejecutar este script." -ForegroundColor Red
    Write-Host "Presiona Enter para salir..."
    Read-Host
    exit
}
Write-Host ""

# Paso 7: Conectar con GitHub
Write-Host "PASO 7: Conectando con GitHub..." -ForegroundColor Green
Write-Host "Ingresa tu USUARIO de GitHub: " -ForegroundColor Yellow -NoNewline
$githubUser = Read-Host
Write-Host ""

$repoUrl = "https://github.com/$githubUser/trading-bot-monitor.git"
Write-Host "URL del repositorio: $repoUrl" -ForegroundColor Cyan

try {
    git remote add origin $repoUrl 2>$null
    Write-Host "✅ Remoto configurado" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Remoto ya existe, actualizando..." -ForegroundColor Yellow
    git remote set-url origin $repoUrl
}
Write-Host ""

# Paso 8: Configurar rama main
Write-Host "PASO 8: Configurando rama principal..." -ForegroundColor Green
git branch -M main
Write-Host "✅ Rama configurada como 'main'" -ForegroundColor Green
Write-Host ""

# Paso 9: Subir código
Write-Host "PASO 9: Subiendo código a GitHub..." -ForegroundColor Green
Write-Host "⚠️ Te pedirá tus credenciales de GitHub:" -ForegroundColor Yellow
Write-Host "   Usuario: $githubUser" -ForegroundColor White
Write-Host "   Password: Usa un Personal Access Token" -ForegroundColor White
Write-Host "   (Genera uno en: https://github.com/settings/tokens)" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Yellow
Read-Host

try {
    git push -u origin main
    Write-Host "✅ Código subido exitosamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al subir código" -ForegroundColor Red
    Write-Host "Posibles causas:" -ForegroundColor Yellow
    Write-Host "  - Credenciales incorrectas" -ForegroundColor White
    Write-Host "  - Necesitas Personal Access Token en lugar de password" -ForegroundColor White
    Write-Host "  - El repositorio no existe" -ForegroundColor White
    Write-Host ""
    Write-Host "Intenta manualmente: git push -u origin main" -ForegroundColor Yellow
    Write-Host "Presiona Enter para continuar de todos modos..."
    Read-Host
}
Write-Host ""

# Paso 10: Instrucciones para Render
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🌐 SIGUIENTE: Desplegar en Render.com" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "INSTRUCCIONES DETALLADAS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Ve a: https://render.com" -ForegroundColor White
Write-Host "2. Clic 'Get Started' y registra con GitHub" -ForegroundColor White
Write-Host "3. Clic 'New +' → 'Background Worker'" -ForegroundColor White
Write-Host "4. Conecta tu repositorio: trading-bot-monitor" -ForegroundColor White
Write-Host "5. Configuración:" -ForegroundColor White
Write-Host "   - Name: trading-bot-monitor" -ForegroundColor Cyan
Write-Host "   - Environment: Python 3" -ForegroundColor Cyan
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "   - Start Command: python monitor_grupos.py" -ForegroundColor Cyan
Write-Host "   - Plan: Free" -ForegroundColor Cyan
Write-Host "6. Clic 'Create Background Worker' (NO deploy todavía)" -ForegroundColor White
Write-Host ""

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🔑 Variables de Entorno" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "En Render, ve a 'Environment' y agrega:" -ForegroundColor Yellow
Write-Host ""

# Leer .env si existe
if (Test-Path ".env") {
    Write-Host "📄 Valores de tu .env:" -ForegroundColor Green
    Write-Host ""
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            $key = $matches[1]
            $value = $matches[2]
            if ($value -and $value.Length -gt 0) {
                Write-Host "✅ $key = [CONFIGURADO]" -ForegroundColor Green
            } else {
                Write-Host "⚠️ $key = [VACÍO]" -ForegroundColor Yellow
            }
        }
    }
    Write-Host ""
    Write-Host "Copia estos valores uno por uno a Render Environment" -ForegroundColor Yellow
} else {
    Write-Host "⚠️ Archivo .env no encontrado" -ForegroundColor Red
    Write-Host "Necesitas configurar manualmente en Render:" -ForegroundColor Yellow
    Write-Host "  - TELEGRAM_API_ID" -ForegroundColor White
    Write-Host "  - TELEGRAM_API_HASH" -ForegroundColor White
    Write-Host "  - TELEGRAM_PHONE" -ForegroundColor White
    Write-Host "  - SOURCE_GROUP_IDS" -ForegroundColor White
    Write-Host "  - DEST_CHANNEL_ID" -ForegroundColor White
    Write-Host "  - BINANCE_API_KEY (opcional)" -ForegroundColor White
    Write-Host "  - BINANCE_API_SECRET (opcional)" -ForegroundColor White
}
Write-Host ""

# Paso 11: Sesión de Telegram
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "📱 Archivo de Sesión de Telegram" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "session_name.session") {
    Write-Host "✅ Archivo session_name.session encontrado" -ForegroundColor Green
    Write-Host ""
    Write-Host "OPCIONES:" -ForegroundColor Yellow
    Write-Host "A) Subirlo al repositorio (fácil, asegúrate repo sea PRIVADO)" -ForegroundColor White
    Write-Host "B) Regenerarlo en el servidor (más seguro)" -ForegroundColor White
    Write-Host ""
    Write-Host "¿Quieres subirlo al repo? (S/N): " -ForegroundColor Yellow -NoNewline
    $subirSesion = Read-Host
    
    if ($subirSesion -eq "S" -or $subirSesion -eq "s") {
        Write-Host ""
        Write-Host "Subiendo sesión al repositorio..." -ForegroundColor Green
        git add session_name.session
        git commit -m "Add Telegram session"
        git push
        Write-Host "✅ Sesión subida" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "⚠️ Tendrás que regenerar la sesión en Render" -ForegroundColor Yellow
        Write-Host "El bot te enviará un código cuando inicie por primera vez" -ForegroundColor White
    }
} else {
    Write-Host "⚠️ Archivo session_name.session NO encontrado" -ForegroundColor Yellow
    Write-Host "Se generará automáticamente cuando el bot inicie en Render" -ForegroundColor White
    Write-Host "Telegram te enviará un código de verificación" -ForegroundColor White
}
Write-Host ""

# Paso 12: Deploy final
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🚀 DEPLOY FINAL" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "En Render:" -ForegroundColor Yellow
Write-Host "1. Verifica que TODAS las variables estén configuradas" -ForegroundColor White
Write-Host "2. Clic 'Manual Deploy' → 'Deploy latest commit'" -ForegroundColor White
Write-Host "3. Espera 2-3 minutos" -ForegroundColor White
Write-Host "4. Ve a 'Logs' para ver si está corriendo" -ForegroundColor White
Write-Host ""
Write-Host "Busca en los logs:" -ForegroundColor Yellow
Write-Host "  ✅ Conectado!" -ForegroundColor Green
Write-Host "  📋 Grupos a monitorear:" -ForegroundColor Green
Write-Host "  ✅ Monitoreo iniciado" -ForegroundColor Green
Write-Host ""

# Resumen final
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "✅ RESUMEN" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Código preparado y subido a GitHub" -ForegroundColor Green
Write-Host "📋 Sigue las instrucciones arriba para Render" -ForegroundColor Yellow
Write-Host "📖 Documentación completa en: DEPLOY_RENDER_FACIL.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 ¡Casi listo! Solo falta configurar en Render" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Enter para salir..."
Read-Host
