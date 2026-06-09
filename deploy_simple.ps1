# Script de Despliegue SIMPLIFICADO
# Usa la configuración de Git que ya tienes

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🚀 DESPLIEGUE AUTOMÁTICO" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Detectar usuario de Git
$gitUser = git config --global user.name
$gitEmail = git config --global user.email

Write-Host "📋 Configuración detectada:" -ForegroundColor Green
Write-Host "   Usuario Git: $gitUser" -ForegroundColor White
Write-Host "   Email: $gitEmail" -ForegroundColor White
Write-Host ""

# Preguntar qué usuario de GitHub usar
Write-Host "¿Qué usuario de GitHub quieres usar?" -ForegroundColor Yellow
Write-Host "1) jorgerueda777 (detectado en tu sistema)" -ForegroundColor White
Write-Host "2) renovationpro77 (mencionaste este)" -ForegroundColor White
Write-Host "3) Otro (ingresarlo manualmente)" -ForegroundColor White
Write-Host ""
Write-Host "Elige opción (1/2/3): " -ForegroundColor Yellow -NoNewline
$opcion = Read-Host

switch ($opcion) {
    "1" { $githubUser = "jorgerueda777" }
    "2" { $githubUser = "renovationpro77" }
    "3" { 
        Write-Host "Ingresa tu usuario de GitHub: " -ForegroundColor Yellow -NoNewline
        $githubUser = Read-Host
    }
    default { $githubUser = "jorgerueda777" }
}

Write-Host ""
Write-Host "✅ Usando usuario: $githubUser" -ForegroundColor Green
Write-Host ""

# Verificar Git instalado
Write-Host "Verificando Git..." -ForegroundColor Green
try {
    $gitVersion = git --version
    Write-Host "✅ $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git no instalado" -ForegroundColor Red
    Write-Host "Instala desde: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit
}
Write-Host ""

# Verificar archivos
Write-Host "Verificando archivos necesarios..." -ForegroundColor Green
$archivos = @("monitor_grupos.py", "requirements.txt", "Dockerfile", ".gitignore")
$todosExisten = $true

foreach ($archivo in $archivos) {
    if (Test-Path $archivo) {
        Write-Host "✅ $archivo" -ForegroundColor Green
    } else {
        Write-Host "❌ $archivo" -ForegroundColor Red
        $todosExisten = $false
    }
}

if (-not $todosExisten) {
    Write-Host ""
    Write-Host "Faltan archivos. Verifica tu proyecto." -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit
}
Write-Host ""

# Inicializar Git
Write-Host "Inicializando Git..." -ForegroundColor Green
if (Test-Path ".git") {
    Write-Host "✅ Ya existe repositorio Git" -ForegroundColor Yellow
} else {
    git init
    Write-Host "✅ Repositorio inicializado" -ForegroundColor Green
}
Write-Host ""

# Agregar archivos
Write-Host "Agregando archivos..." -ForegroundColor Green
git add .
Write-Host "✅ Archivos agregados" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "Creando commit..." -ForegroundColor Green
git commit -m "Initial commit - Trading bot" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit creado" -ForegroundColor Green
} else {
    Write-Host "⚠️ Ya existe commit o no hay cambios" -ForegroundColor Yellow
}
Write-Host ""

# Instrucciones GitHub
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "📋 PASO 1: Crear repo en GitHub" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Abre en tu navegador: https://github.com/new" -ForegroundColor White
Write-Host "2. Nombre: trading-bot-monitor" -ForegroundColor White
Write-Host "3. Visibilidad: PRIVADO 🔒" -ForegroundColor White
Write-Host "4. NO marques ninguna casilla" -ForegroundColor White
Write-Host "5. Clic 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Enter cuando hayas creado el repo..." -ForegroundColor Yellow
Read-Host
Write-Host ""

# Conectar GitHub
Write-Host "Conectando con GitHub..." -ForegroundColor Green
$repoUrl = "https://github.com/$githubUser/trading-bot-monitor.git"
Write-Host "URL: $repoUrl" -ForegroundColor Cyan

try {
    git remote add origin $repoUrl 2>$null
} catch {
    git remote set-url origin $repoUrl
}
git branch -M main
Write-Host "✅ Repositorio conectado" -ForegroundColor Green
Write-Host ""

