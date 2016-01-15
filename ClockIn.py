import datetime
import shelve
import json
from models import TimeSheet


class ClockIn(object):

    @property
    def __shelf_name(self):
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
        return TimeSheet.select().order_by(TimeSheet.id.desc())[0].id

    @staticmethod
    def _is_clocked_in(time_id):
        return TimeSheet.get(TimeSheet.id == time_id).time_out is None

    def punch_in(self):

        if self._is_clocked_in(self._get_newest()):
            return self._response()

        ts = datetime.datetime.utcnow()
        t = TimeSheet(time_in=ts, user_id=1)
        t.save()

        ts_iso = ts.isoformat()
        return self._response(response={"ts": ts_iso})

    def punch_out(self):
        row_id = self._get_newest()
        if not self._is_clocked_in(row_id):
                return self._response()

        ts = datetime.datetime.utcnow()
        q = TimeSheet.update(time_out=ts).where(TimeSheet.id == row_id)
        q.execute()

        ts_iso = ts.isoformat()
        return self._response(response={"ts": ts_iso})

    def total_time_today(self):
        duration = self._sum_of_durs(self.__shelf_name)
        return self._response(response={'msg': "{} hours".format(duration)})

    def _sum_of_durs(self, shelf_name):
        durations = []
        with shelve.open(shelf_name, writeback=True) as shelf:
            for entry in shelf:
                start = shelf[entry]['in']
                if shelf[entry]['out']:
                    finish = shelf[entry]['out']
                else:
                    finish = datetime.datetime.now()
                duration = finish - start
                durations.append(duration.total_seconds())

        sum_of_durs = sum(durations)
        return self._get_hours(sum_of_durs)

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

        #get today's iso number
        today = datetime.datetime.utcnow()
        today_iso = datetime.datetime.utcnow().isoweekday()

        # store monday reference by finding difference between
        # current iso number and 1 then subtracting the difference
        # which will always result in 1 which is monday
        td = datetime.timedelta(days=today_iso - 1)
        weekday = today - td

        #start the while loop to add the times
        counter = 0
        sum_of_durs = 0.0
        shelf = None
        while counter <= 7:

            # #printweekday.isoweekday()
            fn = weekday.date().isoformat()
            print(fn)
            try:
                shelf_name = fn
                day_durs_sum = self._sum_of_durs(shelf_name)

                summary[iso_day_lookup[
                    weekday.isoweekday()
                ]] = day_durs_sum

                sum_of_durs += day_durs_sum
            except Exception as e:
                raise Exception(str(e))
                pass
            #increment the timedelta
            counter += 1
            td = datetime.timedelta(days=1)
            weekday = weekday + td

        summary['message'] = "{} hours this week".format(sum_of_durs)
        return self._response({'msg': summary})

    @staticmethod
    def _get_hours(seconds):
        return round((seconds / 60) / 60, 2)

    def list_entries_for_day(self):
        shelf_list = []
        with shelve.open(self.__shelf_name, writeback=True) as shelf:
            for entry in shelf:
                isofied = {'in': shelf[entry]['in'].isoformat()}
                if shelf[entry]['out']:
                    isofied['out'] = shelf[entry]['out'].isoformat()

                shelf_list.append(isofied)

        return self._response(response=sorted(shelf_list, key=lambda dct: dct['in']))

if __name__ == "__main__":

    c = ClockIn()
    print(c.punch_out())
