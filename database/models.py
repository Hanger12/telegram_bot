from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)
from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)


class Commands(BaseModel):
    command_id = AutoField()
    title = CharField()
    user = ForeignKeyField(User, backref="command")

    def __str__(self):
        return f"{self.title}"


class CommandData(BaseModel):
    command_data_id = AutoField()
    command = ForeignKeyField(Commands, backref="command_data")
    page_size = IntegerField()
    platforms = CharField(null=True)
    developers = CharField(null=True)
    genres = CharField(null=True)
    page = IntegerField()

    def __str__(self):
        return (f"Платформы: {self.platforms},\n"
                f"отобразить(штук): {self.page_size},\n"
                f"Разработчики: {self.developers if self.developers is not None else "Нет"},\n"
                f"Жанр: {self.genres if self.genres is not None else "Нет"},\n")


def create_models():
    db.create_tables(BaseModel.__subclasses__())
