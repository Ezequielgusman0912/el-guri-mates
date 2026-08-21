# El Guri Mates — Ecommerce

Sitio de venta de mates, bombillas, canastas materas y termos. Hecho con Django.
Catálogo administrable desde `/admin`, botón flotante de WhatsApp, y pedidos
por formulario que envían un email de confirmación al cliente y al dueño.

## 1. Levantarlo en tu compu

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

copy .env.example .env         # Windows (usá "cp" en Mac/Linux)
# Editá .env: al menos poné un SECRET_KEY propio. El resto puede quedar
# vacío para probar en local (usa SQLite y muestra los emails en la consola).

python manage.py migrate
python manage.py seed_categories   # crea Mates, Bombillas, Canastas Materas, Termos
python manage.py createsuperuser   # para entrar a /admin

python manage.py runserver
```

Abrí http://127.0.0.1:8000 y http://127.0.0.1:8000/admin para cargar productos
(nombre, categoría, precio, stock, imagen, descripción).

## 2. Variables de entorno importantes

| Variable | Para qué sirve |
|---|---|
| `SECRET_KEY` | Clave de seguridad de Django. Generá una propia en producción. |
| `DEBUG` | `True` en local, `False` en producción. |
| `DATABASE_URL` | Cadena de conexión a Postgres (Neon, Supabase, etc). Vacía = SQLite local. |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | Tu Gmail y una [contraseña de aplicación](https://myaccount.google.com/apppasswords) (no tu contraseña normal). |
| `OWNER_EMAIL` | A dónde te llegan los avisos de pedido nuevo. |
| `WHATSAPP_NUMBER` | Tu número con código de país, sin `+` ni espacios (ej: `5493511234567`). |
| `CLOUDINARY_URL` | Opcional pero recomendado para producción (ver abajo). |

Sin `EMAIL_HOST_USER`/`EMAIL_HOST_PASSWORD` configurados, los emails no se
envían de verdad: se imprimen en la terminal, así podés probar el flujo
completo sin tocar tu Gmail.

## 3. Subir a GitHub

```bash
git init
git add .
git commit -m "Proyecto inicial El Guri Mates"
git branch -M main
git remote add origin <URL-DE-TU-REPO>
git push -u origin main
```

## 4. Desplegar en Vercel

1. Importá el repo desde el dashboard de Vercel.
2. En **Project Settings > Environment Variables**, cargá las mismas variables
   del paso 2 (como mínimo `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`,
   `WHATSAPP_NUMBER`, y las de email si querés que los pedidos manden mail real).
3. Necesitás una base de datos Postgres externa (Vercel no incluye una):
   creá una gratis en [Neon](https://neon.tech) o [Supabase](https://supabase.com)
   y pegá la connection string en `DATABASE_URL`.
4. Deploy. Vercel corre `build_files.sh` (instala dependencias y junta los
   estáticos) y sirve el sitio con `config/wsgi.py`.
5. Después del primer deploy, corré las migraciones contra esa base Postgres
   desde tu compu (apuntando `DATABASE_URL` a la misma base):
   ```bash
   python manage.py migrate
   python manage.py seed_categories
   python manage.py createsuperuser
   ```

### Importante sobre las imágenes de producto

Vercel no tiene disco persistente: si subís una foto desde `/admin` sin
configurar `CLOUDINARY_URL`, la imagen puede desaparecer en el próximo deploy.
Para que las fotos queden guardadas de verdad:

1. Creá una cuenta gratis en [Cloudinary](https://cloudinary.com).
2. Copiá tu "API Environment variable" (`CLOUDINARY_URL=cloudinary://...`).
3. Pegala como variable de entorno en Vercel (y opcionalmente en tu `.env` local).

Con eso, las imágenes que subas desde el admin se guardan en Cloudinary
automáticamente, sin tocar código.

## Estructura del proyecto

- `catalog/` — categorías y productos, home, panel admin.
- `orders/` — carrito en sesión, checkout, envío de emails de pedido.
- `templates/` — HTML (incluye `templates/emails/` para los mails).
- `static/` — CSS y JS.
- `vercel.json`, `build_files.sh` — configuración de despliegue.
