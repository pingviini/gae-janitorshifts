#!/usr/bin/env python

import cgi
import webapp2
import jinja2
import os
import logging
import re
import datetime

from janitorshifts import Janitorshifts


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):

    def get(self):
        template_values = {}

        start_apartment = self.request.get('start_apartment', None)
        end_apartment = self.request.get('end_apartment', None)
        apartments = self.request.get('apartments', None)

        if start_apartment:
            start_apartment = start_apartment.upper()
        if end_apartment:
            end_apartment = end_apartment.upper()
        if apartments:
            apartments = apartments.upper()

        year = self.request.get('year', datetime.datetime.now().year)

        if apartments:
            apartmentsdict = self.prepare_apartments(apartments)
            apartmentslist = self.get_apartments_list(apartmentsdict)
            apartmentslist.sort()
            janitor = Janitorshifts(apartmentsdict, year=int(year),
                                    start=start_apartment, end=end_apartment)
            shifts = janitor.create_shifts()

            template_values['apartments'] = apartments
            template_values['apartmentsdict'] = apartmentsdict
            template_values['shifts'] = shifts
            template_values['nextyear'] = int(year) + 1
            template_values['year'] = year
            template_values['previousyear'] = int(year) - 1
            template_values['next_start_apartment'] =\
                self.get_next_apartment(apartmentslist,
                                        shifts[-1]['apartment'])
            template_values['previous_start_apartment'] =\
                self.get_previous_apartment(apartmentslist,
                                            shifts[0]['apartment'])

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

    def prepare_apartments(self, apartments):
        """Return dict of apartments (eg. {'A': [1,2,3]})."""
        tmp = apartments.split(',')
        apartmentsdict = {}

        for apartment in tmp:
            data = re.findall("\w", apartment)
            key = data[0]
            apartment_numbers = data[1:]
            logging.info(apartment_numbers)
            value = range(int(apartment_numbers[0]),
                          int(apartment_numbers[1]) + 1)
            apartmentsdict[key] = value

        logging.info(apartmentsdict)
        return apartmentsdict

    def get_apartments_list(self, apartmentsdict):

        apartmentslist = []

        for key, value in apartmentsdict.items():
            for number in value:
                apartmentslist.append(key + str(number))

        return apartmentslist

    def get_previous_apartment(self, apartmentslist, current):
        return apartmentslist[apartmentslist.index(current) - 1]

    def get_next_apartment(self, apartmentslist, current):
        try:
            return apartmentslist[apartmentslist.index(current) + 1]
        except IndexError:
            return apartmentslist[0]


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
