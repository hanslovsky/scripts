#!/usr/bin/env python

import sys
import re
import numpy as np
import Levenshtein



# colortable = {'#ffffff' : '15', '#000000' : '0'}


def get_closest_string_from_dict(s, d):
    max_sim = -1
    ret_k, ret_v = (None, None)
    for key, val in d.iteritems():
        curr_sim = Levenshtein.ratio(s, key)
        if curr_sim > max_sim:
            max_sim = curr_sim
            ret_k, ret_v = key, val
    return max_sim, ret_k, ret_v


def get_closest_string_from_dict_html_specific(s, d):
    min_dist = 100000000
    ret_k, ret_v = (None, None)
    for key, val in d.iteritems():
        curr_dist = html_specific_dist(s, key)
        if curr_dist < min_dist:
            min_dist = curr_dist
            ret_k, ret_v = key, val
    return min_dist, ret_k, ret_v


def preprocess(fn):
    s = open(fn, 'r').read()
    s = s.replace('</font>', '')
    s = s.replace('<br>', r'\033[0m\n')
    s = s.replace('black', '#000000')
    s = s.replace('white', '#ffffff')
    return s

    
def get_html_colors(s):
    expr = re.compile(r'#\w{6,6}')
    colors = np.unique(expr.findall(s))
    return colors


def hex_diff(c1, c2):
    try:
        c1 = int('c1')
    except ValueError:
        c1 = ord(c1) - ord('a') + 10

    try:
        c2 = int('c2')
    except ValueError:
        c2 = ord(c2) - ord('a') + 10

    return c1 - c2


def html_specific_dist(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()
    assert len(s1) == 7
    assert len(s2) == 7
    dist = 0
    for i in range(1,7,2):
        dist += 16*abs(hex_diff(s1[i], s2[i]))
        dist += abs(hex_diff(s1[i+1], s2[i+1]))
    return dist



def create_new_dict(colors, d):
    new_dict = {}
    for c in colors:
        max_sim, ret_k, ret_v = get_closest_string_from_dict_html_specific(c, d)
        # print max_sim, ret_k, c, ret_v
        new_dict[c] = ret_v
    return new_dict


def create_colortable_from_file(fn):
    data = np.genfromtxt(fn, dtype=str, comments=')')
    # return dict(enumerate(data))
    return {val : str(idx) for idx, val in enumerate(data)}

colortable = create_colortable_from_file('term_colors_html.dat')

    
    

if __name__ == "__main__":
    fn = sys.argv[1]
    s = preprocess(fn)
    colors = get_html_colors(s)
    new_dict = create_new_dict(colors, colortable)
    
    
    for key, val in new_dict.iteritems():
        s = s.replace('<font color=%s>' % key, r'\e[48;05;%sm\e[01;38;05;%sm' % (val, val))
    s = s + r'\033[0m'
    # print create_colortable_from_file('term_colors_html.dat')
    print s
    # print "\"%s\"" % s
