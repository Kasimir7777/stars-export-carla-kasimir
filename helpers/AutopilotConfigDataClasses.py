from typing import List


class Feature:
    def __init__(self, name: str, value: int, normal_distributed: bool):
        self.name = name
        self.value = value
        self.normal_distributed = normal_distributed

    def __str__(self):
        return ("name: " + self.name + "\n" +
                "value: " + str(self.value) + "\n" +
                "normal_distributed: " + str(self.normal_distributed))

    def __repr__(self):
        return str(self)

class OverlappingGroup:
    def __init__(self, name: str, fraction: int, features: List[Feature]):
        self.name = name
        self.fraction = fraction
        self.features = features

    def __str__(self):
        return ("name: " + self.name + "\n" +
                "fraction: " + str(self.fraction) + "\n" +
                "features: " + str(self.features))

    def __repr__(self):
        return str(self)


class DisjunctGroup:
    def __init__(self, name: str, fraction: int, overlapping_groups: List[OverlappingGroup]):
        self.name = name
        self.fraction = fraction
        self.overlapping_groups = overlapping_groups

    def __str__(self):
        return ("name: " + self.name + "\n" +
                "fraction: " + str(self.fraction) + "\n" +
                "overlapping_groups: " + str(self.overlapping_groups))

    def __repr__(self):
        return str(self)

class AutopilotConfig:
    def __init__(self, disjunct_groups: List[DisjunctGroup]):
        self.disjunct_groups = disjunct_groups

    def __str__(self):
        return "disjuncts: " + str(self.disjunct_groups)

    def __repr__(self):
        return str(self)