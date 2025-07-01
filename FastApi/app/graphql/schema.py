import graphene
from graphene import ObjectType, String, Int, Field, List
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models.user import User
from app.database.database import SessionLocal, get_db

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)

    posts = List(lambda: PostObject)

    def resolve_posts(self, info):
        return self.posts

class Query(ObjectType):
    # Definimos los campos que queremos consultar
    hello = graphene.String()
    users = graphene.List(UserObject)
    user = graphene.Field(UserObject, id=Int())

    def resolve_hello(self, info):
        return "¡Hola desde GraphQL!"

    def resolve_users(self, info):
        db = SessionLocal()
        try:
            return db.query(User).all()
        finally:
            db.close()

    def resolve_user(self, info, id):
        db = SessionLocal()
        try:
            return db.query(User).filter(User.id == id).first()
        finally:
            db.close()

schema = graphene.Schema(query=Query, auto_camelcase=False)
