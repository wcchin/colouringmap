 # -*- coding: utf-8 -*-

import os

#import get_colours
import breaking_levels
import theme_mapping
import mapping_utility

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib_scalebar.scalebar import ScaleBar
#import matplotlib.patches as mpatches
from matplotlib.text import TextPath
import matplotlib.lines as mlines


def map_scatter(gdf, ax, size=12, marker='.', facecolor='navy', zorder=1, extend_context=True, alpha=1.):
    colour_list = [facecolor]*len(gdf)
    sizes = [size]*len(gdf)
    ax = _mapping(gdf, colour_list, ax, marker=marker, sizes=sizes, alpha=alpha, zorder=zorder, extend_context=extend_context,)
    return ax

def map_category(gdf, cat_column, ax, cat_order=None, marker_order=None, size_order=None, colour_order=None, size=12, facecolor='navy', zorder=1, extend_context=False, alpha=1.):
    default_marker_list = ['.', '*', '+', ',',  '<', '>','^', '_',  'D', 'H', 'P', 'X', 'd', 'h', 'o', 'p', 's', 'v', 'x', '|', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,'1', '2', '3', '4', '8', ]

    if cat_order is None:
        catset = list(set(gdf[cat_column].tolist()))
    else:
        catset = cat_order

    markerset = []
    if not(marker_order is None):
        markerset = marker_order
    i = 0
    while len(markerset)<len(catset):
        if default_marker_list[i] not in markerset:
            markerset.append(default_marker_list[i])
        i+=1
        if i>=len(default_marker_list):
            j = len(catset)-len(markerset)
            if j<=len(default_marker_list):
                markerset.extend(default_marker_list[:j])
            else:
                markerset.extend(default_marker_list)
                i = len(default_marker_list)-1
            print '!!! warning: repeated markers !!!'

    sizeset = []
    if not(size_order is None):
        sizeset = size_order
    while len(sizeset)<len(catset):
        sizeset.append(size)
    colourset = []
    if not(colour_order is None):
        colourset = colour_order
    while len(colourset)<len(catset):
        colourset.append(facecolor)

    for c,m,s,o in zip(catset, markerset, sizeset, colourset):
        temp_gdf = gdf[gdf[cat_column]==c]
        olist = [o]*len(temp_gdf)
        slist = [s]*len(temp_gdf)
        ax = _mapping(temp_gdf, olist, ax, marker=m, sizes=slist, alpha=alpha, zorder=zorder, extend_context=False,)

    if extend_context:
        minx, miny, maxx, maxy = gdf.geometry.total_bounds
        xlim = [minx,maxx]
        ylim = [miny,maxy]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    return ax

def map_colour(gdf, colour_column, ax, size=12, marker='.', zorder=1., extend_context=True, alpha=1.):
    colour_list = gdf[colour_column].tolist()
    sizes = [size]*len(gdf)
    ax = _mapping(gdf, colour_list, ax, marker=marker, sizes=sizes, alpha=alpha, zorder=zorder, extend_context=extend_context,)
    return ax

def map_size(gdf, size_column, ax, size_scale=1., marker='.', facecolor='navy', zorder=1, extend_context=True, alpha=1.):
    colour_list = [facecolor]*len(gdf)
    sizes = gdf[size_column].tolist()
    sizes = [ s*size_scale for s in sizes ]
    ax = _mapping(gdf, colour_list, ax, marker=marker, sizes=sizes, alpha=alpha, zorder=zorder, extend_context=extend_context,)
    return ax

