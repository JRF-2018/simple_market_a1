#!/usr/bin/python3
__version__ = '0.0.3' # Time-stamp: <2020-02-23T13:41:26Z>
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
    parser.add_argument("--trials", default=50, dest="trials", type=int)

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


    parser.add_argument("--coeff-of-intellprop-buyer", default=0.8, dest="coeff_of_intellprop_buyer", type=float)
    parser.add_argument("--coeff-of-intellprop-seller", default=0.8, dest="coeff_of_intellprop_seller", type=float)
    parser.add_argument("--coeff-of-land-buyer", default=0.3, dest="coeff_of_land_buyer", type=float)
    parser.add_argument("--coeff-of-land-seller", default=0.8, dest="coeff_of_land_seller", type=float)
    parser.add_argument("--sort-of-intellprop-buyer", default="liability", dest="sort_of_intellprop_buyer", choices=["ascend", "descend", "liability", "cash", "poor", "rich", "hybrid"])
    parser.add_argument("--sort-of-intellprop-seller", default="ascend", dest="sort_of_intellprop_seller", choices=["ascend", "descend", "liability", "cash"])
    parser.add_argument("--sort-of-land-buyer", default="cash", dest="sort_of_land_buyer", choices=["land", "cash", "poor", "rich", "liability"])
    parser.add_argument("--sort-of-land-seller", default="land", dest="sort_of_land_seller", choices=["land", "liability", "cash"])
    parser.add_argument("--asset-rank", default="net", dest="asset_rank", choices=["intellprop", "gross", "net", "land", "cash", "liability"])
    parser.add_argument("--cash-on-hand", default="loose", dest="cash_on_hand", choices=["rigid", "loose"])

    parser.add_argument("--devaluation-of-intellprop", default=False, action='store_true')
    parser.add_argument("--devaluation-of-liability", default=False, action='store_true')
    parser.add_argument("--intellprop-transform", default="sqrt", dest="intellprop_transform", choices=["log", "sqrt"])

    parser.add_argument("--needs-of-necessaries", default=2.0, dest="needs_of_necessaries", type=float)
    parser.add_argument("--price-of-wages", default=30.0, dest="price_of_wages", type=float)
    parser.add_argument("--price-of-necessaries", default=10.0, dest="price_of_necessaries", type=float)
    parser.add_argument("--price-of-luxuries", default=15.0, dest="price_of_luxuries", type=float)

    parser.add_argument("--intellprop-mag", default=1.0, dest="intellprop_mag", type=float)
    parser.add_argument("--intellprop-land-mag", default=1.0, dest="intellprop_land_mag", type=float)
    parser.add_argument("--cash-margin", default=0.0, dest="cash_margin", type=float)
    parser.add_argument("--add-cash-margin-30", default=0.0, dest="add_cash_margin_30", type=float)
    parser.add_argument("--add-repayment-rate-30", default=0.0, dest="add_repayment_rate_30", type=float)
    parser.add_argument("--add-price-of-wages-30", default=0.0, dest="add_price_of_wages_30", type=float)
    parser.add_argument("--add-price-of-luxuries-30", default=0.0, dest="add_price_of_luxuries_30", type=float)
    

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

        self.cur_sell = 0

        ## レポート用の変数
        self.num = None
        self.max = None
        self.min = None
        self.luxuries = 0
    
    def net_asset (self):
        return self.savings + self.land + self.intellprop - self.liability

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
            x.cur_sell = 0
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

        totalIntellpropTransaction = 0
        totalLandTransaction = 0

        ipSellerA = ARGS.land_unit / np.log(1 + ARGS.land_unit)
        ipSellerF = lambda seller: seller.intellprop \
            + ARGS.intellprop_land_mag \
            * ipSellerA * np.log(1 + seller.land)

        a = ARGS.coeff_of_land_buyer / ARGS.population
        b = 1
        key = {
            'cash': lambda x: - x.liability,
            'liability': lambda x: x.liability,
            'poor': lambda x: - x.net_asset(),
            'rich': lambda x: x.net_asset(),
            'land': lambda x: - x.land,
            }[ARGS.sort_of_land_buyer]
        l = sorted(random.sample(self.players, ARGS.population),
                   key=key, reverse=False)
        l = [(random.uniform(0.0, a * i + b), x)  for i, x in enumerate(l)]
        l = sorted(l, key=lambda x: x[0], reverse=True)
        landBuyer = list(map(lambda x: x[1], l[0:ARGS.transactions_of_land]))

        a = ARGS.coeff_of_land_seller / ARGS.population
        b = 1
        key = {
            'cash': lambda x: - x.liability,
            'liability': lambda x: x.liability,
            'land': lambda x: x.land,
            }[ARGS.sort_of_land_seller]
        l = sorted(random.sample(self.players, ARGS.population),
                   key=key, reverse=False)
        l = [(random.uniform(0.0, a * i + b), x)  for i, x in enumerate(l)]
        l = sorted(l, key=lambda x: x[0], reverse=True)
        landSeller = list(map(lambda x: x[1], l[0:ARGS.transactions_of_land]))
        landSeller = random.sample(landSeller, len(landSeller))

        a = ARGS.coeff_of_intellprop_buyer / ARGS.population
        b = 1
        key = {
            'cash': lambda x: - x.liability,
            'liability': lambda x: x.liability,
            'rich': lambda x: x.net_asset(),
            'poor': lambda x: - x.net_asset(),
            'hybrid': lambda x: (x.liability - x.savings
                                 if x.liability - x.savings > 0 else 0) \
                + x.intellprop,
            'descend': lambda x: - ipSellerF(x),
            'ascend': ipSellerF,
            }[ARGS.sort_of_intellprop_buyer]
        l = sorted(random.sample(self.players, ARGS.population),
                   key=key, reverse=False)
        l = [(random.uniform(0.0, a * i + b), x)  for i, x in enumerate(l)]
        l = sorted(l, key=lambda x: x[0], reverse=True)
        ipBuyer = list(map(lambda x: x[1],
                           l[0:ARGS.transactions_of_intellprop]))

        a = ARGS.coeff_of_intellprop_seller / ARGS.population
        b = 1
        key = {
            'cash': lambda x: - x.liability,
            'liability': lambda x: x.liability,
            'descend': lambda x: - ipSellerF(x),
            'ascend': ipSellerF,
            }[ARGS.sort_of_intellprop_seller]
        l = sorted(random.sample(self.players, ARGS.population),
                   key=key, reverse=False)
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
                if ARGS.cash_on_hand == "rigid":
                    seller.liability -= ARGS.land_unit
                else:
                    seller.cur_sell += ARGS.land_unit
                totalLandTransaction += ARGS.land_unit

        for i in range(ARGS.transactions_of_intellprop):
            buyer = ipBuyer[i]
            seller = ipSeller[i]
            price = random.uniform(0, ipSellerF(seller)) \
                * ARGS.intellprop_mag
            if ARGS.intellprop_transform == 'log':
                a = price / (2 * np.log(1 + price))
                y = a * np.log(1 + buyer.intellprop) + price
            else:
                a = 0.25 * price
                y = np.sqrt(a * buyer.intellprop) + price
            valuation = random.uniform(price, y)
            buyer.intellprop += valuation
            buyer.liability += price
            if ARGS.cash_on_hand == "rigid":
                seller.liability -= price
            else:
                seller.cur_sell += price
            totalIntellpropTransaction += price

        totalRepay = 0.0
        totalErosion = 0.0
        curDemandOfLuxuries = 0
        base = curS * 3.0
        boughtByRepayer = 0
        numErosion = 0
        numErosionBoughtByRepayer = 0
        for x in self.players:
            curRepay = 0
            if x.working and x.liability > 0:
                curRepay = curS * ARGS.repayment_rate
                if curRepay >= x.liability:
                    curRepay = x.liability
                totalRepay += curRepay
                x.liability -= curRepay

            curCash = x.savings + x.cur_sell
            if - x.liability + ARGS.cash_margin > 0:
                curCash += - x.liability + ARGS.cash_margin

            trueWages = curPrice.wages

            if x.working:
                if curCash + curS - curRepay >= base \
                        and ((curCash + curS - curRepay - base) / 3) + base \
                        >= curPrice.luxuries:
                    curDemandOfLuxuries += 1
                    x.luxuries +=1
                    x.savings += trueWages - curPrice.necessaries * curD \
                        - curPrice.luxuries - curRepay
                    if curRepay > 0:
                        boughtByRepayer += 1
                else:
                    x.savings += trueWages - curPrice.necessaries * curD \
                        - curRepay
            else:
                self.social_debt += curPrice.necessaries * curD ## 失業手当
