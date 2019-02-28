class Rhythm:

    def __init__(self):

        self.on_off = None
        self.bursts = None
        self.durations = None
        self.period = None
        self.cycles = None
        self.id = None
        self.indexes = None

    def __eq__(self, other):
        if isinstance(other, Rhythm) and compare(self.durations, other.durations) == 2 and self.cycles == other.cycles:
            return True
        else:
            return False

    def __str__(self):
        return 'R_' + str(self.id)

    def __repr__(self):
        return 'R_' + str(self.id)


def search_rhythm(bursts_pauses, burst_limits, delta=0.1):
    rhythm_id = 0
    result = []

    def get_rhythms(seq):
        nonlocal rhythm_id
        rhythms = []
        ps_close = [False, False]
        start = -1
        stop = -2
        cycles = [0, 0]
        for pos, (preceding, sequent) in enumerate(zip(seq[:-1], seq[1:])):
            if not ps_close[1] and compare(preceding, sequent, delta) == 2:
                start = preceding[0][2]
                cycles[0] = pos
                fb_ind = (preceding[0][2], preceding[-1][2] + 1)
                ps_close[1] = True

            elif ps_close[1] and compare(preceding, sequent, delta) == 2:
                ps_close[0] = ps_close[1]
                if (ps_close[0] and ps_close[1]) and pos == len(seq) - 2:
                    stop = sequent[-1][2]
                    cycles[1] = pos
                    ps_close = [False, False]

            elif ps_close[1] and compare(preceding, sequent, delta) == 1:
                stop = sequent[-1][2]
                cycles[1] = pos
                ps_close = [False, False]

            elif ps_close[0] and ps_close[1] and compare(preceding, sequent, delta) == 0:
                stop = sequent[-1][2] - 1
                cycles[1] = pos

                ps_close = [False, False]
            else:
                start = -1
                ps_close = [False, False]
                continue
            if stop >= start:

                new_r = Rhythm()
                new_r.on_off = [(burst_limits[start][0], burst_limits[stop][1])]
                new_r.bursts = burst_limits[fb_ind[0]:fb_ind[1]]
                new_r.durations = bursts_pauses[fb_ind[0]:fb_ind[1]]
                new_r.period = burst_limits[sequent[0][2]][0] - burst_limits[preceding[0][2]][0]
                new_r.indexes = [(start, stop)]
                new_r.cycles = cycles[1] - cycles[0] + 1

                rhythms.reverse()
                for i, r in enumerate(rhythms):
                    if compare(new_r.durations, r.durations, delta) == 2 and new_r.cycles == r.cycles:
                        rhythms[i].on_off.append((burst_limits[start][0], burst_limits[stop][1]))
                        rhythms[i].indexes.append((start, stop))
                        new_r.id = r.id
                        break
                rhythms.reverse()

                if new_r.id is None:
                    new_r.id = rhythm_id
                    rhythm_id += 1
                    rhythms.append(new_r)
                start = -1
                stop = -2

        return rhythms

    def process_bp():
        for i in range(1, 1 + len(bursts_pauses) // 2):
            bp_div = divide(bursts_pauses, i)
            for bp in bp_div:
                rhythms = get_rhythms(bp)
                for r in rhythms:
                    insert_rhythm(bursts_pauses, r)
                    result.append(r)
                if rhythms:
                    return process_bp()

    process_bp()

    return result


def compare(first, second, delta=0.05):
    result = 2
    if len(first) == len(second):
        for i, elem in enumerate(first):
            if isinstance(first[i][0], float) and isinstance(second[i][0], float):

                if abs(first[i][0] - second[i][0]) > delta or abs(first[i][1] - second[i][1]) > delta:
                    result = 0
                if i == len(first) - 1:
                    if abs(first[i][0] - second[i][0]) < delta and not abs(first[i][1] - second[i][1]) < delta:
                        result = 1

            elif isinstance(first[i][0], Rhythm) and isinstance(second[i][0], Rhythm):

                if first[i][0] != second[i][0] or abs(first[i][1] - second[i][1]) > delta:
                    result = 0
                if i == len(first) - 1:
                    if first[i][0] == second[i][0] and not abs(first[i][1] - second[i][1]) < delta:
                        result = 1
            else:
                result = 0
                break
    else:
        result = 0

    return result


def get_burst_limits(activation_sequence, time):
    """Finds time limits of each burst.

    Iterates through every neighboring pair of elements in binary activation sequence of a neuron and finds the time
    of each activity change (from 1 to 0 and inverse).

    :param list activation_sequence: Binary sequence of activation function values of a neuron.
    :param list time: Sequence of float numbers defining the time of an event occurrence.
    :return: List of two-element lists where the first and the second elements are the the onset and
        the offset times of the burst respectively.
    :rtype: list
    """

    burst_limits = []

    for i, (preceding, sequent) in enumerate(zip(activation_sequence[:-1], activation_sequence[1:])):

        if (preceding == 0 and sequent == 1) or (i == 0 and preceding == 1):
            burst_limits.append([time[i + 1]])

        elif preceding == 1 and sequent == 0:
            burst_limits[-1].append(time[i + 1])

    if burst_limits and len(burst_limits[-1]) == 1:
        burst_limits[-1].append(time[-1])

    return burst_limits


def get_bursts_pauses(burst_limits, time):
    """Finds duration of each burst.

    Iterates through the list of burst limits and finds the difference between the onset and the offset time.

    :param list burst_limits: List of burst time limits.
    :return: List if float numbers equal to durations of bursts.
    :rtype: list
    """

    bursts_pauses = []

    for i, (preceding, sequent) in enumerate(zip(burst_limits[:-1], burst_limits[1:])):
        burst = preceding[1] - preceding[0]
        pause = sequent[0] - preceding[1]
        bursts_pauses.append((burst, pause, i))
        if i == len(burst_limits) - 2:
            bursts_pauses.append((sequent[1] - sequent[0], time[-1] - sequent[1], i + 1))
    return bursts_pauses


def divide(bursts_pauses, i):
    result = []
    for start in range(1, i + 1):
        int_result = []
        elem = []
        for pos, num in enumerate(bursts_pauses[start - 1:]):
            if len(bursts_pauses[pos:]) + len(elem) >= i and len(bursts_pauses[start - 1:])//i > 1:
                elem.append(num)
                if len(elem) == i:
                    int_result.append(elem)
                    elem = []
            else:
                break
        if int_result:
            result.append(int_result)

    return result


def insert_rhythm(bursts_pauses, r):
    for on_off in r.indexes:
        start = next(i for i, j in enumerate(bursts_pauses) if j[2] == on_off[0])
        stop = next(i for i, j in enumerate(bursts_pauses) if j[2] >= on_off[1])
        pause = next(i[1] for i in bursts_pauses if i[2] >= on_off[1])

        del bursts_pauses[start:stop + 1]
        bursts_pauses.insert(start, (r, pause, on_off[0]))


class Neuron:
    """Класс, определяющий свойства универсального нейрона."""
    def __init__(self, transmitters, ecs):

        self.name = 'Neuron '
        self.max_potential = 0.9
        self.min_potential = 0
        self.threshold = 0.6
        self.rest_potential = 0
        self.rebound_threshold = -9999
        self.rebound_speed = 500
        self.speed_01 = 0
        self.speed_10 = 0
        self.speed_11 = 0
        self.speed_00 = 0
        self.potential = [0, 0]
        self.receptor_weight = [[0] * transmitters] * ecs
        self.transmitter_dose = [[0] * transmitters] * ecs

        self.residual_time = 9999
        self.zero_time = 9999
        self.flag = 0
        self.time = [self.residual_time, self.zero_time]
        self.du_end = 0

        self.du = 0
        self.activations = []

        self.w_zero_list = [0]*transmitters
        self.sum = 0
        self.rhythm = []

    def calc_time(self, ecs, time):

        u = self.potential
        w = self.receptor_weight
        u_max = self.max_potential
        u_min = self.min_potential
        u_rest = self.rest_potential
        u_threshold = self.threshold
        u_pir_threshold = self.rebound_threshold
        self.du = 0
        self.sum = 0
        self.residual_time = 9999
        self.flag = 0

        # Суммарное воздействие всех трансмиттеров
        for i in range(len(ecs)):
            if w[i] != self.w_zero_list:
                for k in range(len(ecs[i].con)):
                    self.sum += w[i][k] * ecs[i].con[k][-1]
            else:
                continue
        if self.speed_01 >= 0:
            if abs(u[-1] - u_rest) < 5e-06 and u[-2] >= u_rest:
                self.du_end = self.speed_01
            elif abs(u[-1] - u_threshold) < 5e-06 and u[-2] < u_threshold - 5e-06 and u[-1] >= u_threshold:
                self.du_end = self.speed_11
            elif abs(u[-1] - u_max) < 5e-06 and u[-2] >= u_threshold - 5e-06:
                self.du_end = self.speed_10
            elif u[-2] >= u_threshold - 5e-06 and u_rest + 5e-06 < u[-1] < u_threshold:
                self.du_end = self.speed_00

        elif self.speed_01 < 0:
            if abs(u[-1] - u_rest) < 5e-06:
                if self.sum == 0:
                    self.du_end = 0
                elif self.sum > 0:
                    self.du_end = self.speed_01
                elif self.sum < 0:
                    self.du_end = (-1) * self.speed_01
            elif u_rest - u[-1] > 5e-06:
                self.du_end = (-1)*self.speed_01
            elif u[-1] - u_rest > 5e-06 and 5e-06 > u[-2] - u_rest:
                self.du_end = self.speed_01
            elif abs(u[-1] - u_threshold) < 5e-06 and u[-2] < u_threshold - 5e-06 and u[-1] >= u_threshold:
                self.du_end = self.speed_11
            elif abs(u[-1] - u_max) < 5e-06 and u[-2] >= u_threshold - 5e-06:
                self.du_end = self.speed_10
            elif u[-2] >= u_threshold - 5e-06 and u_rest + 5e-06 < u[-1] < u_threshold:
                self.du_end = self.speed_00

        if abs(u[-1] - u_pir_threshold) < 5e-06:
            self.du_pir = self.rebound_speed
        elif abs(u[-1] - u_threshold) < 5e-06 and self.du_pir == self.rebound_speed:
            self.du_pir = 0
        if time[-1] == 0:
            self.du_pir = 0


        self.du += self.sum + self.du_end + self.du_pir

        if self.speed_01 < 0 and self.speed_10 < 0 and u[-1] < u_rest - 5e-06 and self.du > 0:
            self.residual_time = (u_rest - u[-1]) / self.du
        elif self.speed_01 < 0 and self.speed_10 < 0 and abs(
            u[-1] - u_rest) < 5e-06 and self.du != 0:
            self.residual_time = 0.0001

        elif u_max >= u[-1] > (u_threshold + 5e-06) and self.du < 0:
            self.residual_time = -(u[-1] - u_threshold + (2e-06)) / self.du

        elif (u_max - 5e-06) > u[-1] >= u_threshold and self.du > 0:
            self.residual_time = (u_max - u[-1]) / self.du

        elif (u_rest + 5e-06 < u[-1] <= u_threshold) and self.du < 0:
            self.residual_time = -(u[-1] - u_rest) / self.du

        elif u[-1] < u_threshold - 5e-06 and self.du > 0:
            self.residual_time = (u_threshold - u[-1]) / self.du

        elif u_pir_threshold >= u_min and (u_pir_threshold < u[-1] < u_threshold) and self.du < 0:
            self.residual_time = -(u[-1] - u_pir_threshold) / self.du

    def update_state(self, time):

        u = self.potential
        u_max = self.max_potential
        u_min = self.min_potential
        u_rest = self.rest_potential
        u_threshold = self.threshold
        u_pir_threshold = self.rebound_threshold

        if self.zero_time == 0 and self.flag == 'u_max':
            u.append(u_max)
        elif self.zero_time == 0 and self.flag == 'u_min':
            u.append(u_rest)
        else:
            u.append(u[-1] + (time[-1] - time[-2]) * self.du)

        if u[-1] > u_max:
            u[-1] = u_max
        elif u[-1] < u_min:
            u[-1] = u_min
        if abs(u[-1] - u_threshold) < 5e-07:
            u[-1] = u_threshold
            pass
        if abs(u[-1] - u_pir_threshold) < 5e-07:
            u[-1] = u_pir_threshold

        if u[-1] >= u_threshold:
            self.activations.append(1)
        else:
            self.activations.append(0)

    def get_rhythm(self, time):
        burst_limits = get_burst_limits(self.activations, time)
        bursts_pauses = get_bursts_pauses(burst_limits, time)
        self.rhythm = search_rhythm(bursts_pauses, burst_limits)