def map_sequence(gdf, bysequence, ax, by_colour=None, by_size=None,
    sizing='level', sizes=12, size_scale=None, marker='.',  break_method='quantile',
    break_N=6, break_cuts=[], break_vmin=None, break_vmax=None,
    color_group='cmocean_sequential', color_name='Turbid_10', reverse=False,
    alpha=1., zorder=1, facecolor='navy',
    extend_context=True, add_legend=True,
    font_path=None, legend_loc='upper left', legend_format='%.2f'):

    if by_colour==True and (by_size is None or by_size==False):
        ax = colour_level_points(gdf, bysequence, ax, sizes=sizes, marker=marker, break_method=break_method,
            break_N=break_N, break_cuts=break_cuts, break_vmin=break_vmin, break_vmax=break_vmax,
            color_group=color_group, color_name=color_name, reverse=reverse,
            legend_format=legend_format, alpha=alpha, zorder=zorder,
            extend_context=extend_context, add_legend=add_legend,
            font_path=font_path, legend_loc=legend_loc)
    elif by_size==True and (by_colour is None or by_colour==False):
        ax = size_level_points(gdf, bysequence, ax, sizing=sizing, sizes=sizes, marker=marker, break_method=break_method,
            break_N=break_N, break_cuts=break_cuts, break_vmin=break_vmin, break_vmax=break_vmax,
            facecolor=facecolor, size_scale=size_scale,
            legend_format=legend_format, alpha=alpha, zorder=zorder,
            extend_context=extend_context, add_legend=add_legend,
            font_path=font_path, legend_loc=legend_loc)
    elif by_size==True and by_colour==True:
        ax = colour_size_level_points(gdf, bysequence, ax, sizing=sizing, sizes=sizes, marker=marker, break_method=break_method,
            break_N=break_N, break_cuts=break_cuts, break_vmin=break_vmin, break_vmax=break_vmax,
            color_group=color_group, color_name=color_name, reverse=reverse,
            legend_format=legend_format, alpha=alpha, zorder=zorder,
            extend_context=extend_context, add_legend=add_legend,
            font_path=font_path, legend_loc=legend_loc)

    elif by_colour is None and by_size is None:
        print 'no styling(by_colour and/or by_size) is True, use map_scatter'
        if isinstance(sizes, (list,tuple)):
            sizes=sizes[0]
        ax = map_scatter(gdf, ax, size=sizes, marker=marker, facecolor=facecolor, zorder=zorder, extend_context=extend_context, alpha=alpha)
    else: # by_size==False and by_colour==False
        print 'nothing had been done cause all types of drawing are False'
        print 'returning empty ax'
    return ax


def colour_level_points(gdf, bysequence, ax, sizes=12, marker='.', break_method='quantile',
    break_N=6, break_cuts=[], break_vmin=None, break_vmax=None,
    color_group='cmocean_sequential', color_name='Turbid_10', reverse=False,
    alpha=1., zorder=1, extend_context=True, add_legend=True,
    font_path=None, legend_loc='upper left',
    legend_format='%.2f'):

    if isinstance(sizes, list):
        sizes = sizes[0]
    sizes = [sizes]*len(gdf)

    level_list, colour_list, colour_tuples = theme_mapping.colouring_sequence(gdf, bysequence, break_method=break_method, break_N=break_N, break_cuts=break_cuts, break_vmin=break_vmin, break_vmax=break_vmax, color_group=color_group, color_name=color_name, reverse=reverse, legend_format=legend_format)

    if add_legend:
        colour_tuples2 = colour_tuples
    else:
        colour_tuples2 = None

    ax = _mapping(gdf, colour_list, ax, colour_tuples=colour_tuples2, marker=marker, sizes=sizes, alpha=alpha, zorder=zorder, extend_context=extend_context, font_path=font_path, legend_loc=legend_loc)
    return ax


def size_level_points(gdf, bysequence, ax, sizing='level', break_method='quantile', break_N=6, break_cuts=[], break_vmin=None, break_vmax=None,
    facecolor='navy', sizes=12, marker='.', size_scale=None,
    alpha=1., zorder=1, extend_context=True, add_legend=True,
    font_path=None, legend_loc='upper left', legend_format='%.2f'):

    size_list = theme_mapping.get_sizes(gdf, bysequence, break_method, break_N, break_cuts, break_vmin, break_vmax, sizing, sizes, size_scale)

    colour_list = [facecolor]*len(gdf)

    ax = _mapping(gdf, colour_list, ax, marker=marker, sizes=size_list, alpha=alpha, zorder=zorder, extend_context=extend_context, font_path=font_path, legend_loc=legend_loc)
    return ax