#                x.liability += curPrice.necessaries * curD
                if (curCash >= base
                    and ((curCash - base) / 3) + base >= curPrice.luxuries):
                    curDemandOfLuxuries += 1
                    x.luxuries +=1
                    x.savings -= curPrice.luxuries

            if x.savings < 0:
                x.liability += - x.savings
                totalErosion += - x.savings
                x.savings = 0
                numErosion += 1
                if curRepay > 0:
                    numErosionBoughtByRepayer += 1
            x.liability -= x.cur_sell

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
        maxLand = np.argmax(list(map(lambda x: x.land, self.players)))

        key = {
            'intellprop': lambda x: x.intellprop,
            'land': lambda x: x.land,
            'liability': lambda x: x.liability,
            'cash': lambda x: - x.liability,
            'gross': lambda x: x.land + x.intellprop,
            'net': lambda x: x.net_asset(),
            }[ARGS.asset_rank]
        l = sorted(self.players, key=key)
        for i, x in enumerate(l):
            if x.min is None or i < x.min:
                x.min = i
            if x.max is None or x.max < i:
                x.max = i
        upMean = np.mean(list(map(lambda x: x.max - x.min, self.players)))
        maxAsset = l[len(self.players) - 1]

        num = self.players[maxLand].num
        landSellerMax = False
        for x in landSeller:
            if x.num == num:
                landSellerMax = True
        landBuyerMax = False
        for x in landBuyer:
            if x.num == num:
                landBuyerMax = True

        meanLuxuries = np.mean(list(map(lambda x: x.luxuries, self.players)))
        minLuxuries = np.min(list(map(lambda x: x.luxuries, self.players)))

        numLiabilityPlus = sum(list(map(lambda x: int(x.liability >= 0),
                                        self.players)))

        ## レポート
        print("Increase of Intellprop:Savings:Liability : {}:{}:{}"
              .format(totalIntellprop - prevTotalIntellprop,
                      totalSavings - prevTotalSavings,
                      totalLiability - prevTotalLiability))
        print("Total Intellprop:Land:Savings:Liability : {}:{}:{}:{}"
              .format(totalIntellprop, totalLand, totalSavings,
                      totalLiability))
        print("Gross Transactions of Intellprop:Land : {}:{}"
              .format(totalIntellpropTransaction, totalLandTransaction))
        print("Working: {}".format(numWorking))
        print("Total Erosion:Repay : {}:{}"
              .format(totalErosion, totalRepay))
        print("Demand of Luxuries: {}".format(curDemandOfLuxuries))
        print("Luxuries Bought By Repayer:Number of Erosion:Other : {}:{}:{}"
              .format(boughtByRepayer, numErosion,
                      curDemandOfLuxuries - boughtByRepayer - numErosion \
                          + numErosionBoughtByRepayer))
        print("Number of Liability Minus:Plus : {}:{}"
              .format(len(self.players) - numLiabilityPlus, numLiabilityPlus))
        f = lambda x: self.players[x].num
        print("MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : {}:{}:{}:{}:{}"
              .format(f(minLiability), f(maxLiability), f(maxIntellprop),
                      f(maxLand), maxAsset.num))
        print("Value of MinLiability:MaxLiability : {}:{}"
              .format(self.players[minLiability].liability,
                      self.players[maxLiability].liability))
        f = lambda x: self.players[x].luxuries
        print("Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : {}:{}:{}:{}:{}"
              .format(f(minLiability), f(maxLiability), f(maxIntellprop),
                      f(maxLand), maxAsset.luxuries))
        print("Luxuries Mean:Min : {}:{}"
              .format(meanLuxuries, minLuxuries))
        print("MaxLand Sell:MaxLand Buy ? : {}:{}"
              .format(landSellerMax, landBuyerMax))
        print("Rank Change Mean: {}"
              .format(upMean))
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
            x.num = i
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
        if i + 1 == 30:
            ARGS.cash_margin += ARGS.add_cash_margin_30
            ARGS.repayment_rate += ARGS.add_repayment_rate_30
            economy.price.wages += ARGS.add_price_of_wages_30
            economy.price.luxuries += ARGS.add_price_of_luxuries_30
        elif i + 1 == 40:
            ARGS.cash_margin -= ARGS.add_cash_margin_30
            ARGS.repayment_rate -= ARGS.add_repayment_rate_30
            economy.price.wages -= ARGS.add_price_of_wages_30
            economy.price.luxuries -= ARGS.add_price_of_luxuries_30
        economy.step()
        eplot.plot(economy, i + 1)
        plt.pause(ARGS.pause)
    plt.show()
