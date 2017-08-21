# -*- coding: utf-8 -*-

from colouringmap import theme_mapping as tm
import geopandas as gpd
import matplotlib.pyplot as plt

def test_shp():
    gdf = gpd.read_file('testdata/county.shp')

    level_list, colour_list, colour_tuples = tm.colouring_sequence(gdf, colorbysequence='area', break_method='natural_break')

    fig,ax = plt.subplots(figsize=(7,7))
    ax.set_facecolor('cornflowerblue')
    ax = tm.simple_mapping(gdf, colour_list, ax, colour_tuples=colour_tuples, title='area')
    ## colour_tuples for legend (ind, range, colorhex)

    plt.show()

if __name__ == '__main__':
    test_shp()
