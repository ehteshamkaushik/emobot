class AffectiveDomain(dict):
    __instance__ = None
    emotions = []
    mood = None
    affectiveState = None

    def __new__(cls, *args, **kwargs):
        if AffectiveDomain.__instance__ is None:
            AffectiveDomain.__instance__ = dict.__new__(cls)
        return AffectiveDomain.__instance__

    def __repr__(self) -> str:
        return str(self.emotions)