def colour_size_level_points(gdf, bysequence, ax, marker='.',
    break_method='quantile', break_N=6, break_cuts=[],
    break_vmin=None, break_vmax=None,
    color_group='cmocean_sequential', color_name='Turbid_10', reverse=False,
    sizing='level', sizes=12, size_scale=None,
    alpha=1., zorder=1, extend_context=True, add_legend=True,
    font_path=None, legend_loc='upper left',
    legend_format='%.2f'):

    level_list, colour_list, colour_tuples = theme_mapping.colouring_sequence(gdf, bysequence, break_method=break_method, break_N=break_N, break_cuts=break_cuts, break_vmin=break_vmin, break_vmax=break_vmax, color_group=color_group, color_name=color_name, reverse=reverse, legend_format=legend_format)

    size_list = theme_mapping.get_sizes(gdf, bysequence, break_method, break_N, break_cuts, break_vmin, break_vmax, sizing, sizes, size_scale)

    if add_legend:
        colour_tuples2 = colour_tuples
    else:
        colour_tuples2 = None

    ax = _mapping(gdf, colour_list, ax, colour_tuples=colour_tuples2, marker=marker, sizes=size_list, alpha=alpha, zorder=zorder, extend_context=extend_context, font_path=font_path, legend_loc=legend_loc)
    return ax


"""
def get_icons(iconset, font_size=12):
    mdir = os.path.dirname(__file__)
    fname = os.path.join(mdir, iconset+'.ttf')
    myfont = FontProperties(fname=fname, size=font_size)
    return myfont
"""

def get_font(font_path=None, font_size=12, font_style='normal'):
    if font_path is None:
        mdir = os.path.dirname(__file__)
        #fname = os.path.join(mdir, 'fonts', 'NotoSans-Regular.ttf')
        fname = os.path.join(mdir, 'fonts', 'GenJyuuGothicL-P-Normal.ttf')
    else:
        fname = font_path
    myfont = FontProperties(fname=fname, size=font_size, style=font_style)
    return myfont


def _mapping(gdf, colour_list, ax, colour_tuples=None, marker='.', xlim=None, ylim=None, ec='#FFFFFF', lw=1., sizes=12, alpha=1., zorder=1, extend_context=True, font_path=None, legend_loc='upper left'):
    ## todo legend of the color_levels

    if extend_context:
        minx, miny, maxx, maxy = gdf.geometry.total_bounds
        if xlim is None:
            xlim = [minx,maxx]
        if ylim is None:
            ylim = [miny,maxy]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    pts = gdf.geometry.tolist()
    points = [[],[]]
    for i in range(len(pts)):
        P = pts[i]
        #co = colour_list[i]
        #print co
        xx,yy = P.xy
        #pa = PolygonPatch(P, fc=co, ec=ec, lw=lw, alpha=alpha, zorder=zorder)
        points[0].append(list(xx)[0])
        points[1].append(list(yy)[0])

    if isinstance(marker, str):
        ax.scatter(points[0], points[1], c=colour_list, marker=marker, s=sizes, alpha=alpha, zorder=zorder)
    elif isinstance(marker, tuple):
        w, ifont = marker
        for xx,yy,co,ss in zip(points[0], points[1], colour_list, sizes):
            ax.text(xx, yy, w, fontproperties=ifont, size=ss, color=co, alpha=alpha, zorder=zorder, ha='center', va='center')

    if not(colour_tuples is None):
        myfont = get_font(font_path=font_path)
        handles = []
        if isinstance(marker, tuple):
            w, ifont = marker
            tp = TextPath((0,0), w, prop=ifont, size=12)
            for v,r,c in colour_tuples:
                patch = ax.scatter([-1000,],[-1000,], s=500, marker=tp,  c=c,label=r.decode('utf-8'))
                handles.append(patch)
            ax.legend(handles=handles, prop=myfont, loc=legend_loc)
        elif isinstance(marker, str):
            msize = sizes
            if isinstance(sizes, (list,tuple)):
                msize = sizes[0]
            elif isinstance(sizes, (float,int)):
                msize = sizes
            else:
                msize = 8
            for v,r,c in colour_tuples:
                mar = mlines.Line2D([], [], linestyle="None", color=c, marker=marker,
                          markersize=12, label=r.decode('utf-8'))
                handles.append(mar)
            ax.legend(handles=handles, prop=myfont, loc=legend_loc)

    return ax

