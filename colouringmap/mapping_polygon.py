 # -*- coding: utf-8 -*-

#import breaking_levels
#import get_colours
import theme_mapping
import mapping_utility

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
from descartes import PolygonPatch
from matplotlib_scalebar.scalebar import ScaleBar


def map_shape(gdf, ax, fc='mediumslateblue', lw=1., ec='#000000', alpha=1., zorder=1, extend_context=True):
    if extend_context:
        minx, miny, maxx, maxy = gdf.geometry.total_bounds
        xlim = [minx,maxx]
        ylim = [miny,maxy]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    patches = []
    patches = [ PolygonPatch(g, fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=zorder) for g in gdf.geometry.tolist() ]
    ax.add_collection(PatchCollection(patches, match_original=True))
    return ax

def map_colour(gdf, colour_col, ax, lw=1., ec='#000000', alpha=1., zorder=1, extend_context=True):
    colour_list = gdf[colour_col].tolist()
    ax = _mapping(gdf, colour_list, ax, colour_tuples=None, lw=lw, ec=ec, alpha=alpha, zorder=zorder, extend_context=extend_context)
    return ax

def map_sequence(gdf, colorbysequence, ax, break_method='quantile', break_N=6, break_cuts=[], break_vmin=None, break_vmax=None, color_group='cmocean_sequential', color_name='Turbid_10', reverse=False, lw=1., ec='#000000', alpha=1., zorder=1, extend_context=True, add_legend=True, font_path=None, legend_loc='upper left', legend_format='%.2f'):
    #'%.2E'

    level_list, colour_list, colour_tuples = theme_mapping.colouring_sequence(gdf, colorbysequence, break_method=break_method, break_N=break_N, break_cuts=break_cuts, break_vmin=break_vmin, break_vmax=break_vmax, color_group=color_group, color_name=color_name, reverse=reverse, legend_format=legend_format)

    if add_legend:
        colour_tuples2 = colour_tuples
    else:
        colour_tuples2 = None
    ax = _mapping(gdf, colour_list, ax, colour_tuples=colour_tuples2, lw=lw, ec=ec, alpha=alpha, zorder=zorder, extend_context=extend_context, font_path=font_path, legend_loc=legend_loc)
    return ax


def map_category(gdf, colorbycategory, ax, color_group='tableau', color_name='TableauLight_10', reverse=False,
  lw=1., ec='#000000', alpha=1., zorder=1, extend_context=True, add_legend=True, font_path=None, legend_loc='upper left', cat_order=None):

    colour_list, colour_tuples = theme_mapping.colouring_category(gdf, colorbycategory, color_group=color_group, color_name=color_name, reverse=reverse, cat_order=cat_order)

    if add_legend:
        colour_tuples2 = colour_tuples
    else:
        colour_tuples2 = None
    ax = _mapping(gdf, colour_list, ax, colour_tuples=colour_tuples2, lw=lw, ec=ec, alpha=alpha, zorder=zorder, extend_context=extend_context, font_path=font_path, legend_loc=legend_loc)
    return ax



def add_border(gdf, ax, ec='#FFFFFF', lw=1., alpha=1., zorder=2, extend_context=False):
    if extend_context:
        minx, miny, maxx, maxy = gdf.geometry.total_bounds
        xlim = [minx,maxx]
        ylim = [miny,maxy]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    patches = []
    patches = [ PolygonPatch(g,fc='none', ec=ec, lw=lw, alpha=alpha, zorder=zorder) for g in gdf.geometry.tolist() ]
    ax.add_collection(PatchCollection(patches, match_original=True))
    return ax


def add_label(gdf, ax, labelcol, font_path=None, font_size=12, font_style='normal', font_colour='black'):
    geom = gdf.geometry.tolist()
    print labelcol
    labs = gdf[labelcol].tolist()

    myfont = get_font(font_path=None, font_size=font_size, font_style=font_style)
    for g,l in zip(geom,labs):
        pt = g.representative_point()
        xx = pt.x
        yy = pt.y
        ax.text(xx, yy, l, color=font_colour, fontproperties=myfont, ha='center', va='center')
    return ax


def add_scalebar(ax, unit='m', fixed_value=None):
    scalebar = ScaleBar(1, unit, fixed_value=fixed_value) # 1 pixel = 0.2 meter
    ax.add_artist(scalebar)
    return ax


