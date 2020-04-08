#!/usr/bin/python3
__version__ = '0.0.2' # Time-stamp: <2019-06-10T10:15:24Z>
## Language: Japanese/UTF-8

"""A Simple Simulation of Asset Market."""

##
## License:
##
##   Public Domain
##   (Since this small code is close to be mathematically trivial.)
##
## Author:
##
##   JRF
##   http://jrf.cocolog-nifty.com/society/
##   (The page is written in Japanese.)
##

import random
import numpy as np
import matplotlib.pyplot as plt
import argparse

def parse_args ():
    global ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", default=20, dest="trials", type=int)

    parser.add_argument("--population", default=1000, dest="population", type=int)
    parser.add_argument("--land-unit", default=10.0, dest="land_unit", type=float)
    parser.add_argument("--initial-land-mean", default=20.0, dest="initial_land_mean", type=float)
    parser.add_argument("--initial-intellprop-mean", default=20.0, dest="initial_intellprop_mean", type=float)
    parser.add_argument("--initial-liability-sigma", default=20.0, dest="initial_liability_sigma", type=float)
    parser.add_argument("--max-working", default=900, dest="max_working", type=int)
    parser.add_argument("--min-working", default=600, dest="min_working", type=int)

    parser.add_argument("--transactions-of-land", default=300, dest="transactions_of_land", type=int)
    parser.add_argument("--transactions-of-intellprop", default=300, dest="transactions_of_intellprop", type=int)
    parser.add_argument("--repayment-rate", default=0.5, dest="repayment_rate", type=float)


    parser.add_argument("--coeff-of-intellprop-buyer", default=0.3, dest="coeff_of_intellprop_buyer", type=float)
    parser.add_argument("--coeff-of-intellprop-seller", default=0.3, dest="coeff_of_intellprop_seller", type=float)
    parser.add_argument("--coeff-of-land-buyer", default=0.8, dest="coeff_of_land_buyer", type=float)
    parser.add_argument("--coeff-of-land-seller", default=0.8, dest="coeff_of_land_seller", type=float)

    parser.add_argument("--devaluation-of-intellprop", default=False, action='store_true')
    parser.add_argument("--devaluation-of-liability", default=False, action='store_true')
    parser.add_argument("--intellprop-transform", default="sqrt", dest="intellprop_transform", choices=["log", "sqrt"])

    parser.add_argument("--needs-of-necessaries", default=2.0, dest="needs_of_necessaries", type=float)
    parser.add_argument("--price-of-wages", default=30.0, dest="price_of_wages", type=float)
    parser.add_argument("--price-of-necessaries", default=10.0, dest="price_of_necessaries", type=float)
    parser.add_argument("--price-of-luxuries", default=15.0, dest="price_of_luxuries", type=float)

    parser.add_argument("--bins", default=20, dest="bins", type=int)
    parser.add_argument("--pause", default=1.0, dest="pause", type=float)
    parser.add_argument("--first-pause", default=None, dest="first_pause", type=float)

    ARGS = parser.parse_args()

    if ARGS.first_pause is None:
        ARGS.first_pause = ARGS.pause

class Player:
    def __init__ (self):
        self.working = False
        self.savings = 0.0
        self.liability = 0.0
        self.land = 0.0
        self.intellprop = 0.0

class Price:
    def __init__ (self):
        self.wages = 0.0
        self.necessaries = 0.0
        self.luxuries = 0.0