def prepare_map(ax, map_context=None, background_colour=None, xlim=None, ylim=None, show_xy=False):
    return mapping_utility.prepare_map(ax, map_context=map_context, background_colour=background_colour, xlim=xlim, ylim=ylim, show_xy=show_xy)





######################3 testing area
def test_scatter():
    import geopandas as gpd
    import markerset as ms
    gdf = gpd.read_file('../testdata/points2008.shp')
    ii = ms.get_marker('weathercons', 'night-lightning')
    fig,ax = plt.subplots(figsize=(7,7))
    ax = prepare_map(ax, map_context=gdf, background_colour='royalblue', show_xy=False)
    ax = map_scatter(gdf, ax, marker=ii, extend_context=False)
    #plt.show()

def test_sequential_colour():
    import geopandas as gpd
    import markerset as ms
    ii = ms.get_marker('brandico', 'facebook')
    #ii = ms.weathercons('horizon')
    gdf = gpd.read_file('../testdata/points2008.shp')
    fig,ax = plt.subplots(figsize=(7,7))
    ax = prepare_map(ax, map_context=gdf, background_colour='royalblue', show_xy=False)
    ax = map_sequence(gdf, 'time', ax, by_colour=True,  marker=ii, extend_context=False)
    #ax = add_border(gdf, ax, lw=1.5, ec='#000000', alpha=0.3)
    #ax.set_title('areaa')
    ## colour_tuples for legend (ind, range, colorhex)
    ax.set_title('test sequential colour')
    #plt.show()

def test_sequential_size():
    import geopandas as gpd
    import markerset as ms
    ii = ms.get_marker('maki', 'airport')
    #ii = ms.weathercons('horizon')
    gdf = gpd.read_file('../testdata/points2008.shp')
    fig,ax = plt.subplots(figsize=(7,7))
    ax = prepare_map(ax, map_context=gdf, background_colour='royalblue', show_xy=False)
    ax = map_sequence(gdf, 'time', ax, by_size=True, marker=ii, extend_context=False)
    ax.set_title('test sequential size level')
    #plt.show()

def test_sequential_size2():
    import geopandas as gpd
    import markerset as ms
    ii = ms.get_marker('linecons', 'paper-plane')
    #ii = ms.weathercons('horizon')
    gdf = gpd.read_file('../testdata/points2008.shp')
    fig,ax = plt.subplots(figsize=(7,7))
    ax = prepare_map(ax, map_context=gdf, background_colour='royalblue', show_xy=False)
    ax = map_sequence(gdf, 'time', ax, by_size=True, sizing='graduated', marker=ii, extend_context=False)
    ax.set_title('test sequential size graduated')
    #plt.show()

def test_sequential_both():
    import geopandas as gpd
    import markerset as ms
    ii = ms.get_marker('fontawesome', 'user-o')
    #ii = ms.weathercons('horizon')
    gdf = gpd.read_file('../testdata/points2008.shp')
    fig,ax = plt.subplots(figsize=(7,7))
    ax = prepare_map(ax, map_context=gdf, background_colour='royalblue', show_xy=False)
    ax = map_sequence(gdf, 'time', ax, by_colour=True, by_size=True, marker=ii, extend_context=False)
    ax.set_title('test sequential colour and size')
    #plt.show()

def test_listing():
    import markerset as ms
    print ms.list_icon_sets()
    print ms.list_icon_names('weathercons')
    #print ms.get_char_map('weathercons')['horizon']
    ii = ms.get_marker('weathercons', 'night-lightning')
    #ii = ms.weathercons('horizon') # or this

if __name__ == '__main__':
    test_listing()
    test_sequential_colour()
    test_sequential_size()
    test_sequential_size2()
    test_sequential_both()
    test_scatter()
    plt.show()

######################3 testing area
