multiple_patterns = []


class Comparator:
    """The object allows to compare all combinations of an element and sequence elements.
    
    Creates a tree that branches as long as the combinations of elements for which the coherent function returns 
    True exist. If there are no coherent combinations, appends element to global variable 'multiple_patterns'.
    
    ('A', ['B', 'C', 'D'])
            |
            |__('AB', ['C', 'D'])
            |       |
            |       |__('ABC', ['D'])
            |       |       |
            |       |       |__('ABCD', []) - leaf node
            |       |
            |       |__('ABD', []) - leaf node
            |
            |__('AC', [D])
            |       |
            |       |__('ACD', []) - leaf node
            |
            |__('AD', []) - leaf node     
    Example:
        element = 'a'
        sequence = ['b', 'c', 'd']
        Comparator(element, sequence)
        if coherent('a', 'b') == True and coherent('a', 'c') == False and coherent('a', 'd') == True:
            self.container = [Comparator('ab', ['c', 'd']), Comparator('ad', [])]
    """
    def __init__(self, element, sequence):
        global multiple_patterns
        self.element = element
        self.sequence = sequence
        self.container = []
        self.fill()
        if not self.container and not self.already_in():
            multiple_patterns.append(self.element)

    @staticmethod
    def coherent(first, second, delta=0.05):

        intersects = True
        if first.on_off[0] - delta > second.on_off[1] or first.on_off[1] + delta < second.on_off[0]:
            intersects = False

        if abs(first.period - second.period) < delta and intersects:
            return True
        else:
            return False

    def fill(self):
        multiples = []
        for i, second in enumerate(self.sequence):

            if self.coherent(self.element, second):
                on = max(self.element.on_off[0], second.on_off[0])
                off = min(self.element.on_off[1], second.on_off[1])
                neurons = self.element.neurons + second.neurons
                neurons_rhythms = self.element.neurons_rhythms + second.neurons_rhythms
                period = (self.element.period + second.period) / 2
                on_off = (on, off)
                index = self.sequence.index(second)
                in_seq = self.sequence[index + 1:]
                multiples.append(Comparator(Pattern(neurons, neurons_rhythms, period, on_off), in_seq[:]))
        self.container += multiples

    def contained(self, x, y):
        if len(x) >= len(y):
            return set(x).intersection(set(y)) == set(y)
        else:
            return self.contained(y, x)

    def already_in(self):
        res = False
        for num, i in enumerate(multiple_patterns):
            if self.contained(i.neurons_rhythms, self.element.neurons_rhythms):
                res = True
                break
            elif self.contained(self.element.neurons_rhythms, i.neurons_rhythms):
                multiple_patterns[num] = self.element
                res = True
                break
        return res


def search_ensembles(names, neurons, time):
    global multiple_patterns
    multiple_patterns = []
    single_patterns = []
    neurons = [n for n in neurons if n.name in names]

    for n in neurons:
        print(n.name)
        n.get_rhythm(time)
        for r in n.rhythm:
            neurons_l = [n.name]
            neurons_rhythms = [(n.name, r.__repr__())]
            period = r.period
            for on_off in r.on_off:
                single_patterns.append(Pattern(neurons_l, neurons_rhythms, period, on_off))

    for i, elem in enumerate(single_patterns):
        Comparator(elem, single_patterns[i + 1:])
    return multiple_patterns


class Pattern:

    def __init__(self, neurons, neurons_rhythms, period, on_off):
        self.neurons = neurons
        self.neurons_rhythms = neurons_rhythms
        self.period = period
        self.on_off = on_off


    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
