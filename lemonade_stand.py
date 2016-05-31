#!/usr/bin/env python

""" Simple version of classic lemonade stand game. Written in Python 2.7
"""

__author__ = 'Rich von Lehe'

import random


class Day:
    """ Day responsible for things that change daily
    """

    def __init__(self):
        self.day = 0
        self.weather = 0
        self.lemonade_price = 0

    def new_day(self):
        self.day += 1
        self._update_lemonade_price()
        self._update_weather()

        print("Today's weather: %d" % self.weather)
        print("Cost per cup of lemonade: " + str(float(self.lemonade_price) / 100))
        print

    def demand(self, price):
        cups = random.randrange(1, 101)
        price_factor = float(100 - price) / 100
        heat_factor = 1 - (((100 - self.weather) * 2) / float(100))
        demand = 0

        if 0 == price:
            demand += cups + random.randrange(1, 100)   # Additional demand when free

        demand += int(round(cups * price_factor * heat_factor))

        return demand

    def _update_lemonade_price(self):
        self.lemonade_price = random.randrange(1, 10)

    def _update_weather(self):
        self.weather = random.randrange(50, 100)


class Game:
    """ Game class enables multi-player lemonade
    """

    def __init__(self):
        """ setup initial parameters
        """
        self.players = 0
        self.day = Day()
        self.active = True
        self.lemonade_stands = []

    def _run_day(self):
        self.day.new_day()

        for stand in self.lemonade_stands:
            stand.run(self.day)

        print('Day:     ' + str(self.day.day))
        print('Weather: ' + str(self.day.weather))

        for stand in self.lemonade_stands:
            stand.print_summary()
            print

    def _get_players(self):
        while True:
            try:
                self.players = int(raw_input('How many players are there (1-3)?'))
                if self.players not in range(1, 4):
                    raise ValueError
                else:
                    break
            except ValueError:
                print('Please choose a number from 1 to 3')

        for i in range(1, self.players + 1):
            print('Enter a name for player %d \n' % i)
            name = raw_input()
            self.lemonade_stands += [LemonadeStand(name)]

    def _prompt_continue(self):
        while True:
            print('Press 1 to continue, 2 to quit')
            try:
                choice = int(raw_input())
                if choice in range(1, 3):
                    break
            except ValueError:
                pass  # TODO

        if 2 == choice:
            print('Are you sure you want to quit? (y/n)')
            choice = raw_input()

            if 'y' == choice:
                self.active = False

    def run(self):
        self._get_players()

        while self.active:
            self._run_day()

            self._prompt_continue()


class LemonadeStand:
    """ LemonadeStand keeps track of player-specific data
    """

    def __init__(self, name):
        self.name = name
        self.lemonade = 0
        self.cash = 100.00
        self.cups_sold = 0
        self.cost_to_make = 0
        self.cups_made = 0
        self.earnings = 0.0
        self.cups_demanded = 0

        print('Lemonade stand owned by %s\n' % self.name)

    def run(self, day):
        """ Get decision and update lemonade, cash, """

        self.cups_made = 0
        self.cups_sold = 0
        self.cups_demanded = 0
        self.earnings = 0

        while True:
            print('%s: 1 to make lemonade, 2 to sell lemonade' % self.name)
            try:
                choice = int(raw_input())
                if choice in range(1, 3):
                    break
                else:
                    raise ValueError

            except ValueError:
                print('Please try again')

        if 1 == choice:
            self._make_lemonade(day)
        elif 2 == choice:
            self._sell_lemonade(day)

    def _make_lemonade(self, day):
        while True:
            try:
                self.cups_made = int(raw_input('How many cups will you make (1-10)?'))
                if self.cups_made in range(1, 11):
                    break
                else:
                    raise ValueError

            except ValueError:
                print('You must choose an integer from 1 to 10')
        self.lemonade += self.cups_made
        self.cost_to_make = self.cups_made * (float(day.lemonade_price) / 100)
        self.cash -= self.cost_to_make

    def _sell_lemonade(self, day):
        while True:
            try:
                price = int(raw_input('How many cents will you charge per cup of lemonade? (0-100)?'))
                if price in range(0, 101):
                    break
                else:
                    raise ValueError
            except ValueError:
                pass

        self.cups_demanded = day.demand(price)

        if self.cups_demanded <= self.lemonade:
            self.lemonade -= self.cups_demanded
            self.cups_sold = self.cups_demanded
        else:
            self.cups_sold = self.lemonade
            self.lemonade = 0

        self.earnings = self.cups_sold * (float(price) / 100)
        self.cash += self.earnings

    def print_summary(self):
        print('Player: %s' % self.name)
        print('---------------')
        print('Total lemonade: %d' % self.lemonade)
        print('Demand: %d' % self.cups_demanded)
        print('Cups sold: %d' % self.cups_sold)
        print('Earnings: %.02f' % (round(self.earnings, 2)))
        print('Cash: %.02f' % (round(self.cash, 2)))


def main():
    game = Game()

    game.run()


main()