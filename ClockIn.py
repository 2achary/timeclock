import datetime
import shelve
import json
import time
from os import path


class ClockIn(object):
    __time_format = '%I:%M:%S %p'
    __datetime_format = '%Y-%m-%d %I:%M:%S %p'
    __today = datetime.datetime.today()
    __edit_date = None
    __todays_date = __today.date(
            ).isoformat()
    __shelf_name = '{}_timesheet.shelf'.format(__todays_date)
    __edit_shelf_name = '{}_timesheet.shelf'.format(__edit_date)

    def _get_today(self):
        self.__todays_date = datetime.datetime.today().date().isoformat()

    def punch_in(self):
        self._get_today()
        shelf = shelve.open(self.__shelf_name)
        if 'is-clocked-in' not in shelf:
            shelf['is-clocked-in'] = False
        is_clocked_in = shelf['is-clocked-in']

        if not is_clocked_in:
            time_stamp = datetime.datetime.now()
            key_name = time_stamp.isoformat()
            shelf['is-clocked-in'] = True
            entry = {"in": time_stamp, "out": None}
            shelf[key_name] = entry
            shelf['most_recent'] = key_name
            shelf.close()
            return "\nClocked in at {}".format(time_stamp.strftime(
                self.__time_format))
        else:
            return "Already clocked in"

    def punch_out(self):
        self._get_today()
        shelf = shelve.open(self.__shelf_name)

        if 'is-clocked-in' not in shelf:
            shelf['is-clocked-in'] = False
        is_clocked_in = shelf['is-clocked-in']

        if is_clocked_in:
            shelf['is-clocked-in'] = False
            time_stamp = datetime.datetime.now()
            entry = shelf[shelf['most_recent']]
            entry['out'] = time_stamp
            shelf[shelf['most_recent']] = entry
            shelf.close()

            return "\nClocked out at {}\n".format(time_stamp.strftime(
                self.__time_format))
        else:
            return "\nNot clocked in\n"

    def total_time_today(self):
        self._get_today()
        shelf = shelve.open(self.__shelf_name)
        duration = self._sum_of_durs(shelf)
        return "{} hours".format(duration)

    def _sum_of_durs(self, shelf_name):
        durations = []

        for entry in shelf_name:
            if entry == 'most_recent' or entry == 'durations' or (
                        entry == 'is-clocked-in'):
                continue
            else:
                start = entry['in']
                if entry['out']:
                    finish = entry['out']
                else:
                    finish = datetime.datetime.now()
                duration = finish - start
                durations.append(duration.total_seconds())

        sum_of_durs = sum(durations)
        shelf_name.close()
        return round(self._get_hours(sum_of_durs), 2)

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
        today = datetime.datetime.today()
        today_iso = datetime.datetime.today().isoweekday()

        #store monday reference
        td = datetime.timedelta(days=today_iso - 1)
        weekday = today - td

        #start the while loop to add the times
        counter = 0
        sum_of_durs = 0
        shelf = None
        while counter <= 7:

            # #printweekday.isoweekday()
            fn = "{}_timesheet.shelf.db".format(weekday.date().isoformat())
            print(fn)
            if path.isfile(fn):

                # #print"it's a file"
                shelf_name = fn[:-3]

                day_durs_sum = self._sum_of_durs(shelf_name)

                summary[iso_day_lookup[
                    weekday.isoweekday()
                ]] = day_durs_sum

                sum_of_durs += day_durs_sum
                shelf.close()

            #increment the timedelta
            counter += 1
            td = datetime.timedelta(days=1)
            weekday = weekday + td

        summary['message'] = "{} hours this week".format(
            round(self._get_hours(sum_of_durs), 2))
        return json.dumps(summary)

    def _get_hours(self, seconds):
        return round((seconds / 60) / 60, 2)

    def change_day(self, time_delta):
        td = datetime.timedelta(days=time_delta)
        self.__today -= td

    def list_entries_for_day(self):
        shelf = shelve.open(self.__shelf_name)
        shelf_list = []
        shelf_objects = []

        for entry in shelf:
            if entry == 'most_recent' or entry == 'durations' or (
                    entry == 'is-clocked-in'):
                continue
            shelf_objects.append(shelf[entry])

        for entry in shelf_objects:
            readable = {'in': entry['in'].strftime(self.__time_format)}

            if entry['out']:
                readable['out'] = entry['out'].strftime(self.__time_format)

            shelf_list.append(readable)
        return json.dumps(shelf_list)

    def select_day_shelf(self, day_to_select):
        today_number = int(datetime.datetime.today().isoweekday())
        todays_date = datetime.datetime.today()

        if day_to_select < today_number:
            difference = today_number - day_to_select
            td = datetime.timedelta(days=difference)
            edit_date = (todays_date - td).date().isoformat()
            edit_shelf_name = '{}_timesheet.shelf'.format(edit_date)

            if path.isfile(edit_shelf_name + ".db"):
                return edit_shelf_name
            else:
                return

        elif day_to_select > today_number:
            difference = day_to_select - today_number
            td = datetime.timedelta(days=difference)
            edit_date = (todays_date + td).date().isoformat()
            edit_shelf_name = '{}_timesheet.shelf'.format(edit_date)

            if path.isfile(edit_shelf_name + ".db"):
                return edit_shelf_name
            else:
                return
        else:
            edit_shelf_name = '{}_timesheet.shelf'.format(todays_date.date().isoformat())
            if path.isfile(edit_shelf_name + ".db"):
                return edit_shelf_name
            else:
                return None

    def list_entry_keys(self, shelf_name):
        shelf = shelve.open(shelf_name)
        for entry in shelf:
            if entry == 'most_recent' or entry == 'durations' or entry == 'is-clocked-in':
                continue
            #printentry
        shelf.close()

    def make_edit(self, shelf_name, key_to_edit, in_or_out, update_string):
        shelf = shelve.open(shelf_name)
        entry = shelf[key_to_edit]
        update_datetime = datetime.datetime.strptime(update_string, self.__datetime_format)
        entry[in_or_out] = update_datetime
        shelf[key_to_edit] = entry
        shelf.close()
        # #print"**performed edit**"

    # def edit_entry(self):
    #     while True:
    #         #print"\n[1]: Monday, [2]: Tuesday,  [3]: Wednesday, [4]: Thursday,"
    #         #print"[5]: Friday, [6]: Saturday, [7]: Sunday/n"
    #         day_to_edit = int(raw_input("Enter day number: "))
    #         if day_to_edit in range(1, 8):
    #             day_shelf = self.select_day_shelf(day_to_edit)
    #             if day_shelf:
    #                 #print"[e]: edit entry"
    #                 #print"[d]: delete entry"
    #                 #print"[n]: new entry"
    #                 action_choice = input("Select action: ")
    #                 if action_choice == 'e':
    #                     self.list_entry_keys(day_shelf)
    #                     key_to_edit = input("choose entry from above: ")
    #                     #print"[i]: In time, [o]: Out time"
    #                     in_or_out = input("edit in or out time: ")
    #                     #print"YYYY-MM-DD HH:MM:SS AM"
    #                     user_update_string = input("enter date and time in format above: ")
    #                     self.make_edit(day_shelf, key_to_edit, in_or_out, user_update_string)
    #
    #                     break
    #             else:
    #                 #print"no record for that day"
    #         else:
    #             #print"invalid day number"


    # def user_prompt(self):
    #     while True:
    #         #print"\n[i]: punch in"
    #         #print"[o]: punch out"
    #         #print"[t]: total time"
    #         #print"[q]: quit"
    #         #print"[l]: list entrys"
    #         #print"[e]: edit entry"
    #         user_input = raw_input("Choose an option from above: ")
    #         if not user_input or user_input == 'q':
    #             break
    #         if user_input == 'i':
    #             self.punch_in()
    #         if user_input == 'o':
    #             self.punch_out()
    #         if user_input == 't':
    #             #printself.total_time_today()
    #         if user_input == 'l':
    #             #printself.list_entries_for_day()
    #         if user_input == 'e':
    #             self.edit_entry()



if __name__ == "__main__":
    c = ClockIn()
    c.punch_in()
    time.sleep(3)
    c.punch_out()
    time.sleep(3)
    print(c.total_time_this_week())
