import peewee
import settings
from playhouse.db_url import connect
from playhouse.pool import PooledMySQLDatabase


mysql_db = PooledMySQLDatabase(settings.db_name, **settings.kwargs)


class User(peewee.Model):
    username = peewee.CharField(unique=True)

    class Meta:
        database = mysql_db


class TimeSheet(peewee.Model):

    time_in = peewee.DateTimeField()
    time_out = peewee.DateTimeField(null=True)
    user_id = peewee.ForeignKeyField(User)

    class Meta:
        database = mysql_db


if __name__ == '__main__':
    pass
    # mysql_db.connect()
    # mysql_db.create_tables([TimeSheet])
    # u = User(username='2achary')
    # u.save()



