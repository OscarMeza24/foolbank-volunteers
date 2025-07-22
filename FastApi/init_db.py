from app.database.database import Base, engine
from app.models.models import Usuarios, Voluntarios, Eventos, Asignaciones, Feedback

print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("¡Tablas creadas exitosamente!")