from peewee import *

db = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Player(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    age = IntegerField()


class Position(BaseModel):
    id_player = ForeignKeyField(Player, to_field='id')
    position = CharField()

    class Meta:
        primary_key = CompositeKey('id_player', 'position')


class Skills(BaseModel):
    id_player = ForeignKeyField(Player, to_field='id')
    skill = CharField()
    value = IntegerField()

    class Meta:
        primary_key = CompositeKey('id_player', 'skill')


class Statistics(BaseModel):
    id_player = ForeignKeyField(Player, to_field='id')
    tournament = CharField()
    games = IntegerField()
    goals = IntegerField()
    passing = IntegerField()
    rating = FloatField()

    class Meta:
        primary_key = CompositeKey('id_player', 'tournament')


def add_in_database(table: [BaseModel], data: list[dict]):
    db.create_tables([Player, Position, Skills, Statistics])
    table.insert_many(data).on_conflict_replace().execute()
