# -*- coding: utf-8 -*-
#
# This file is part of the virus propagator simulation.
# Copyright (C) 2020 Daniel Prelipcean.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Population and person implementation."""


import numpy as np

from parameters.user_parameters import displacement, FEATURES, improvement_factor_hospitalized_recovery, \
    improvement_factor_hospitalized_death
from parameters.virus_parameters import min_recovery_time, max_recovery_time, data_age, incubation_time,  \
    p_get_recovered, p_get_infected, p_dies, data_gender

from utils.binomial_expansion import find_incremental_probability


class Person:
    def __init__(self, age=None, gender=None):
        self.age = age
        if age:
            self.risk_age = self.find_risk_age(age)

        self.gender = gender
        if gender:
            self.risk_gender = self.find_risk_gender(gender)

        self.healthy = 1
        self.infected = 0
        self.recovered = 0
        self.dead = 0

        self.hospitalized = 0

        self.time = 0
        self.contact_time = None

        self.personal_incubation_time = np.random.randint(low=incubation_time[0], high=incubation_time[1]+1)
        self.personal_recovery_time = np.random.randint(low=min_recovery_time, high=max_recovery_time+1)

    def set_position(self, space_x, space_y):
        """Set the position of this person in the physical world.

        Parameters
        ----------
        space_x: int
            Physical world size on x coordinate.
        space_y: int
            Physical world size on y coordinate.
        """
        self.space_x = space_x
        self.space_y = space_y

        self.x = np.random.randint(space_x)
        self.y = np.random.randint(space_y)

    def get_position(self):
        """Return the position of this person."""
        return self.x, self.y

    def motion(self, i):

        if not self.dead:
            dx, dy = int((np.random.randint(displacement+1))-(displacement/2)), \
                     int((np.random.randint(displacement+1))-(displacement/2))

            self.x += dx
            self.y += dy

            if self.x >= self.space_x or self.x < 0:
                self.x = self.space_x - np.abs(self.x)

            if self.y >= self.space_y or self.y < 0:
                self.y = self.space_y - np.abs(self.y)

            self.time = i

    def virus_outcome(self):
        """Decide what the virus does to this person."""
        # ToDo: add this infection mechanism
        # #If the person is infected the area becomes infected or it's counter start over
        # #The living time of the infected increases
        # if self.infected != 0:
        #     world.x[self.x,self.y] = 1
        #     self.infected_time += 1

        if self.is_infected():
            self.get_recovered_or_die()

    def is_healthy(self):
        """Return the health status of this person.

        Returns
        -------
        out: bool
        """
        return bool(self.healthy)

    def is_infected(self):
        """Return the infection status of this person.

        Returns
        -------
        out: bool
        """
        return bool(self.infected)

    def is_recovered(self):
        """Return the recovery status of this person.

        Returns
        -------
        out: bool
        """
        return bool(self.recovered)

    def is_dead(self):
        """Return the death status of this person.

        Returns
        -------
        out: bool
        """
        return bool(self.dead)

    def get_infected(self):
        """Infect this person if healthy."""
        if self.healthy == 1:
            if np.random.random() < p_get_infected:
                self.healthy = 0
                self.infected = 1
                self.recovered = 0
                self.dead = 0

                self.contact_time = self.time

    def get_recovered_or_die(self):
        """The virus can either result in a recovery, death, or no outcome."""
        time_infected = (self.time - self.contact_time)
        if time_infected > self.personal_incubation_time:
            # A person can die only after an incubation time
            self.get_death()

            if time_infected > self.personal_recovery_time:
                self.get_recovered()

    def get_recovered_probability(self):
        p_individidual_recovers = p_get_recovered
        if self.hospitalized:
            p_individidual_recovers *= improvement_factor_hospitalized_recovery
        return p_individidual_recovers

    def get_recovered(self):
        """Recover this person."""
        p_individidual_recovers = self.get_recovered_probability()

        if np.random.random() < p_individidual_recovers:
            self.healthy = 0
            self.infected = 0
            self.recovered = 1
            self.dead = 1

    def is_hospitalized(self):
        return self.hospitalized

    def get_hospitalized(self):
        self.hospitalized = 1

    def get_out_of_hospital(self):
        self.hospitalized = 0

    def die(self):
        """Set this person status to dead."""
        self.healthy = 0
        self.infected = 0
        self.recovered = 0
        self.dead = 1

    def compute_death_probability(self):
        p_individidual_dies = p_dies
        if self.age:
            p_individidual_dies = self.risk_age
        if self.gender:
            p_individidual_dies += self.risk_gender
            p_individidual_dies /= 2

        if self.hospitalized:
            p_individidual_dies /= improvement_factor_hospitalized_death

        return p_individidual_dies

    def get_death(self):
        """Inflict death upon this person."""

        p_individidual_dies = self.compute_death_probability()

        if np.random.random() < p_individidual_dies:
            self.die()

    def get_status(self):
        """Get the current status of the person.

        Returns
        -------
        out: [0, 1, 2, 3]
        """
        if self.infected == 1:
            status = 1
        elif self.recovered == 1:
            status = 2
        elif self.dead == 1:
            status = 3
        else:
            status = 0
        return status

    def get_gender(self):
        """Return the gender of this person.

        Returns
        -------
        out: ['female', 'male']
        """
        return self.gender

    def get_age(self):
        """Return the age of this person.

        Returns
        -------
        out: int
        """
        return self.age

    @staticmethod
    def find_risk_age(age):
        """Find the risk of this person dying based on their age.

        Parameters
        ----------
        age: int

        Returns
        -------
        out: float
            Probability (between 0 and 1) of death
        """
        risk_age = None
        for key in data_age.keys():
            if int(key[0:2]) <= age <= int(key[-2:]):
                risk_age = float(data_age[key][:-1])/100
        risk_age = find_incremental_probability(risk_age)
        return risk_age

    @staticmethod
    def find_risk_gender(gender):
        """Find the risk of this person dying based on their gender.

        Parameters
        ----------
        gender: str

        Returns
        -------
        out: float
            Probability (between 0 and 1) of death
        """
        risk_gender = float(data_gender[gender][:-1])/100
        risk_gender = find_incremental_probability(risk_gender)
        return risk_gender


class Population:
    """Class implementing a population of several Persons."""

    def __init__(self, number_of_people):
        """

        Parameters
        ----------
        number_of_people: int
            Population size.
        """
        self.people = []
        self.number_of_people = number_of_people

    def initialize_population(self):
        """Initialize the population of size number_of_people."""
        self._create_population()
        self._initialize_infected_people()

    def _create_population(self):
        for i in range(self.number_of_people):
            age = self._distribution_age()
            gender = self._distribution_gender()

            self.people.append(Person(age, gender))

    def _initialize_infected_people(self):
        self.people[0].infected = 1
        self.people[0].contact_time = 0

    @staticmethod
    def _distribution_age():
        if FEATURES['consider_age']:
            age = np.random.randint(low=0, high=99 + 1)
        else:
            age = None
        return age

    @staticmethod
    def _distribution_gender():
        if FEATURES['consider_gender']:
            gender = np.random.choice(['male', 'female'])
        else:
            gender = None
        return gender