def _mapping(gdf, colour_list, ax, colour_tuples=None, xlim=None, ylim=None, ec='#FFFFFF', lw=1., alpha=1., zorder=1, extend_context=True, font_path=None, legend_loc='upper left'):
    ## todo legend of the color_levels

    polys = gdf.geometry.tolist()
    if extend_context:
        minx, miny, maxx, maxy = gdf.geometry.total_bounds
        if xlim is None:
            xlim = [minx,maxx]
        if ylim is None:
            ylim = [miny,maxy]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    patches = []
    for i in range(len(polys)):
        P = polys[i]
        co = colour_list[i]
        #print co
        pa = PolygonPatch(P, fc=co, ec=ec, lw=lw, alpha=alpha, zorder=zorder)
        patches.append(pa)
    ax.add_collection(PatchCollection(patches, match_original=True))


    if not(colour_tuples is None):
        myfont = get_font(font_path=font_path)
        handles = []
        for v,r,c in colour_tuples:
            #print type(r), r.decode('utf-8')
            patch = mpatches.Patch(color=c, label=r.decode('utf-8'))
            handles.append(patch)
        plt.legend(handles=handles, prop=myfont, loc=legend_loc)

    return ax

def get_font(font_path=None, font_size=12, font_style='normal'):
    if font_path is None:
        import os
        mdir = os.path.dirname(__file__)
        #fname = os.path.join(mdir, 'fonts', 'NotoSans-Regular.ttf')
        fname = os.path.join(mdir, 'fonts', 'GenJyuuGothicL-P-Normal.ttf')
    else:
        fname = font_path
    myfont = FontProperties(fname=fname, size=font_size, style=font_style)
    return myfont

def prepare_map(ax, map_context=None, background_colour=None, xlim=None, ylim=None, show_xy=False):
    return mapping_utility.prepare_map(ax, map_context=map_context, background_colour=background_colour, xlim=xlim, ylim=ylim, show_xy=show_xy)
"""
    ax.set_aspect('equal')
    if not show_xy:
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
    else:
        #ax.spines['right'].set_visible(True)
        #ax.spines['top'].set_visible(True)
        ax.tick_params(top='on', right='on')
        ax.xaxis.set_visible(True)
        ax.yaxis.set_visible(True)

    if not map_context is None:
        minx, miny, maxx, maxy = map_context.geometry.total_bounds
        xlim = [minx,maxx]
        ylim = [miny,maxy]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    elif (not xlim is None) and (not ylim is None):
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    if not background_colour is None:
        ax.set_facecolor(background_colour)

    return ax
"""
"""
def test_sequential():
    gdf = gpd.read_file('../testdata/county.shp')

    #sns.set(rc={'axes.facecolor':'cornflowerblue', 'figure.facecolor':'white'})
    fig,ax = plt.subplots(figsize=(7,7))
    #ax.set_facecolor('cornflowerblue')
    ax = prepare_map(ax, map_context=gdf, background_colour='royalblue')
    ax = map_sequence(gdf, 'area', ax, lw=0.)
    ax = add_border(gdf, ax, lw=1.5, ec='#000000', alpha=0.3)
    ax.set_title('areaa')
    ## colour_tuples for legend (ind, range, colorhex)

    plt.show()

def test_category():
    gdf = gpd.read_file('../testdata/county.shp')
    print gdf.head()
    fig,ax = plt.subplots(figsize=(7,7))
    #ax.set_facecolor('cornflowerblue')
    ax = prepare_map(ax, map_context=gdf, background_colour='skyblue')
    ax = map_category(gdf, 'countyname', ax, lw=0., add_legend=False)#cat_order=[u'宜蘭縣',u'新竹縣',u'苗栗縣'])
    ax = add_border(gdf, ax, lw=1.5, ec='#000000', alpha=0.2)
    ax = add_label(gdf, ax, 'countyname', font_colour='blue')
    ax.set_title('county')

    plt.show()

def test_blank():
    gdf = gpd.read_file('../testdata/county.shp')
    fig,ax = plt.subplots(figsize=(7,7))
    #ax.set_facecolor('cornflowerblue')
    ax = prepare_map(ax, map_context=gdf, background_colour='skyblue', show_xy=True)
    ax = map_shape(gdf, ax)
    ax = add_border(gdf, ax, lw=2., ec='white')
    ax.tick_params(top='on', right='on')
    ax = add_scalebar(ax, 'm', fixed_value=100000)
    plt.show()

def test_randomcolor():
    import random
    gdf = gpd.read_file('../testdata/county.shp')
    fig,ax = plt.subplots(figsize=(7,7))
    #ax.set_facecolor('cornflowerblue')
    ax = prepare_map(ax, map_context=gdf, background_colour='skyblue', show_xy=True)
    clrs = []
    for i in range(len(gdf)):
        clrs.append((random.random(),random.random(),random.random()))
    gdf['clrs'] = clrs
    ax = map_colour(gdf, 'clrs', ax)
    plt.show()
"""

if __name__ == '__main__':
    #import seaborn as sns
    import geopandas as gpd
    import matplotlib.pyplot as plt
    #test_sequential()
    #test_category()
    test_blank()
    #test_randomcolor()
