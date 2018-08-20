class AbstractDomain(dict):
    __instance__ = None
    suddenness = 0.0
    familiarity = 0.0
    predictability = 0.0
    valence = 0.0
    goal_relevance = 0.0
    discrepancy_from_expectation = 0.0
    conducive_to_goal = 0.0
    urgency = 0.0
    control = 0.0
    power = 0.0
    adjustment = 0.0

    def __new__(cls, *args, **kwargs):
        if AbstractDomain.__instance__ is None:
            AbstractDomain.__instance__ = dict.__new__(cls)
        return AbstractDomain.__instance__

    def __repr__(self) -> str:
        return "Calculated Variables: \n" + "suddenness=" + str(self.suddenness) + "\nfamiliarity=" \
               + str(self.familiarity) + "\npredictibility=" + str(self.predictability) + "\nvalence=" \
               + str(self.valence) + "\ndiscrepancyFromExpectation=" + str(self.discrepancy_from_expectation) \
               +"\nconduciveToGoal=" + str(self.conducive_to_goal) + "\nurgency=" + str(self.urgency)



