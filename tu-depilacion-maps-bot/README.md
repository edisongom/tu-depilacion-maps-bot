# Tu Depilación Maps Bot

Automatiza la subida de portadas de reels a Google Maps todos los jueves.

## Setup

### 1. Google Cloud Credentials

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea un nuevo Service Account:
   - IAM & Admin → Service Accounts → Create Service Account
   - Nombre: `tu-depilacion-bot`
   - Grant role: `Editor` (o más restrictivo si prefieres)
3. Crea una JSON key:
   - Click en el service account
   - Keys → Add Key → Create new key → JSON
   - Descarga el archivo JSON

### 2. Google Maps Admin

1. En Google Maps, ve a Settings de tu negocio
2. Users & Permissions → Add user
3. Invita al email del service account (ej: `tu-depilacion-bot@...iam.gserviceaccount.com`)
4. Dale permisos de admin
5. Obtén el Location ID:
   - URL de Maps: `https://business.google.com/locations/{LOCATION_ID}`

### 3. GitHub Secrets

1. Ve a Settings del repo → Secrets and variables → Actions
2. Crea dos secrets:
   - `GOOGLE_MAPS_CREDENTIALS`: Pega el contenido del JSON completo
   - `BUSINESS_LOCATION_ID`: El ID de arriba

### 4. Habilitar Workflows

1. Ve a Actions → Enable workflows

## Testing

Ejecuta manualmente:
- Actions → Upload to Google Maps → Run workflow

## Estructura

```
contenido/
  2026-11/
    portada.png  ← Se sube automáticamente cada jueves
  2026-12/
    portada.png
  ...
```

El bot busca la portada más reciente y la sube a Maps.

