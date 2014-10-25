from intervaltree import *

""" The most important function exported from this module is the final one,
    best_partners(), which, given a tree, a student in the tree, and a set of
    weights for times of day, returns a list of students, sorted by "time score",
    which signifies how much of their free time overlaps, giving more weight
    to longer periods of consecutive time, and to time which is weighted highly.

    The other functions in this module are primarily helper functions, but they
    could be useful for other interval-tree-querying.
"""


def amount_overlap(start1, end1, start2, end2):
    later_start = start1 if start1 > start2 else start2
    earlier_end = end1 if end1 < end2 else end2
    time = earlier_end - later_start if earlier_end > later_start else 0
    return (time, later_start, earlier_end)


def list_overlaps(tree, start, end):
    result = {}
    for x in tree[start:end]:
        if x.data not in result:
            result[x.data] = []
        result[x.data].append(amount_overlap(x.begin, x.end, start, end))
    return result


def concatenate_list_dicts(d1, d2):
    result = {}
    for key in d1:
        result[key] = d1[key]
    for key in d2:
        if key not in result:
            result[key] = []
        result[key].append(d2[key])
    return result

def clean(d):
    for key in d:
        one_list = []
        for elem in d[key]:
            for tup in elem:
                one_list.append(tup)
        d[key] = one_list
    return d


def student_overlaps(tree, student_name):
    student_times = []
    totals = {}
    for period in tree:
        if period.data == student_name:
            totals = concatenate_list_dicts(totals, list_overlaps(tree, period.begin, period.end))
    return clean(totals)


def best_partners(tree, student_name, time_weights):
    laps = student_overlaps(tree, student_name)
    time_squares = {}
    for partner in laps:
        time_squares[partner] = 0
        for time in laps[partner]:
            (inc, start, end) = time
            for period in time_weights:
                if period[0] <= start <= period[1]:
                    inc *= period[2]
                    break
            time_squares[partner] += inc ** 2
    time_squares = sorted(time_squares.items(), key=lambda x: x[1], reverse=True)
    return time_squares