# Push
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "📤 PASO 2: Subir código a GitHub" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ahora voy a subir el código..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️ Te pedirá credenciales:" -ForegroundColor Yellow
Write-Host "   Usuario: $githubUser" -ForegroundColor White
Write-Host "   Password: Usa tu Personal Access Token" -ForegroundColor White
Write-Host ""
Write-Host "Si NO tienes token:" -ForegroundColor Yellow
Write-Host "1. Abre: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "2. 'Generate new token (classic)'" -ForegroundColor White
Write-Host "3. Marca solo 'repo'" -ForegroundColor White
Write-Host "4. Generate y copia el token (empieza con ghp_)" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Yellow
Read-Host
Write-Host ""

git push -u origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅✅✅ CÓDIGO SUBIDO EXITOSAMENTE ✅✅✅" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Error al subir" -ForegroundColor Red
    Write-Host "Posibles causas:" -ForegroundColor Yellow
    Write-Host "- Credenciales incorrectas" -ForegroundColor White
    Write-Host "- Necesitas token en lugar de password" -ForegroundColor White
    Write-Host "- El repo no existe" -ForegroundColor White
    Write-Host ""
    Write-Host "Presiona Enter para ver instrucciones de Render de todos modos..."
    Read-Host
}
Write-Host ""

# Instrucciones Render
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🌐 PASO 3: Desplegar en Render" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "A) CREAR CUENTA Y SERVICIO:" -ForegroundColor Yellow
Write-Host "   1. Ve a: https://render.com" -ForegroundColor White
Write-Host "   2. 'Get Started' → Registra con GitHub" -ForegroundColor White
Write-Host "   3. 'New +' → 'Background Worker'" -ForegroundColor White
Write-Host "   4. Conecta: trading-bot-monitor" -ForegroundColor White
Write-Host ""

Write-Host "B) CONFIGURAR SERVICIO:" -ForegroundColor Yellow
Write-Host "   Name: trading-bot-monitor" -ForegroundColor Cyan
Write-Host "   Environment: Python 3" -ForegroundColor Cyan
Write-Host "   Build Command: pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "   Start Command: python monitor_grupos.py" -ForegroundColor Cyan
Write-Host "   Plan: Free" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Clic 'Create' (NO deploy todavía)" -ForegroundColor White
Write-Host ""

Write-Host "C) AGREGAR VARIABLES DE ENTORNO:" -ForegroundColor Yellow
Write-Host "   Pestaña 'Environment' → Agregar:" -ForegroundColor White
Write-Host ""

# Leer .env
if (Test-Path ".env") {
    Write-Host "   📄 Variables de tu .env:" -ForegroundColor Green
    Write-Host ""
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            $key = $matches[1]
            $value = $matches[2]
            if ($value) {
                Write-Host "   $key = [tu_valor]" -ForegroundColor Cyan
            }
        }
    }
} else {
    Write-Host "   TELEGRAM_API_ID" -ForegroundColor Cyan
    Write-Host "   TELEGRAM_API_HASH" -ForegroundColor Cyan
    Write-Host "   TELEGRAM_PHONE" -ForegroundColor Cyan
    Write-Host "   SOURCE_GROUP_IDS" -ForegroundColor Cyan
    Write-Host "   DEST_CHANNEL_ID" -ForegroundColor Cyan
    Write-Host "   BINANCE_API_KEY" -ForegroundColor Cyan
    Write-Host "   BINANCE_API_SECRET" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "   Copia los valores de tu .env" -ForegroundColor White
Write-Host "   Clic 'Save Changes'" -ForegroundColor White
Write-Host ""

Write-Host "D) DEPLOY:" -ForegroundColor Yellow
Write-Host "   1. 'Manual Deploy' → 'Deploy latest commit'" -ForegroundColor White
Write-Host "   2. Espera 2-3 minutos" -ForegroundColor White
Write-Host "   3. Ve a 'Logs'" -ForegroundColor White
Write-Host "   4. Busca: '✅ Conectado!'" -ForegroundColor White
Write-Host ""

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "✅ PROCESO COMPLETADO" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Código preparado y (esperemos) subido a GitHub" -ForegroundColor Green
Write-Host "Sigue las instrucciones arriba para Render" -ForegroundColor Yellow
Write-Host ""
Write-Host "📖 Más ayuda: DEPLOY_RENDER_FACIL.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Enter para salir..."
Read-Host