class Economy:
    def __init__ (self):
        self.debug = False
        self.social_debt = 0
        self.players = []
        self.needs_of_necessaries = ARGS.needs_of_necessaries
        self.price = Price()
        self.price.wages = ARGS.price_of_wages
        self.price.necessaries = ARGS.price_of_necessaries
        self.price.luxuries = ARGS.price_of_luxuries

    def step (self):
        numWorking = random.randint(ARGS.min_working, ARGS.max_working)
        curPrice = self.price
        curD = self.needs_of_necessaries
        curS = curPrice.wages - curPrice.necessaries * curD
        for i, x in enumerate(self.players):
            if i < numWorking:
                x.working = True
            else:
                x.working = False

        totalIntellprop = 0
        totalLand = 0
        totalSavings = 0
        totalLiability = 0
        for x in self.players:
            totalIntellprop += x.intellprop
            totalLand += x.land
            totalSavings += x.savings
            totalLiability += x.liability
        prevTotalIntellprop = totalIntellprop
        prevTotalLand = totalLand
        prevTotalSavings = totalSavings
        prevTotalLiability = totalLiability

        a = ARGS.coeff_of_land_buyer / ARGS.population
        b = 1
        l = sorted(random.sample(self.players, ARGS.population),
                   key=lambda x: x.liability, reverse=True)
        l = [(random.uniform(0.0, a * i + b), x)  for i, x in enumerate(l)]
        l = sorted(l, key=lambda x: x[0], reverse=True)
        landBuyer = list(map(lambda x: x[1], l[0:ARGS.transactions_of_land]))

        a = ARGS.coeff_of_land_seller / ARGS.population
        b = 1
        l = sorted(random.sample(self.players, ARGS.population),
                   key=lambda x: x.liability, reverse=False)
        l = [(random.uniform(0.0, a * i + b), x)  for i, x in enumerate(l)]
        l = sorted(l, key=lambda x: x[0], reverse=True)
        landSeller = list(map(lambda x: x[1], l[0:ARGS.transactions_of_land]))
        landSeller = random.sample(landSeller, len(landSeller))

        a = ARGS.coeff_of_intellprop_buyer / ARGS.population
        b = 1
        l = sorted(random.sample(self.players, ARGS.population),
                   key=lambda x: x.liability, reverse=True)
        l = [(random.uniform(0.0, a * i + b), x)  for i, x in enumerate(l)]
        l = sorted(l, key=lambda x: x[0], reverse=True)
        ipBuyer = list(map(lambda x: x[1],
                           l[0:ARGS.transactions_of_intellprop]))

        a = ARGS.coeff_of_intellprop_seller / ARGS.population
        b = 1
        l = sorted(random.sample(self.players, ARGS.population),
                   key=lambda x: x.liability, reverse=False)
        l = [(random.uniform(0.0, a * i + b), x)  for i, x in enumerate(l)]
        l = sorted(l, key=lambda x: x[0], reverse=True)
        ipSeller = list(map(lambda x: x[1],
                            l[0:ARGS.transactions_of_intellprop]))
        ipSeller = random.sample(ipSeller, len(ipSeller))
        
        for i in range(ARGS.transactions_of_land):
            buyer = landBuyer[i]
            seller = landSeller[i]
            if seller.land >= ARGS.land_unit:
                buyer.land += ARGS.land_unit
                seller.land -= ARGS.land_unit
                buyer.liability += ARGS.land_unit
                seller.liability -= ARGS.land_unit

        for i in range(ARGS.transactions_of_intellprop):
            buyer = ipBuyer[i]
            seller = ipSeller[i]
            a = ARGS.land_unit / np.log(1 + ARGS.land_unit)
            price = random.uniform(0, seller.intellprop 
                                   + a * np.log(1 + seller.land))
            if ARGS.intellprop_transform == 'log':
                a = price / (2 * np.log(1 + price))
                y = a * np.log(1 + buyer.intellprop) + price
            else:
                a = 0.25 * price
                y = np.sqrt(a * buyer.intellprop) + price
            valuation = random.uniform(price, y)
            buyer.intellprop += valuation
            buyer.liability += price
            seller.liability -= price

        totalRepay = 0.0
        totalErosion = 0.0
        curDemandOfLuxuries = 0
        base = curS * 3.0
        for x in self.players:
            curRepay = 0
            if x.working and x.liability > 0:
                curRepay = curS * ARGS.repayment_rate
                if curRepay >= x.liability:
                    curRepay = x.liability
                totalRepay += curRepay
                x.liability -= curRepay

            curCash = x.savings
            if x.liability < 0:
                curCash = - x.liability + x.savings

            trueWages = curPrice.wages

            if x.working:
                if curCash + curS - curRepay >= base \
                        and ((curCash + curS - curRepay - base) / 3) + base \
                        >= curPrice.luxuries:
                    curDemandOfLuxuries += 1
                    x.savings += trueWages - curPrice.necessaries * curD \
                        - curPrice.luxuries - curRepay
                else:
                    x.savings += trueWages - curPrice.necessaries * curD \
                        - curRepay
            else:
                self.social_debt += curPrice.necessaries * curD ## 失業手当
                if (curCash >= base
                    and ((curCash - base) / 3) + base >= curPrice.luxuries):
                    curDemandOfLuxuries += 1
                    x.savings -= curPrice.luxuries

            if x.savings < 0:
                x.liability += - x.savings
                totalErosion += - x.savings
                x.savings = 0

        totalIntellprop = 0
        totalLand = 0
        totalSavings = 0
        totalLiability = 0
        for x in self.players:
            totalIntellprop += x.intellprop
            totalLand += x.land
            totalSavings += x.savings
            totalLiability += x.liability

        minLiability = np.argmin(list(map(lambda x: x.liability, self.players)))
        maxLiability = np.argmax(list(map(lambda x: x.liability, self.players)))
        maxIntellprop = np.argmax(list(map(lambda x: x.intellprop,
                                           self.players)))

        ## レポート
        print("Increase of Intellprop:Savings:Liability : {}:{}:{}"
              .format(totalIntellprop - prevTotalIntellprop,
                      totalSavings - prevTotalSavings,
                      totalLiability - prevTotalLiability))
        print("Total Intellprop:Land:Savings:Liability : {}:{}:{}:{}"
              .format(totalIntellprop, totalLand, totalSavings,
                      totalLiability))
        print("Working: {}".format(numWorking))
        print("Demand of Luxuries: {}".format(curDemandOfLuxuries))
        print("Total Erosion:Repay : {}:{}"
              .format(totalErosion, totalRepay))
        print("MinLiability == MaxIntellprop ? : {}"
              .format(minLiability == maxIntellprop))
        print("MaxLiability == MaxIntellprop ? : {}"
              .format(maxLiability == maxIntellprop))
        print("", flush=True)


        ## 切り下げ
        if ARGS.devaluation_of_intellprop:
            r = prevTotalIntellprop / totalIntellprop
            for x in self.players:
                x.intellprop *= r
        
        if ARGS.devaluation_of_liability:
            y = totalErosion - totalRepay
            if y > 0:
                l = 0.0
                for x in self.players:
                    if x.liability > 0:
                        l += x.liability
                if l > 0:
                    r = (l - y) / l
                    if r < 0:
                        for x in self.players:
                            x.liability = 0.0
                    else:
                        for x in self.players:
                            if x.liability > 0:
                                x.liability *= r
            else:
                l = 0.0
                for x in self.players:
                    if x.liability < 0:
                        l += - x.liability
                if l > 0:
                    r = (l + y) / l
                    if r < 0:
                        for x in self.players:
                            x.liability = 0.0
                    else:
                        for x in self.players:
                            if x.liability < 0:
                                x.liability *= r

        ## 労働者と失業者をランダムにソート
        working = []
        notWorking = []
        for x in random.sample(self.players, len(self.players)):
            if x.working:
                working.append(x)
            else:
                notWorking.append(x)
        self.players = working + notWorking


    def initialize_0 (self):
        numPlayers = ARGS.population
        numWorking = random.randint(ARGS.min_working, ARGS.max_working)

        p = self.price
        s = p.wages - p.necessaries * self.needs_of_necessaries

        ## 労働者を1000人創り、貯蓄・土地・知財を決定。
        self.players = []
        liabilityPlus = 0.0
        liabilityMinus = 0.0
        for i in range(numPlayers):
            x = Player()
            self.players.append(x)
            if i < numWorking:
                x.working = True
            else:
                x.worknig = False
            x.savings = random.expovariate(1.0/s)
            l = random.expovariate(1.0 / (ARGS.initial_land_mean \
                                              / ARGS.land_unit))
            x.land = np.round(l) * ARGS.land_unit
            x.intellprop = random.expovariate(1.0 /
                                              ARGS.initial_intellprop_mean)
            x.liability = random.normalvariate(0.0,
                                               ARGS.initial_liability_sigma)
            if x.liability > 0:
                liabilityPlus += x.liability
            else:
                liabilityMinus += - x.liability

        r = liabilityMinus / liabilityPlus
        for x in self.players:
            if x.liability > 0:
                x.liability *= r


