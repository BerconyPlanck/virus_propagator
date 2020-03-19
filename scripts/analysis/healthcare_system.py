# -*- coding: utf-8 -*-
#
# This file is part of the virus propagator simulation.
# Copyright (C) 2020 Daniel Prelipcean.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Healthcare system."""


class HealthcareSystem:

    def __init__(self, capacity):
        self.capacity = capacity

        self.admitted_people = list()

    def treat_person(self, person):
        if person.is_infected():
            if not person.is_hospitalized():
                if len(self.admitted_people) <= self.capacity:
                    person.get_hospitalized()
                    self.admitted_people.append(person)

        if person.is_hospitalized():
            if person.is_recovered() or person.is_dead():
                person.get_out_of_hospital()

                self.admitted_people.remove(person)

    def is_capacity_reached(self):
        if len(self.admitted_people) >= self.capacity:
            print("Healthcare System capacity reached.")
