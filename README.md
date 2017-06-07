# colouringmap
A tool for colouring the geodataframe (adding categories and colours) for making thematic choropleth map.

### intro 
This is a simple python library for colouring the geodataframe based on a column for scaling. 

Let say there is a polygon geodataframe, with a column recording the population density of each area, and you want to create a thematic map that each polygon shows a colour that match its population density, the denser the population, the darker the colour. Therefore, first thing to do is to categorize them by the population density. Several popular ways to do this, including natural break, equal interval, quantile, standard deviation, head-tail break. After breaking the column values into several levels, next thing to do is setting the colours according to level. 

This tool provide two functions to accomplish these tasks:
1. breaking column values into several levels.
2. setting the colours according to the levels (from the above or user specified).

The two functions returns a list that contain the levels of each record(row), and a list that contain the colours, in the same order as the geodataframe you give it. 

There is another simple_mapping(gdf, colour_list, ax, colour_tuples=colour_tuples) function, that take the polygon geodataframe, colour list (from the above, with the same length as the gdf), an axes (matplotlib ax), and a colour tuples (for legend, also from above), to make a simple polygon map. 

ps: This is designed to use with vmapper, a vector mapping tool in python that generate svg map. But since mapping the variable into map is a common job, so I separated this part as an individual tool for working with geopandas geodataframe.


### dependencies
- numpy: quantile breaks
- jenkspy: natural break
- palettable: getting color map

### install

this package is in alpha, so it is a good idea to install in editable mode (-e)
```sh
git clone https://github.com/wcchin/colouringmap.git
cd colouringmap/
pip install -e .

```

or 

```sh
pip install -e git+https://github.com/wcchin/colouringmap.git#egg=colouringmap

```


### usage

```python
import geopandas as gpd
from colouringmap import theme_mapping as tm 

## reading files (labels in chinese)
gdf = gpd.read_file('testdata/county.shp') ## a polygon file, encoding is utf-8, projection Twd1997/TM2
#gdf = gdf.to_crs(crs) ## reproject to a valid projection's crs

## prepare the level_list, colour_list, and colour_tuples
level_list, colour_list, colour_tuples = tm.colouring_sequence(gdf, colorbysequence='area', break_method='natural_break', break_N=7, color_group='cmocean_sequential', color_name='Turbid_10')

## preparing the matplotlib fig and ax
fig,ax = plt.subplots(figsize=(7,7))
ax.set_facecolor('cornflowerblue') # set the background to a blue color

## making the polygon map
ax = tm.simple_mapping(gdf, colour_list, ax, colour_tuples=colour_tuples, title='area')
plt.show()
```

colouringmap.theme_mapping has three main functions: colouring_sequence (colouring based on a series of statistic numbers), colouring_category (based on a pre-defined category, or named categories), and simple_mapping. 

colouringmap.breaking_levels has a main function: get_levels, which take one list of values (with some other arguments like method, N, cuts), and return two lists: the level_list and cuts point values. 

colouringmap.get_colours has a main function: colour_list, which take a level_list (a list of integer to represent the level), and the colourmaps info (color_group, colour_name, reverse), then return a list of colours with the same length as the level-list (for colouring), and a list with the same length as the set of levels (for making legend). 


### more info
#### about the color
The colors will be getting from palettable, as now the version ins 3.0.0. 

The valid color_group include:
- 'cmocean_diverging'
- 'cmocean_sequential'
- 'colorbrewer_diverging'
- 'colorbrewer_qualitative'
- 'colorbrewer_sequential'
- 'cubehelix'
- 'matplotlib'
- 'mycarta'
- 'tableau'
- 'wesanderson'

The valid color_name can check the website: https://jiffyclub.github.io/palettable/


#### about the breaking methods

The valid breaking methods include:
- 'manual' # must provide a list of cuts (something like [20, 40, 60, 70, 100] for a variable range from 0 to 100), the max element should be the max element of the list, or it will be added
- 'equal_interval' # provide the number of cuts expected
- 'quantile' # must either provide the number of cuts (4 for .25,.50,.75, 1.), or a list of cuts like [.25, .50, .75, 1.]
- 'standard_deviation' # must provide a number of cut, if len(alist)%2==0, then the mean of all values will also be included
- 'natural_break' # must provide a number of cut
- 'head_tail_break' # must provide a number of cut, i have simplified it so it is not that natural as it is in the paper
