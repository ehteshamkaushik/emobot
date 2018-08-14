class Emotion:
    arousal = 0.0
    type = None
    decayRate = None
    names = ["Joy", "Surprise", "Fear", "Anger", "Sadness"]

    def __init__(self, type, arousal, decayRate):
        self.type = type
        self.arousal = arousal
        self.decayRate = decayRate

    def decay(self):
        self.arousal -= self.arousal*self.decayRate
        return self.arousal

    def __repr__(self):
        return self.names[self.type] + " " + str(self.arousal)
