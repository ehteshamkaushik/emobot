import Domains.AbstractDomain as abd
import Domains.AffectiveDomain as afd
import Domains.Emotion as em


class GenerateEmotion:
    affective_domain = None
    abstract_domain = None

    def __init__(self):
        self.affective_domain = afd.AffectiveDomain()
        self.abstract_domain = abd.AbstractDomain()
        self.affective_domain.emotions.clear()

    def calculateEmotions(self):
        self.calculate_fear()
        self.calculate_anger()
        self.calculate_sadness()
        self.calculate_joy()
        self.calculate_surprise()

    def calculate_fear(self):
        value = (self.abstract_domain.suddenness + -1*self.abstract_domain.familiarity + \
                -1*self.abstract_domain.predictability + -1*self.abstract_domain.valence + \
                self.abstract_domain.discrepancy_from_expectation + -1*self.abstract_domain.conducive_to_goal + \
                self.abstract_domain.urgency + -1*self.abstract_domain.power + -1*self.abstract_domain.adjustment) / 9
        if value > 0:
            emotion = em.Emotion(2, value, 0)
            self.affective_domain.emotions.append(emotion)

    def calculate_anger(self):
        value = (self.abstract_domain.suddenness + -1 * self.abstract_domain.familiarity + \
                -1 * self.abstract_domain.predictability + self.abstract_domain.discrepancy_from_expectation + \
                -1*self.abstract_domain.conducive_to_goal + self.abstract_domain.urgency + self.abstract_domain.power \
                + self.abstract_domain.adjustment + self.abstract_domain.control) / 9
        if value > 0:
            emotion = em.Emotion(3, value, 0)
            self.affective_domain.emotions.append(emotion)

    def calculate_sadness(self):
        value = (self.abstract_domain.suddenness*-1 + -1 * self.abstract_domain.conducive_to_goal +
                 -1*self.abstract_domain.urgency + -1*self.abstract_domain.power + -1*self.abstract_domain.control +
                 2*(.5 - self.abstract_domain.adjustment) + -1 * self.abstract_domain.familiarity) / 7
        if value > 0:
            emotion = em.Emotion(4, value, 0)
            self.affective_domain.emotions.append(emotion)

    def calculate_joy(self):
        value = (2*(.5 - self.abstract_domain.suddenness) + -1*self.abstract_domain.predictability +
                 self.abstract_domain.conducive_to_goal + -1*self.abstract_domain.urgency +
                 2*(.5 - self.abstract_domain.adjustment)) / 5
        if value > 0:
            emotion = em.Emotion(0, value, 0)
            self.affective_domain.emotions.append(emotion)

    def calculate_surprise(self):
        value = (self.abstract_domain.suddenness + -1*self.abstract_domain.predictability +
                 self.abstract_domain.conducive_to_goal + self.abstract_domain.urgency +
                 self.abstract_domain.discrepancy_from_expectation + 2*(.5 - self.abstract_domain.adjustment) +
                 -1*self.abstract_domain.control) / 7
        if value > 0:
            emotion = em.Emotion(1, value, 0)
            self.affective_domain.emotions.append(emotion)




