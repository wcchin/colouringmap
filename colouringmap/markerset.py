 # -*- coding: utf-8 -*-

import os
import pickle
from matplotlib.font_manager import FontProperties


def get_icons(icon_set, size=12):
    mdir = os.path.dirname(__file__)
    fname = os.path.join(mdir, 'icons', icon_set+'.ttf')
    myfont = FontProperties(fname=fname)
    return myfont

def get_marker(icon_set, icon_name):
    iconsmap = get_char_map(icon_set)
    myfont = get_icons(icon_set)
    return unichr(iconsmap[icon_name]), myfont

def get_char_map(icon_set=None):
    mdir = os.path.dirname(__file__)
    fname = os.path.join(mdir, 'icons', 'icon_map.txt')
    with open(fname, 'rb') as handle:
        iconsmap = pickle.loads(handle.read())
    if not icon_set is None:
        return iconsmap[icon_set]
    else:
        return iconsmap

def list_icon_sets():
    iconsmap = get_char_map()
    return sorted(iconsmap.keys())

def list_icon_names(icon_set):
    iconsmap = get_char_map(icon_set)
    return sorted(iconsmap.keys())

def brandico(icon_name):
    iconsmap = get_char_map('brandico')
    myfont = get_icons('brandico')
    return unichr(iconsmap[icon_name]), myfont

def elusive(icon_name):
    iconsmap = get_char_map('elusive')
    myfont = get_icons('elusive')
    return unichr(iconsmap[icon_name]), myfont

def entypo(icon_name):
    iconsmap = get_char_map('entypo')
    myfont = get_icons('entypo')
    return unichr(iconsmap[icon_name]), myfont

def fontawesome(icon_name):
    iconsmap = get_char_map('fontawesome')
    myfont = get_icons('fontawesome')
    return unichr(iconsmap[icon_name]), myfont

def fontelico(icon_name):
    iconsmap = get_char_map('fontelico')
    myfont = get_icons('fontelico')
    return unichr(iconsmap[icon_name]), myfont

def iconic(icon_name):
    iconsmap = get_char_map('iconic')
    myfont = get_icons('iconic')
    return unichr(iconsmap[icon_name]), myfont

def linecons(icon_name):
    iconsmap = get_char_map('linecons')
    myfont = get_icons('linecons')
    return unichr(iconsmap[icon_name]), myfont

def maki(icon_name):
    iconsmap = get_char_map('maki')
    myfont = get_icons('maki')
    return unichr(iconsmap[icon_name]), myfont

def meteocons(icon_name):
    iconsmap = get_char_map('meteocons')
    myfont = get_icons('meteocons')
    return unichr(iconsmap[icon_name]), myfont

def modernpics(icon_name):
    iconsmap = get_char_map('modernpics')
    myfont = get_icons('modernpics')
    return unichr(iconsmap[icon_name]), myfont

def typicons(icon_name):
    iconsmap = get_char_map('typicons')
    myfont = get_icons('typicons')
    return unichr(iconsmap[icon_name]), myfont

def weathercons(icon_name):
    iconsmap = get_char_map('weathercons')
    myfont = get_icons('weathercons')
    return unichr(iconsmap[icon_name]), myfont

def zocial(icon_name):
    iconsmap = get_char_map('zocial')
    myfont = get_icons('zocial')
    return unichr(iconsmap[icon_name]), myfont

def show_icon(marker, face_colour='navy', size=12, alpha=1., background_colour ='w'):
    import matplotlib.pyplot as plt
    fig,ax = plt.subplots(figsize=(5,5))
    ax.set_aspect('equal')
    ax.set_facecolor(background_colour)
    w, ifont = marker
    ax.text(0, 0, w, fontproperties=ifont, size=size, color=face_colour, alpha=alpha, ha='center', va='center')
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    return ax

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    ii = maki('airport')
    print ii
    show_icon(ii)
    plt.show()
