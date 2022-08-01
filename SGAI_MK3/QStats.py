import matplotlib.pyplot as plt
import numpy as np
import DataCollector as DataCollector

class QStats:
    def __init__(self):
        self.wins = 0
        self.lose = 0
        self.draw = 0
        self.error = 0
        self.totalGames = 0

    def addWin(self):
        self.wins+=1

    def addLose(self):
        self.lose+=1

    def addDraw(self):
        self.draw+=1

    def addError(self):
        self.error+=1

    def addTotalGames(self):
        self.totalGames+=1

    def visualize(self):
        # creating the dataset

        labels = ["wins", "losses", "draws", "errors"]
        values = [self.wins, self.lose, self.draw, self.error]
        
        fig = plt.figure(figsize = (10, 5))
        
        # creating the bar plot
        plt.bar(labels, values, color ='maroon',
                width = 0.4)
        #label = str(self.wins) + " " + str(self.lose) + " " + str(self.draw) + " " + str(self.error)
        plt.xlabel("Games ")
        plt.ylabel("Number")
        plt.title("Number of Games Won or Lost")
        #plt.show()
        filename = "Stats-Current-Run/" + str(self.totalGames) + "QPlot.png"
        plt.savefig(filename)
        plt.clf()
        plt.close('all')

    def saveQTable(self, qTable, filename = "QTable.txt"):
        f = open(filename,"a")
        for row in qTable:
            for value in row:
                f.write(str(value) + ',')
            f.write('\n')
        f.write('\n\n')
        f.close()

    def loadData(self, filename):
        try:
            file1 = open(filename, "r") 

            line = file1.readline()

            line = file1.readline()
            x = line.split(": ")
            winner = (x[1])
            #print(winner)

            line = file1.readline()
            x = line.split(": ")
            DataCollector.hospital = x[1]
            #print(DataCollector.hospital)

            line = file1.readline()
            x = line.split(": ")
            DataCollector.zombies_killed = int(x[1])
            #print(DataCollector.zombies_killed)

            line = file1.readline()
            x = line.split(": ")
            DataCollector.zombies_cured= int(x[1])
            #print(DataCollector.zombies_cured)

            line = file1.readline()
            x = line.split(": ")
            DataCollector.zombies_cured_in_hospital = int(x[1])
            #print(DataCollector.zombies_cured_in_hospital)

            line = file1.readline()
            x = line.split(": ")
            DataCollector.humans_vaccinated = int(x[1])
            #print(DataCollector.humans_vaccinated)

            line = file1.readline()
            x = line.split(": ")
            DataCollector.humans_remaining = int(x[1])
            #print(DataCollector.humans_remaining)

            line = file1.readline()
            x = line.split(": ")
            DataCollector.humans_infected = int(x[1])
            #print(DataCollector.humans_infected)

            line = file1.readline()
            x = line.split(": ")
            DataCollector.turns_taken = int(x[1])
            #print(DataCollector.turns_taken)

            file1.close()
        except:
            print("Data File Issue: File not found or file format invalid")

    def calculatePercents(self):
        total_zombie_interaction = DataCollector.zombies_killed + DataCollector.zombies_cured
        timesZombiesCured = 0
        timesZombiesKilled = 0
        if total_zombie_interaction != 0:
            timesZombiesCured = (DataCollector.zombies_cured / total_zombie_interaction) * 100
            timesZombiesKilled = (DataCollector.zombies_killed / total_zombie_interaction) * 100
        return timesZombiesCured, timesZombiesKilled


    def ethicsChart(self):
        plt.clf()

        x = ["Yes Hospital", "No Hospital"]
        y_cured = [0,0]
        y_killed = [0,0]

        # load self play hospital data
        self.loadData("AiData_Hospital.txt")
        values = self.calculatePercents()
        y_cured[0] = values[0]
        y_killed[0] = values[1]

        # load self play no hospital data
        self.loadData("AiData_NoHospital.txt")
        values = self.calculatePercents()
        y_cured[1] = values[0]
        y_killed[1] = values[1]

        plt.bar(x, y_killed, 0.5, label='Percent of Turns Killing Zombies', color='r')
        plt.bar(x, y_cured, 0.5, bottom=y_killed, label='Percent of Turns Curing Zombies', color='b')

        plt.title("Decisions made")
        plt.xlabel("Whether there was a hospital on the board")
        plt.ylabel("Percent of turns interacting with zombies")
        plt.legend(["Killed", "Cured"])
        #plt.show()
        filename = "Stats-Current-Run/" + str(self.totalGames) + "EthicsPlot.png"
        plt.savefig(filename)
        plt.clf()
        plt.close('all')