class EconomyPlot:
    def __init__ (self):
	#plt.style.use('bmh')
        fig = plt.figure(figsize=(6, 4))
        #plt.tight_layout()
        self.ax1 = fig.add_subplot(2, 2, 1)
        self.ax2 = fig.add_subplot(2, 2, 2)
        self.ax3 = fig.add_subplot(2, 2, 3)
        self.ax4 = fig.add_subplot(2, 2, 4)

    def plot (self, economy, term):
        ax = self.ax1
        ax.clear()
        ax.set_title('Term: %i: Land' % term)
        ax.hist(list(map(lambda x: x.land, economy.players)), bins=ARGS.bins)

        ax = self.ax2
        ax.clear()
        ax.set_title('Intellprop')
        ax.hist(list(map(lambda x: x.intellprop, economy.players)),
                bins=ARGS.bins)

        ax = self.ax3
        ax.clear()
        ax.set_xlabel('Savings')
        ax.hist(list(map(lambda x: x.savings, economy.players)),
                bins=ARGS.bins)
        
        ax = self.ax4
        ax.clear()
        ax.set_xlabel('Liability')
        ax.hist(list(map(lambda x: x.liability, economy.players)),
                bins=ARGS.bins)


if __name__ == '__main__':
    parse_args()
    economy = Economy()
    economy.initialize_0()
    eplot = EconomyPlot()
    eplot.plot(economy, 0)
    plt.pause(ARGS.first_pause)
    for i in range(ARGS.trials):
        print("Term: %i" % (i + 1))
        economy.step()
        eplot.plot(economy, i + 1)
        plt.pause(ARGS.pause)
    plt.show()
