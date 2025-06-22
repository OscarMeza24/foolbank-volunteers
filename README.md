# Sistema de Gestión de Voluntarios de Banco de Alimentos

<p align="center">
<a href="https://laravel.com" target="_blank"><img src="https://raw.githubusercontent.com/laravel/art/master/logo-lockup/5%20SVG/2%20CMYK/1%20Full%20Color/laravel-logolockup-cmyk-red.svg" width="200" alt="Laravel Logo"></a>
</p>

## Descripción

Este proyecto es un sistema web para la gestión de voluntarios en bancos de alimentos. Está desarrollado usando Laravel 10 y utiliza Supabase como base de datos.

## Características Principales

- Gestión completa de eventos de voluntariado
- Sistema de registro y autenticación de usuarios
- Panel de administración para organizadores
- Sistema de inscripción para voluntarios
- Integración con Supabase para almacenamiento de datos
- Interfaz web moderna y responsive

## Requisitos del Sistema

- PHP >= 8.1
- Composer
- Node.js y npm (para assets)
- Supabase cuenta (para base de datos)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPO]
cd foodbank-volunteers
```

2. Instalar dependencias:
```bash
composer install
npm install
```

3. Copiar archivo de configuración:
```bash
cp .env.example .env
```

4. Configurar variables de entorno:
- Configurar las credenciales de Supabase en el archivo `.env`
- Configurar las URLs y claves necesarias

5. Generar clave de aplicación:
```bash
php artisan key:generate
```

6. Ejecutar migraciones:
```bash
php artisan migrate
```

7. Compilar assets:
```bash
npm run build
```

8. Iniciar el servidor:
```bash
php artisan serve
```

## Estructura del Proyecto

```
foodbank-volunteers/
├── app/                 # Código de aplicación
├── database/            # Migraciones y seeders
├── public/              # Archivos públicos
├── resources/           # Vistas y assets
├── routes/              # Definición de rutas
└── tests/              # Pruebas unitarias
```

## Pruebas

Para ejecutar las pruebas:

```bash
php artisan test
```

## Contribución

1. Fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Soporte

Para reportar bugs o solicitar características, por favor usa el sistema de issues de GitHub.

## Agradecimientos

- [Laravel](https://laravel.com) - Framework PHP
- [Supabase](https://supabase.com) - Base de datos
- [Tailwind CSS](https://tailwindcss.com) - Framework de CSS
- [Alpine.js](https://alpinejs.dev) - Framework de JavaScript
