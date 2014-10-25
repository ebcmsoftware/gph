from overlaps import *
from intervaltree import *

class Schedule(object):
    def __init__(self, preferences={}):
        self.tree = IntervalTree()
        self.students = {}
        self.preferences = preferences
        if "time" not in preferences:
            self.preferences["time"] = 10

    def add_preference(self, name, weight):
        self.preferences[name] = weight

    def preference_weight(self, pref):
        if self.preferences[pref]:
            return self.preferences[pref]
        else:
            return 0

    def add_interval(self, name, start, end):
        self.tree[start:end] = name
        if name not in self.students:
            self.students[name] = {}

    def add_student(self, name, time_list, preferences={}):
        self.students[name] = {}
        for category in preferences:
            self.students[name][category] = preferences[category]
        for interval in time_list:
            self.add_interval(name, interval[0], interval[1])

    def best_matches_for(self, student):
        times = best_partners(self.tree, student)
        best_times = [i for i in times if i[0] != student];
        if not best_times or "time" not in self.preferences:
            return best_times
        highest = best_times[0][1]
        time_weight = self.preference_weight("time")
        result = []
        for tup in best_times:
            name = tup[0]
            score = (tup[1] / highest) * time_weight
            for pref in self.preferences:
                if pref in self.students[student] and pref in self.students[name] and self.students[student][pref] == self.students[name][pref]:
                    score += self.preference_weight(pref)
            result.append((name, score));
        return sorted(result, key=lambda x: x[1], reverse=True)
