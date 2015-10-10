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

    def punch_in(self):
        shelf = shelve.open(self.__shelf_name)
        if 'is-clocked-in' not in shelf:
            shelf['is-clocked-in'] = False
        is_clocked_in = shelf['is-clocked-in']

        if not is_clocked_in:
            time_stamp = datetime.datetime.now()
            key_name = time_stamp.isoformat()
            shelf['is-clocked-in'] = True
            entry = {"in": None, "out": None}
            entry['in'] = time_stamp
            shelf[key_name] = entry
            shelf['most_recent'] = key_name
            shelf.close()
            return "\nClocked in at {}".format(time_stamp.strftime(self.__time_format))
        else:
            return "Already clocked in"

    def punch_out(self):

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
            start = entry['in']
            finish = entry['out']
            duration = finish - start
            if 'durations' not in shelf:
                shelf['durations'] = []
            durations = shelf['durations']
            durations.append(duration.total_seconds())
            shelf['durations'] = durations
            # shelf.close()
            return "\nClocked out at {}\n".format(time_stamp.strftime(self.__time_format))
        else:
            return "\nNot clocked in\n"

    def total_time_today(self):
        shelf = shelve.open(self.__shelf_name)
        if 'durations' not in shelf:
                shelf['durations'] = []
        sum_of_durs = sum(shelf['durations'])
        shelf.close()
        minutes = sum_of_durs/60
        hours = minutes/60
        return "{} hours".format(round(hours, 2))

    def total_time_this_week(self):
        today = datetime.datetime.today()
        today_iso = datetime.datetime.today().isoweekday()
        td = datetime.timedelta(days=today_iso - 1)
        weekday = today - td
        print(weekday.isoweekday())
        counter = 0
        sum_of_durs = 0
        shelf = None
        while counter <= 7:
            td = datetime.timedelta(days=1)
            weekday = weekday + td
            # #printweekday.isoweekday()
            fn = "{}_timesheet.shelf.db".format(weekday.date().isoformat())

            if path.isfile(fn):
                # #print"it's a file"
                shelf = shelve.open(fn)

                if 'durations' in shelf:
                    durs = shelf['durations']
                    durs = sum(durs)
                    sum_of_durs += durs
            counter += 1
        if shelf:
            shelf.close()
        return sum_of_durs

    def change_day(self, time_delta):
        td = datetime.timedelta(days=time_delta)
        self.__today -= td

    def list_entries_for_day(self):
        shelf = shelve.open(self.__shelf_name)
        shelf_list = []
        shelf_objects = []

        for entry in shelf:
            if entry == 'most_recent' or entry == 'durations' or entry == 'is-clocked-in':
                continue
            shelf_objects.append(shelf[entry])

        for entry in shelf_objects:
            readable = {}
            readable['in'] = entry['in'].strftime(self.__time_format)

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
    print(c.total_time_this_week())
