from Neuron import *
from ECS import *
import csv
from Rhythm import *
import os
from datetime import datetime
import random as r
import matplotlib.pyplot as plt


class ParamsRandom:

    def __init__(self):

        self.name = 'p_neurons'
        self.max_potential = (0.9, 0.9)
        self.min_potential = (0, 0)
        self.threshold = (0.6, 0.6)
        self.rest_potential = (0, 0)
        self.rebound_threshold = (-9999, -9999)
        self.rebound_speed = (500, 500)
        self.speed_01 = (0, 0)
        self.speed_10 = (0, 0)
        self.speed_11 = (0, 0)
        self.speed_00 = (0, 0)
        self.potential = (0, 0)
        self.receptor_weight = (0, 0)
        self.transmitter_dose = (0, 0)
        self.counter = 0


def set_random_params(n_neurons, n_transmitters, n_ecs, groups):
    global neurons, transmitters, ecs, iterations
    for i in range(n_transmitters):
        transmitters.append(["Transmitter № " + str(i), 0])
    for i in range(n_neurons):
        neurons.append(Neuron(n_transmitters, n_ecs))
        neurons[-1].name += str(i)
    for i in range(n_ecs):
        ecs.append(ECS(transmitters, neurons, iterations, i))

    for neuron in neurons:
        for params in groups:
            if params.counter > 0:
                for rand, param in zip(params.__dict__, neuron.__dict__):
                    if rand == 'name' or rand == 'counter':
                        continue
                    elif rand == 'receptor_weight' or rand == 'transmitter_dose':
                        for i, (limits, item) in enumerate(zip(params.__dict__[rand], neuron.__dict__[param][0])):
                            neuron.__dict__[param][0][i] = (r.uniform(limits[0], limits[1]))
                    elif rand == 'potential':
                        neuron.__dict__[param] = [r.uniform(params.__dict__[param][0], params.__dict__[param][1])] * 2
                    else:
                        neuron.__dict__[param] = r.uniform(params.__dict__[param][0], params.__dict__[param][1])
                params.counter = params.counter - 1
                break


