from overlaps import *
from intervaltree import *


""" This class is meant to hold information about students' schudling preferences.
    Each instance of a schedule class maintains a list of students, and a weighting
    of preferences for students.
    Each student is associated with a list of time intervals, representing when they
    are free.  They may also have:
        - A dictionary of preferences.  When users have the same value set for a
          particular preference, the weight of that preference will be added to
          their score.
        - A list of tuples listing preferences for times of day.  Each tuple has
          the form (start, end, weight), meaning that a time period that begins
          between start and end will be weighted by the given value
    Finally, for a student, you can search the best matches for that student,
    which determines a particular score between that student and each other.
    The score is based on total overlapping free time (with preference given for
    longer amounts of consecutive time), how much of that free time is a preferred
    time for the student, and how many of their preferences are shared.
    You can also search for the best matches for everyone, which results in
    a list of tuples being returned, where the first value is the student, and
    the second is a list of how well they pair with each other student.
    The list is sorted by the score of the best match found for that student.
"""
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

    def add_student(self, name, time_list, preferences={}, time_weights=[]):
        self.students[name] = ({}, time_weights)
        for category in preferences:
            self.students[name][0][category] = preferences[category]
        for interval in time_list:
            self.add_interval(name, interval[0], interval[1])

    def best_matches_for(self, student):
        times = best_partners(self.tree, student, self.students[student][1])
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
                if pref in self.students[student][0] and pref in self.students[name][0] and self.students[student][0][pref] == self.students[name][0][pref]:
                    score += self.preference_weight(pref)
            result.append((name, score));
        return sorted(result, key=lambda x: x[1], reverse=True)

    def get_all_best_matches(self):
        results = {}
        for name in self.students:
            results[name] = self.best_matches_for(name)
        return sorted(results.items(), key=lambda x:x[1][0][1], reverse=True);



def pair_students(sched):
    pairings = sched.get_all_best_matches()
    final_pairings = []
    paired = []
    for x in pairings:
        for y in x[1]:
            if y[0] not in paired:
                final_pairings.append((x[0], y[0]))
                paired.append(x[0])
                paired.append(y[0])
                break
    return final_pairings
