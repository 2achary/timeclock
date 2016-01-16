import peewee
import settings
from playhouse.db_url import connect

mysql_db = connect(settings.mysql_url)


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
    # mysql_db.connect()
    # mysql_db.create_tables([TimeSheet, User])
    # u = User(username='2achary')
    # u.save()
    import datetime
    ts = datetime.datetime.utcnow()
    # t = TimeSheet(time_in=ts, user_id=1)
    # t.save()
    # q = TimeSheet.update(time_out=ts).where(TimeSheet.id == 2)
    # q.execute()
        # print(ts.time_in)
        # print(ts.id)
        # print(ts.time_out)
            # get today
    today = datetime.datetime.utcnow()
    # drop the minutes and hours and all that
    today.replace(hour=0, minute=0, second=0, microsecond=0)
    # get some time deltas for some UTC math
    td_hours = datetime.timedelta(hours=6)
    td_day = datetime.timedelta(days=1)
    date_min = today - td_hours
    date_max = today + td_day - td_hours

    for ts in TimeSheet.select().where(TimeSheet.time_in <= date_max and TimeSheet.time_in >= date_min):
        print(ts.time_in - td_day)

