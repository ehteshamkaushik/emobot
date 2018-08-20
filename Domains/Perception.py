import Stimuli.Speech as sp
import Domains.AbstractDomain as abd


class Perception:
    abstract_domain = None
    stimuli = None
    speech = None
    change = None

    def __init__(self, speech):
        self.speech = speech
        self.abstract_domain = abd.AbstractDomain()

    def calculate(self):
        self.change = 0
        self.calculate_conducive_to_goal()
        self.calculate_discrepancy_from_expectation()
        self.calculate_familiarity()
        self.calculate_suddenness()
        self.calculate_urgency()
        self.calculate_valence()
        self.calculate_predictability()

    def calculate_conducive_to_goal(self):
        value = (2 * (.5 - abs(self.speech.intensity)) + 2*(.5 - abs(self.speech.duration)) +
                 2*(.5 - abs(self.speech.average_pitch)) + 2 * (.5 - abs(self.speech.volume)) +
                 2*(.5 - abs(self.speech.rate)) + 2*(.5 - abs(self.speech.signal_energy))) / 6
        # self.change = abs(self.abstract_domain.conducive_to_goal - value
        print("Calculating coducive: ", value)
        self.abstract_domain.conducive_to_goal = value

    def calculate_discrepancy_from_expectation(self):
        value = (-2*(.5 - abs(self.speech.signal_energy)) + -2*(.5 - abs(self.speech.volume)) +
                 -2*(.5 - abs(self.speech.rate)) + -2*(.5 - abs(self.speech.average_pitch))) / 4
        # self.change = abs(self.abstract_domain.discrepancy_from_expectation - value)
        self.abstract_domain.discrepancy_from_expectation = value

    def calculate_familiarity(self):
        value = (2*(.5 - abs(self.speech.intensity)) + 2*(.5 - abs(self.speech.duration)) +
                 2*(.5 - abs(self.speech.signal_energy)) + 2*(.5 - abs(self.speech.volume)) +
                 2*(.5 - abs(self.speech.rate)) + 2*(.5 - abs(self.speech.average_pitch))) / 6
        # self.change = abs(self.abstract_domain.familiarity - value)
        self.abstract_domain.familiarity = value

    def calculate_predictability(self):
        # self.change = self.change/6
        # value = 2*(.5 - abs(self.change))
        value = (2 * (.5 - abs(self.speech.intensity)) + 2 * (.5 - abs(self.speech.signal_energy)) +
                 2*(.5 - abs(self.speech.volume)) + 2 * (.5 - abs(self.speech.rate))) / 4
        self.abstract_domain.predictability = value

    def calculate_suddenness(self):
        value = (self.speech.intensity + -1*self.speech.duration + self.speech.volume + self.speech.average_pitch) / 4
        # self.change = abs(self.abstract_domain.suddenness - value)
        self.abstract_domain.suddenness = value

    def calculate_valence(self):
        value = (self.speech.intensity + self.speech.average_pitch + self.speech.volume + self.speech.rate +
                 self.speech.signal_energy) / 5
        # self.change = abs(self.abstract_domain.valence - value)
        self.abstract_domain.valence = value

    def calculate_urgency(self):
        value = (self.speech.intensity + self.speech.duration*-1 + self.speech.signal_energy +
                 self.speech.volume + self.speech.rate + self.speech.average_pitch) / 6
        # self.change = abs(self.abstract_domain.urgency - value)
        self.abstract_domain.urgency = value

