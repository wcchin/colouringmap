 # -*- coding: utf-8 -*-

import breaking_levels
import get_colours
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
from descartes import PolygonPatch

def colouring_list(alist, break_method='equal_interval', break_N=5, break_cuts=[], break_vmin=None, break_vmax=None, color_group='cmocean_sequential', color_name='Turbid_10', reverse=False):
    level_list, cuts = breaking_levels.get_levels(alist, method=break_method, N=break_N, cuts=break_cuts, vmin=break_vmin, vmax=break_vmax)
    colour_list, colour_tuples = get_colours.colour_list(level_list, color_group=color_group, color_name=color_name, reverse=False)

    ## prepare for colour_level --> for legend
    ## (level, value range, colour_hex)
    colour_tuples2 = []
    pre = 0
    for v,c in colour_tuples:
        r_start = cuts[pre]
        r_stop = cuts[pre+1]
        range_str = '%.2f - %.2f'%(r_start,r_stop)
        colour_tuples2.append((v,range_str,c))
        pre+=1
    return level_list, colour_list, colour_tuples2

def colouring_sequence(gdf, colorbysequence,  break_method='quantile', break_N=5, break_cuts=[], break_vmin=None, break_vmax=None, color_group='cmocean_sequential', color_name='Turbid_10', reverse=False, legend_format='%.2f'):
    #assert len(colorbysequence)>0, 'please check the scalecolorby argument'
    vector = gdf[colorbysequence].tolist()
    level_list, cuts = breaking_levels.get_levels(vector, method=break_method, N=break_N, cuts=break_cuts, vmin=break_vmin, vmax=break_vmax)
    colour_list, colour_tuples = get_colours.colour_list(level_list, color_group=color_group, color_name=color_name, reverse=False)

    ## prepare for colour_level --> for legend
    ## (level, value range, colour_hex)
    colour_tuples2 = []
    pre = 0
    for v,c in colour_tuples:
        r_start = cuts[pre]
        r_stop = cuts[pre+1]
        rr0 = legend_format%r_start
        rr1 = legend_format%r_stop
        range_str = '%s - %s'%(rr0, rr1)
        colour_tuples2.append((v,range_str,c))
        pre+=1
    return level_list, colour_list, colour_tuples2

def colouring_category(gdf, colorbycategory, color_group='tableau', color_name='TableauLight_10', reverse=False, cat_order=None):
    vector = gdf[colorbycategory].tolist()
    vset = list(set(vector))
    vset2 = []
    if not cat_order is None:
        vset2 = cat_order
        cat_list = []#[ cat_order.index(v) for v in vector ]
        for v in vector:
            if v in cat_order:
                cat_list.append( cat_order.index(v) )
            else:
                cat_list.append( len(cat_order) )
        if max(cat_list)==len(cat_order):
            vset2.append('other')
    else:
        cat_list = [ vset.index(v) for v in vector ] # convert names to integers
        vset2 = vset
    print len(vset2)
    print cat_list, cat_order
    colour_list, colour_tuples = get_colours.colour_list(cat_list, color_group=color_group, color_name=color_name, reverse=False)

    ## prepare for colour_level --> for legend
    ## (level, value range, colour_hex)
    colour_tuples2 = []
    for vind,c in colour_tuples:
        o = vset2[vind]
        #print vind
        if not isinstance(o, str):#type()!=str:
            if isinstance(o, (int, long, float, complex)):
                cat_str = str(o)
            elif isinstance(o, unicode):
                cat_str = o.encode('utf-8','ignore')
            else:
                cat_str = o
        else:
            cat_str = o
        #except:
        #    cat_str = str(vset[vind].encode('utf-8'))
        colour_tuples2.append((vind,cat_str,c))
    return colour_list, colour_tuples2


def simple_mapping(gdf, colour_list, ax, colour_tuples=None, title=None, xlim=None, ylim=None, lw=1.):
    ## todo legend of the color_levels

    polys = gdf.geometry.tolist()
    minx, miny, maxx, maxy = gdf.geometry.total_bounds
    if xlim is None:
        xlim = [minx,maxx]
    if ylim is None:
        ylim = [miny,maxy]

    ax.set_aspect('equal')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    patches = []
    for i in range(len(polys)):
        P = polys[i]
        co = colour_list[i]
        #print co
        pa = PolygonPatch(P,fc=co,ec="white", lw=lw, alpha=0.9, zorder=4)
        patches.append(pa)
    ax.add_collection(PatchCollection(patches, match_original=True))

    if not(colour_tuples is None):
        handles = []
        for v,r,c in colour_tuples:
            patch = mpatches.Patch(color=c, label=r)
            handles.append(patch)
        plt.legend(handles=handles)

    return ax


def test_sequential():
    gdf = gpd.read_file('testdata/county.shp')
    #print gdf.head()
    #print gdf.geometry.total_bounds
    """
    areas = gdf.area.tolist()
    lvl, cuts = breaking_levels.get_levels(areas)
    print lvl,cuts
    """
    level_list, colour_list, colour_tuples = colouring_sequence(gdf, colorbysequence='area', break_method='natural_break')

    #sns.set(rc={'axes.facecolor':'cornflowerblue', 'figure.facecolor':'white'})
    fig,ax = plt.subplots(figsize=(7,7))
    ax.set_facecolor('cornflowerblue')
    ax = simple_mapping(gdf, colour_list, ax, colour_tuples=colour_tuples, title='area')
    ## colour_tuples for legend (ind, range, colorhex)

    plt.show()

def test_category():
    gdf = gpd.read_file('testdata/county.shp')

if __name__ == '__main__':
    import geopandas as gpd
    import matplotlib.pyplot as plt
    #import seaborn as sns
    test_sequential()
