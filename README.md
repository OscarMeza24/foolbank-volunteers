# Sistema de Gestión de Voluntarios para Banco de Alimentos

Este proyecto es una aplicación web desarrollada con Django que facilita la gestión de voluntarios para bancos de alimentos.

## Características Principales

- Gestión de voluntarios
- Sistema de registro y autenticación
- Panel de administración para gestionar voluntarios
- Interfaz intuitiva y fácil de usar

## Requisitos

- Python 3.8 o superior
- Django
- SQLite (base de datos predeterminada)
- Otros paquetes especificados en requirements.txt

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/OscarMeza24/foolbank-volunteers.git
```

2. Crea un entorno virtual:
```bash
python -m venv venv
```

3. Activa el entorno virtual:
```bash
# Windows
venv\Scripts\activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Aplica las migraciones:
```bash
python manage.py migrate
```

6. Crea un superusuario (opcional):
```bash
python manage.py createsuperuser
```

7. Ejecuta el servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

- `foodbankvoluntarios/`: Aplicación principal
- `db.sqlite3`: Base de datos SQLite
- `manage.py`: Script de gestión de Django
- `venv/`: Entorno virtual de Python

## Contribución

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto

Para preguntas o soporte, por favor contacta a:
- Email: omeza2411@gmail.com
- GitHub: OscarMeza24
