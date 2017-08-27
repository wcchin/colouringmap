 # -*- coding: utf-8 -*-

import palettable as pc
#colors = pc.colorbrewer.diverging.RdYlGn_7.hex_colors

def colour_list(level_list, color_group, color_name, reverse=False):
    hexcs = get_colours(color_group, color_name, reverse=reverse)
    level_set = list(set(level_list))
    #assert len(hexcs)>=len(level_set), 'number of groups should be less than or equal to the number of colors'
    len_cols = len(hexcs)
    if len(hexcs)<len(level_set):
        print '!!!'
        print 'number of colour is less then number of level/category'
        print 'colours will be repeating'
        print '!!!'
        level_list = [ v%len_cols for v in level_list ]
        #level_set = [ v%len_cols for v in level_set ]
    colour_list = [ hexcs[v] for v in level_list ]
    colour_tuples = [ (v, hexcs[v%len_cols]) for v in level_set ]
    return colour_list, colour_tuples

"""
def colour_cat(cat_list, color_group, color_name, reverse=False):
    hexcs = get_colours(color_group, color_name, reverse=reverse)
    cat_set = list(set(cat_list))
    cat_ind_list = [ cat_set.index(v) for v in cat_list ]
    if len(hexcs)<len(cat_set):
        print '!!!'
        print 'number of colour is less then number of category'
        print 'colours will be repeating'
        print '!!!'
        len_cols = len(hexcs)
        cat_ind_list = [ v%len_cols for v in cat_ind_list ]
    colour_list = [ hexcs[v] for v in cat_ind_list ]
    colour_tuples = [ (v, hexcs[i]) for i,v in enumerate(cat_set) ]
    return colour_list, colour_tuples
"""

def get_colours(color_group, color_name, reverse=False):
    color_group = color_group.lower()
    cmap = get_map(color_group, color_name, reverse=reverse)
    return cmap.hex_colors
    """
    if not reverse:
        return cmap.hex_colors
    else:
        return cmap.hex_colors[::-1]
    """

def get_map(color_group, color_name, reverse=False):
    if color_group=='cmocean_diverging':
        cmap = cmocean_diverging(color_name, reverse=reverse)
    elif color_group=='cmocean_sequential':
        cmap = cmocean_sequential(color_name, reverse=reverse)
    elif color_group=='colorbrewer_diverging':
        cmap = colorbrewer_diverging(color_name, reverse=reverse)
    elif color_group=='colorbrewer_qualitative':
        cmap = colorbrewer_qualitative(color_name, reverse=reverse)
    elif color_group=='colorbrewer_sequential':
        cmap = colorbrewer_sequential(color_name, reverse=reverse)
    elif color_group=='cubehelix':
        cmap = cubehelix(color_name, reverse=reverse)
    elif color_group=='matplotlib':
        cmap = matplotlib(color_name, reverse=reverse)
    elif color_group=='mycarta':
        cmap = mycarta(color_name, reverse=reverse)
    elif color_group=='tableau':
        cmap = tableau(color_name, reverse=reverse)
    elif color_group=='wesanderson':
        cmap = wesanderson(color_name, reverse=reverse)
    else:
        cmap = None
        print 'color_group not supported, please check palettable v3.0.0'
        print 'return None'
    return cmap

def cmocean_diverging(color_name, reverse=False):
    return pc.cmocean.diverging.get_map(color_name, reverse=reverse)

def cmocean_sequential(color_name, reverse=False):
    return pc.cmocean.sequential.get_map(color_name, reverse=reverse)

def colorbrewer_diverging(color_name, reverse=False):
    color_name2, num = color_name.split('_')
    return pc.colorbrewer.get_map(color_name2,'diverging', num, reverse=reverse)

def colorbrewer_qualitative(color_name, reverse=False):
    color_name2, num = color_name.split('_')
    return pc.colorbrewer.get_map(color_name2,'qualitative', num, reverse=reverse)

def colorbrewer_sequential(color_name, reverse=False):
    color_name2, num = color_name.split('_')
    return pc.colorbrewer.get_map(color_name2,'sequential', num, reverse=reverse)

def cubehelix(color_name, reverse=False):
    return pc.cubehelix.get_map(color_name, reverse=reverse)

def matplotlib(color_name, reverse=False):
    return pc.matplotlib.get_map(color_name, reverse=reverse)

def mycarta(color_name, reverse=False):
    return pc.mycarta.get_map(color_name, reverse=reverse)

def tableau(color_name, reverse=False):
    return pc.tableau.get_map(color_name, reverse=reverse)

def wesanderson(color_name, reverse=False):
    return pc.wesanderson.get_map(color_name, reverse=reverse)

if __name__ == '__main__':
    a = get_colours('mycarta', 'CubeYF_7', reverse=False)
    b = get_colours('mycarta', 'CubeYF_7', reverse=True)
    #print a
    #print b
    #print a==b
    print mycarta('CubeYF_7', reverse=True).hex_colors
    print mycarta('CubeYF_7', reverse=False).hex_colors