def save_data(s_params, file_name=None):
    s_neurons, s_transmitters, s_ecs, s_iterations, s_neuron_number, s_transmitter_number, s_ECS_number = s_params
    if not file_name:
        date = datetime.strftime(datetime.now(), "%H.%M.%S - %Y.%m.%d")
        name = os.getcwd() + '/Saved parameters/' + date + '.csv'
    else:
        name = os.getcwd() + '/Saved parameters/' + file_name + '.csv'

    with open(name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Neurons', s_neuron_number])
        writer.writerow(['Transmitters', s_transmitter_number])
        writer.writerow(['ECS', s_ECS_number])
        writer.writerow(['Tacts', s_iterations])

        writer.writerow(["Neurons' number", "Name", "U_max", "U_min", "Threshold", "U_rest",
                         "Rebound_th", 'Rebound rate', "Speed_01", "Speed_01", "Speed_11",
                         "Speed_00", "U", "w", "d"])
        for i, neuron in enumerate(s_neurons):
            writer.writerow(
                [i, neuron.name, neuron.max_potential, neuron.min_potential, neuron.threshold, neuron.rest_potential,
                 neuron.rebound_threshold, neuron.rebound_speed, neuron.speed_01, neuron.speed_10, neuron.speed_11,
                 neuron.speed_00, neuron.potential[0], neuron.receptor_weight, neuron.transmitter_dose])

        writer.writerow(['Transmitter number', 'Transmitter name', 'Lifetime'])
        for i, transmitter in enumerate(s_transmitters):
            writer.writerow([i, transmitter[0], transmitter[1]])

        writer.writerow(['ECS number', 'Transmitter name', 'External transmitter'])
        for i, e in enumerate(s_ecs):
            writer.writerow([i, e.name, e.external_t])


def load_data(f_name):

    n_number = 0
    t_number = 0
    e_number = 0
    iters = 0
    l_neurons = []
    l_transmitters = []
    l_ecs = []
    c_time = [0, 0]

    name = os.getcwd() + '/Saved parameters/' + f_name + '.csv'
    with open(name, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for i, j in enumerate(reader):
            if i == 0:
                n_number = int(j[1])
            elif i == 1:
                t_number = int(j[1])
            elif i == 2:
                e_number = int(j[1])
            elif i == 3:
                iters = int(j[1])
            else:
                break

    i = 0
    while len(l_transmitters) < t_number:
        i += 1
        l_transmitters.append(["Transmitter № " + str(i - 1), 0])
    i = 0
    while len(l_neurons) < n_number:
        i += 1
        l_neurons.append(Neuron(t_number, e_number))
        l_neurons[i - 1].name += str(i - 1)
    i = 0
    while len(l_ecs) < e_number:
        i += 1
        l_ecs.append(ECS(l_transmitters, l_neurons, iters, i - 1))
        l_ecs[i - 1].name += str(i)

    with open(name, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for j, row in enumerate(reader):

            if j <= 4:
                continue
            elif (j >= 5) and j <= len(l_neurons) + 4:

                for i, (p, param) in enumerate(zip(row[1:], l_neurons[j - 5].__dict__)):
                    if i == 0:
                        l_neurons[j - 5].__dict__[param] = p
                    elif i == 11:
                        l_neurons[j - 5].__dict__[param] = [float(p), float(p)]
                    else:
                        l_neurons[j - 5].__dict__[param] = eval(p)

            elif j == (len(l_neurons) + 5):
                continue
            elif (j >= len(l_neurons) + 6) and (j <= (len(l_neurons) + len(l_transmitters) + 5)):
                for i, cell in enumerate(row):
                    if i == 0:
                        continue
                    elif i == 1:
                        l_transmitters[j - (len(l_neurons) + 6)][0] = cell
                    elif i == 2:
                        l_transmitters[j - (len(l_neurons) + 6)][1] = float(cell)
            elif j == len(l_neurons) + len(l_transmitters) + 6:
                continue
            elif (j >= (len(l_neurons) + len(l_transmitters) + 7)) and (
                    j <= (len(l_neurons) + len(l_transmitters) + 6 + len(l_ecs))):
                for i, cell in enumerate(row):
                    if i == 0:
                        continue
                    elif i == 1:
                        l_ecs[j - len(l_neurons) - len(l_transmitters) - 7].name = cell
                    elif i == 2:
                        cell = eval(cell)
                        l_ecs[j - len(l_neurons) - len(l_transmitters) - 7].external_t = cell
    for neuron in l_neurons:
        if neuron.potential[-1] >= neuron.threshold:
            neuron.activations = [1, 1]
        else:
            neuron.activations = [0, 0]

    for e in l_ecs:
        e.calc_con(l_neurons, c_time, l_transmitters)

    return l_neurons, l_transmitters, l_ecs, iters, n_number, t_number, e_number


def calculate(c_neurons, c_transmitters, c_ecs):
    c_time = [0, 0]
    for i in range(iterations):
        residual_times = []

        for neuron in c_neurons:
            neuron.calc_time(c_ecs, c_time)
            residual_times.append(neuron.residual_time)

        for e in c_ecs:
            e.calc_lifetimes(c_neurons, c_transmitters, c_time)

        if min(residual_times) == 9999:
            dt = 1
        else:
            dt = min(residual_times)
            
        c_time.append(c_time[-1] + dt)

        for neuron in c_neurons:
            neuron.update_state(c_time)

        for e in c_ecs:
            e.calc_con(c_neurons, c_time, c_transmitters)

    return c_neurons, c_ecs, c_time


def show_plot(p_params, t_time):
    col_num = 0
    p_neurons = p_params[0]
    plt.figure(figsize=(4 * len(p_neurons), len(p_neurons)))
    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k'] * neuron_number
    for pic, dat in enumerate(p_neurons):
        for j in p_neurons[pic].transmitter_dose:
            for n, concentr in enumerate(j):
                if concentr != 0:
                    col_num = n
        if col_num == None:
            col_num = 0
        mp_fill = []
        thresh_fill = []
        t_fill = []
        ww = []
        for num, n_fill in enumerate(p_neurons[pic].potential):
            if n_fill >= p_neurons[pic].threshold - 5e-06:
                mp_fill.append(n_fill)
                thresh_fill.append(p_neurons[pic].threshold)
                t_fill.append(t_time[num])
                ww.append(True)
            else:
                ww.append(False)
        plt.subplot(len(p_neurons), 1, pic + 1)

        plt.plot(t_time, p_neurons[pic].potential, color=colors[col_num], linewidth=2, linestyle="-",
                    label=p_neurons[pic].name)
        plt.fill_between(t_time, p_neurons[pic].potential, [p_neurons[pic].threshold] * len(t_time),
                            where=[i >= (p_neurons[pic].threshold - 5e-06) for i in
                                p_neurons[pic].potential], color=colors[col_num], alpha=0.65)

        plt.ylim(p_neurons[pic].min_potential - 0.01, p_neurons[pic].max_potential + 0.01)
        ax = plt.subplot(len(p_neurons), 1, pic + 1)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.get_xticks()
        ax.set_xticks([])
        ax.set_yticks([p_neurons[pic].threshold])
        ax.set_xticklabels([])
        ax.set_yticks([p_neurons[pic].min_potential - 0.01, p_neurons[pic].max_potential + 0.01])
        ax.set_yticks([p_neurons[pic].threshold], minor=True)
        ax.tick_params(axis='y', which='minor', labelsize=14, labelbottom=1)
        ax.set_yticklabels([])

        ax.grid(which='minor', alpha=1)
        ax.grid(which='major', alpha=0)

        ax.grid(True)
        if pic == len(p_neurons) - 1:
            ax.xaxis.set_label_coords(1.01, -0.025)
        elif pic == 0:
            ax.xaxis.set_label_coords(-0.03, 1.3)
    plt.show()

file_name = 'Aplysia reverse'
params = load_data(file_name)
neurons, transmitters, ecs, iterations, neuron_number, transmitter_number, ECS_number = params
neurons, ecs, time = calculate(neurons, transmitters, ecs)

names = [n.name for n in neurons]
print(search_ensembles(names, neurons, time))
save_data(params, file_name)
show_plot(params, time)
