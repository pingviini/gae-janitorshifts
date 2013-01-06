# -*- coding: utf-8 -*-

import calendar
import csv
import logging

from datetime import datetime
from finnish_flag_days import FinnishFlagDays


class Janitorshifts(object):
    """
    Janitorshifts class takes dict of apartments as a parameter and creates
    shifts for the current year. Dict contsists from corridor letter (key)
    and apartment nubmers as a list for current corridor (value).

    Eg. {'A': [1,2]}
    """
    def __init__(self, apartmentsdict, year=None, start=None, end=None):
        self.year = year or datetime.now().year
        self.flagdays = FinnishFlagDays(self.year)
        self.year_dates = calendar.Calendar().yeardatescalendar(self.year,
                                                                width=1)
        self.apartmentsdict = apartmentsdict
        self.apartmentlist = self.countApartments()

        if start:
            self.reorderApartmentListByStart(start)
        elif end:
            self.reorderApartmentListByEnd(end)


    def create_shifts(self):
        shifts = self.get_shifts()
        janitorshifts = []

        for week, data in shifts.items():
            row = {'week': week,
                   'start': data['start'].strftime("%d.%m.%Y"),
                   'end': data['end'].strftime("%d.%m.%Y"),
                   'apartment': data['apartment'],  # .encode('utf-8'),
                   'flagday': self.getWeekFlagdays(data['flagdays'])}
            janitorshifts.append(row)

        return janitorshifts

    def create_csv(self, *args, **kwargs):
        shifts = self.get_shifts()
        csvfile = open('vuorot-%s.csv' % self.year, 'wt')
        csvwriter = csv.writer(csvfile, dialect='excel')

        for week, data in shifts.items():
            row = {'week': week,
                   'start': data['start'].strftime("%d.%m.%Y"),
                   'end': data['end'].strftime("%d.%m.%Y"),
                   'apartment': data['apartment'],  # .encode('utf-8'),
                   'flagday': self.getWeekFlagdays(data['flagdays'])}
                   #.encode('utf-8')}

            csvwriter.writerow((
                'Viikko %s' % week,
                '%s - %s' % (row['start'], row['end']),
                'Asunto %s' % row['apartment'],
                row['flagday'][1:]))

            print "Viikko %(week)s (%(start)s - %(end)s): Asunto \
%(apartment)s%(flagday)s" % row

        csvfile.close()

    def getWeekFlagdays(self, flagdays):
        """Return string containing all the flagdays."""
        tmp = ""
        if len(flagdays.keys()) > 0:
            for day in flagdays.keys():
                tmp += "%s - %s, " % (day.strftime('%d.%m.%Y'), flagdays[day])
            tmp = tmp.rstrip()
            tmp = tmp[:-1] + '.'
        return tmp

    def countApartments(self):
        apartments = []
        for (door, numbers) in self.apartmentsdict.items():
            for number in numbers:
                apartments.append('%s%s' % (door, number))
        return sorted(apartments)

    def reorderApartmentListByStart(self, start):
        while self.apartmentlist[0] != start:
            self.apartmentlist.insert(0, self.apartmentlist.pop())

    def reorderApartmentListByEnd(self, end):
        tmp = self.apartmentlist[:]
        while len(tmp) < 52:
            tmp = tmp*2

        while tmp[51] != end:
            tmp.insert(0, tmp.pop())

        self.apartmentlist = tmp[0:len(self.apartmentlist)]

    def get_shifts(self):
        yeardates = self.year_dates
        shifts = {}
        logging.info(self.apartmentlist)
        apartmentlist = self.apartmentlist * 10

        # Remove week 52 and 53 from list. These are handled by last years
        # listing.
        if yeardates[0][0][0][0].isocalendar()[1] in [52, 53]:
            yeardates[0][0].pop(0)

        for month in yeardates:
            for week in month[0]:
                weeknumber = week[0].isocalendar()[1]
                logging.info("Processing week %s" % str(weeknumber))
                if weeknumber not in shifts.keys():
                    flagdays = {}
                    for day in week:
                        if day in self.flagdays().keys():
                            flagdays[day] = self.flagdays()[day]

                    weekdata = {
                        'start': week[0],
                        'end': week[-1],
                        'apartment': apartmentlist.pop(0),
                        'flagdays': flagdays
                    }
                    logging.info("Weekdata: %s" % str(weekdata))
                    logging.info("Inserting weekdata to week %s" % str(weeknumber))
                    shifts[weeknumber] = weekdata

        return shifts

    def get_week_number(self, date):
        """Return week number for given date."""
        try:
            return date.isocalendar()[1]
        except IndexError:
            return None
        except AttributeError:
            return None

    def get_month_weekdates_as_list(self, year, month):
        """Return month weeks as list."""
        yearlist = calendar.Calendar.yeardatescalendar(year, width=1)
        return yearlist[month][0]


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        try:
            vuorot = Janitorshifts(int(sys.argv[1]), sys.argv[2])
        except ValueError, e:
            print("\nPlease give a proper year. Showing the current years "
                  "shifts.\n")
            vuorot = Janitorshifts()
    else:
        vuorot = Janitorshifts()
