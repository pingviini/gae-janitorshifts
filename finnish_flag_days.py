# -*- coding: utf-8 -*-

import logging

from datetime import date, timedelta, datetime
from calendar import Calendar


class FinnishFlagDays:

    def __init__(self, year=None):

        self.calendar = Calendar()
        self.year = year or datetime.now().year

        self.official_flag_days = {
            date(self.year, 2, 28): u'Kalevalan päivä eli suomalaisen '
                                    u'kulttuurin päivä',
            date(self.year, 5, 1): u'Vappu eli suomalaisen työn päivä',
            self.getMothersOrFathersDay(month=5): u'Äitienpäivä',
            date(self.year, 6, 4): u'Puolustusvoimien lippujuhlan päivä eli '
                                   u'Suomen marsalkka C.G.E. Mannerheimin '
                                   u'syntymäpäivä',
            self.getMidsummersDay() - timedelta(1): u'Juhannusaatto, Suomen '
                                                    u'lipun päivä',
            self.getMidsummersDay(): u'Juhannuspäivä, Suomen lipun päivä',
            date(self.year, 12, 6): u'Itsenäisyyspäivä',
        }

        self.unofficial_flag_days = {
            date(self.year, 2, 5): u'J. L. Runebergin päivä',
            date(self.year, 3, 19): u'Minna Canthin eli tasa-arvon päivä',
            date(self.year, 4, 9): u'Mikael Agricolan päivä eli suomen kielen '
                                   u'päivä',
            date(self.year, 4, 27): u'Kansallinen veteraanipäivä',
            date(self.year, 5, 12): u'J. V. Snellmanin päivä eli '
                                    u'suomalaisuuden päivä',
            self.getFallenHeroesDay(): u'Kaatuneitten muistopäivä',
            date(self.year, 7, 6): u'Eino Leinon päivä eli runon ja suven '
                                   u'päivä',
            date(self.year, 10, 10): u'Aleksis Kiven päivä eli suomalaisen '
                                     u'kirjallisuuden päivä',
            date(self.year, 10, 24): u'Yhdistyneiden kansakuntien päivä',
            date(self.year, 11, 6): u'svenska dagen, ruotsalaisuuden päivä',
            self.getMothersOrFathersDay(month=11): u'Isänpäivä',
            date(self.year, 12, 8): u'Jean Sibeliuksen päivä eli suomalaisen '
                                    u'musiikin päivä',
        }

    def __call__(self, *args, **kwargs):
        all_flag_days = {}
        all_flag_days.update(self.official_flag_days)
        all_flag_days.update(self.unofficial_flag_days)
        return all_flag_days

    def getMothersOrFathersDay(self, month):
        """
        Returns mothers day for the given year. If there is no year given,
        defaults to current year.

        - Finnish mothers day is second Sunday in May.
        - Finnish fathers day is second Sunday in November.
        """

        counter = 0
        for (day, weekday) in self.calendar.itermonthdays2(self.year, month):
            if weekday == 6:
                if counter == 0:
                    counter += 1
                else:
                    return date(self.year, month, day)

    def getMidsummersDay(self):
        """
        Returns midsummerday for the given year. If there is no year given,
        defaults to current year.

        - Midsummers day is the Saturday between 20. and 26. days in June.
        """

        for (day, weekday) in self.calendar.itermonthdays2(self.year, 6):
            if day >= 20:
                if day <= 26:
                    if weekday == 5:
                        return date(self.year, 6, day)

    def getFallenHeroesDay(self):
        """
        Returns date for flagging people fallen in war.
        - Mays third Sunday.
        """

        counter = 0
        for (day, weekday) in self.calendar.itermonthdays2(self.year, 5):
            if weekday == 6:
                if counter < 2:
                    counter += 1
                else:
                    return date(self.year, 5, day)

    def sortFlagDays(self, days_dict):
        """Returns a list of tuples which contains flagdays in sorted order."""
        return sorted(days_dict.iteritems())

    def printFlagDays(self, flagdays):
        sorted_days = self.sortFlagDays(flagdays)
        for day in sorted_days:
            print "%s: %s" % (day[0].strftime('%d.%m.%Y'), day[1])

    def printAllFlagDays(self):
        print("Official flag days")
        self.printFlagDays(flagdays=self.official_flag_days)
        print("\nUnofficial flag days")
        self.printFlagDays(flagdays=self.unofficial_flag_days)

    def isFlagday(self, date):
        """
        Returs flagday name for the given date. Returns False if date is not
        flagday.
        """

        if date in self.official_flag_days.keys():
            return self.official_flag_days[date]
        elif date in self.unofficial_flag_days.keys():
            return self.unofficial_flag_days[date]
        else:
            return False


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            flagdays = FinnishFlagDays(int(sys.argv[1]))
        except ValueError, e:
            logging.info("Please give a proper year. Showing the current "
                         "years flagdays.")
            flagdays = FinnishFlagDays()
    else:
        flagdays = FinnishFlagDays()

    flagdays.printAllFlagDays()
