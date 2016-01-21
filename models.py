import peewee
import settings
from playhouse.db_url import connect
from playhouse.pool import PooledMySQLDatabase
from flask.ext.login import UserMixin
import datetime
from flask.ext.bcrypt import generate_password_hash as make_hash
from flask.ext.bcrypt import check_password_hash as check_hash


mysql_db = PooledMySQLDatabase(settings.db_name, **settings.kwargs)


class User(UserMixin, peewee.Model):
    username = peewee.CharField(unique=True)
    email = peewee.CharField(unique=True)
    password = peewee.CharField(max_length=100)
    joined_at = peewee.DateTimeField(default=datetime.datetime.now)
    is_admin = peewee.BooleanField(default=False)


    class Meta:
        database = mysql_db

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=make_hash(password),
                is_admin=admin)
        except peewee.IntegrityError:
            raise ValueError('User already exists')


class TimeSheet(peewee.Model):

    time_in = peewee.DateTimeField()
    time_out = peewee.DateTimeField(null=True)
    user_id = peewee.ForeignKeyField(User)

    class Meta:
        database = mysql_db


def initialize():
    mysql_db.connect()
    mysql_db.create_tables([User], safe=True)
    mysql_db.close()


# if __name__ == '__main__':

    # mysql_db.connect()
    # TimeSheet.drop_table()
    # User.drop_table()
    # mysql_db.create_tables([User, TimeSheet])
    # # u = User(username='2achary')
    # # u.save()
    # mysql_db.close()



