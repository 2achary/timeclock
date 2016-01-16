import datetime
import shelve
import json
from models import TimeSheet


class ClockIn(object):

    @property
    def _today_iso(self):
        return datetime.datetime.utcnow().isoformat().split('T')[0]

    @staticmethod
    def _response(response=None):
        ret = {}
        if not response:
            ret['processed'] = False
        else:
            ret['processed'] = True
            ret['response'] = response
        return json.dumps(ret)

    @staticmethod
    def _get_newest():
        try:
            return TimeSheet.select().order_by(TimeSheet.id.desc())[0].id
        except Exception:
            pass

    @staticmethod
    def _is_clocked_in(time_id):
        try:
            return TimeSheet.get(TimeSheet.id == time_id).time_out is None
        except Exception:
            return False

    def punch_in(self):

        if self._is_clocked_in(self._get_newest()):
            return self._response()

        ts = datetime.datetime.utcnow()
        t = TimeSheet(time_in=ts, user_id=1)
        t.save()

        ts_iso = ts.isoformat()
        return self._response(response={"ts": ts_iso})

    def punch_out(self):
        try:
            row_id = self._get_newest()
            if not self._is_clocked_in(row_id):
                return self._response()
        except Exception:
            return self._response()

        ts = datetime.datetime.utcnow()
        q = TimeSheet.update(time_out=ts).where(TimeSheet.id == row_id)
        q.execute()

        ts_iso = ts.isoformat()
        return self._response(response={"ts": ts_iso})

    def _get_todays_records(self, day_offset=0):
        # central time is 6 hours before utc
        td_hours = datetime.timedelta(hours=6)
        # get today
        today = datetime.datetime.utcnow()
        print('today minus 6 hours: ', today)
        # apply offset
        today = today + datetime.timedelta(days=day_offset)
        print('today plus the offset: ', today)

        # drop everything smaller than day and for some reason
        # today.replace(hour=0, minute=0, second=0, microsecond=0)
        # was not working at all. so this is my work around
        day = datetime.datetime(today.year, today.month, today.day)
        print('gutted day: ', day)
        # get some time deltas for some UTC math

        td_day = datetime.timedelta(days=1)
        date_min = day

        date_max = day + td_day
        print(date_min, date_max)
        return TimeSheet.select().where(
            TimeSheet.time_in <= date_max, TimeSheet.time_in >= date_min)

    def total_time_today(self, day_offset=0):

        duration = 0
        entries = self._get_todays_records(day_offset=day_offset)
        for entry in entries:
            start = entry.time_in
            if entry.time_out:
                finish = entry.time_out
            else:
                finish = datetime.datetime.utcnow()
            duration += (finish - start).total_seconds()
        duration_hours = self._get_hours(duration)
        return self._response(response={'msg': duration_hours})

    def total_time_this_week(self):

        summary = {}

        iso_day_lookup = {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday",
            7: "Sunday"
        }

        # get today's iso number
        # so there is a 6 hour difference for central
        # I have to store two isoweekday values because half the damn day
        # is a day ahead if you go by utc. So I have to query the utc dates
        # but attribute those durations to centraltime isoweekday
        td_hours = datetime.timedelta(days=6)
        # which is utc today
        today = datetime.datetime.utcnow()
        today_central = datetime.datetime.utcnow() - td_hours
        today_iso = today_central.isoweekday()
        utc_iso = today.isoweekday()

        # store monday reference by finding difference between
        # current iso number and 1 then subtracting the difference
        # which will always result in 1 which is monday
        offset = datetime.timedelta(days=today_iso - 1)
        day_offset = -(utc_iso - 1)
        weekday = today - offset

        #start the while loop to add the times
        counter = 0
        sum_of_durs = 0.0
        while counter <= 7:

            res = self.total_time_today(day_offset=day_offset)
            day_total = json.loads(res)['response']['msg']
            sum_of_durs += day_total

            summary[iso_day_lookup[
                weekday.isoweekday()
            ]] = round(day_total, 2)

            # increment the weekday and counter
            counter += 1
            td = datetime.timedelta(days=1)
            weekday = weekday + td
            day_offset += 1

        summary['message'] = "{} hours this week".format(round(sum_of_durs, 2))
        return self._response({'msg': summary})

    @staticmethod
    def _get_hours(seconds):
        return round((seconds / 60) / 60, 2)

    def list_entries_for_day(self):
        shelf_list = []

        for entry in self._get_todays_records():
            isofied = {'in': entry.time_in.isoformat()}
            if entry.time_out:
                isofied['out'] = entry.time_out.isoformat()

            shelf_list.append(isofied)

        return self._response(response=sorted(shelf_list, key=lambda dct: dct['in']))

if __name__ == "__main__":

    c = ClockIn()
    print(c.list_entries_for_day())
