class ECS:

    def __init__(self, transmitters, neurons, iterations, n):
        self.name = 'ECS '
        self.number = n
        self.con = []
        self.dx = []
        self.external_t = []
        self.t_zero_list = []
        for j in range(len(transmitters)):
            self.con.append([0])
            self.dx.append(0)
            self.external_t.append([0, [0, iterations]])
            self.t_zero_list.append(0)
        self.timestamps = []
        self.lifetimes = []
        for i in range(len(neurons)):
            self.timestamps.append([])
            self.lifetimes.append([])
            for j in range(len(transmitters)):
                self.timestamps[i].append(-1)
                self.lifetimes[i].append(9999)

    def calc_lifetimes(self, neurons, transmitters, time):

        self.lifetimes = []
        self.dx = []
        for i in range(len(neurons)):
            self.lifetimes.append([])
            for j in range(len(transmitters)):
                self.lifetimes[i].append(9999)
        for j in range(len(transmitters)):
            self.dx.append(0)
        for i in range(len(neurons)):
            if neurons[i].transmitter_dose[self.number] != self.t_zero_list:
                for j in range(len(transmitters)):
                    if self.timestamps[i][j] == time[len(time) - 1]:
                        self.timestamps[i][j] = -1
                        self.lifetimes[i][j] = 0
                    elif time[len(time) - 1] < self.timestamps[i][j]:
                        self.lifetimes[i][j] = self.timestamps[i][j] - time[len(time) - 1]
                        self.dx[j] += neurons[i].transmitter_dose[self.number][j]
                    else:
                        self.timestamps[i][j] = -1
            else:
                continue

    def calc_con(self, neurons, time, transmitters):

        for j in range(len(transmitters)):
            self.con[j].append(0)
        for i in range(len(neurons)):
            if neurons[i].transmitter_dose[self.number] != self.t_zero_list:
                for j in range(len(transmitters)):
                    if neurons[i].activations[-2] == 1 and neurons[i].activations[-1] == 0:
                        self.timestamps[i][j] = time[len(time) - 1] + transmitters[j][1]
                    if self.timestamps[i][j] == -1:
                        trans_life_mark = 0
                    else:
                        trans_life_mark = 1

                    self.con[j][- 1] += (neurons[i].activations[- 1] + trans_life_mark)* neurons[i].transmitter_dose[self.number][j]

            else:
                continue
