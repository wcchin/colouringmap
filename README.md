
[english version](#eng_version) -- [中文版](#zh_version)

<a name="eng_version">
# colouringmap
</a>
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
pip install git+https://github.com/wcchin/colouringmap.git#egg=colouringmap

```


### usage

```python
import geopandas as gpd
from colouringmap import theme_mapping as tm 

## reading files
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

colouringmap.theme_mapping has four main functions: colouring_sequence and colouring_list (colouring based on a series of statistic numbers, _sequence take a gdf and a column name as the input, _list take a list as input), colouring_category (based on a pre-defined category, or named categories), and simple_mapping. 

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

### updated
2016-06-10: added colouring_list, to take a list as input and return the 3 lists: levels, colours, and colour_tuples.

-----------

demo map result -- 範例結果
![density choropleth map](testdata/figure_density_of_some_crime.png?raw=true "density of some crime")

-----------

[english version](#eng_version) -- [中文版](#zh_version)

<a name="zh_version">
# colouringmap
</a>
「分層」與「設色」的地圖工具 -- 對 GeoPandas geodataframe 加上分層級及顏色，來製作分層設色的主題地圖的 python 工具。

### 簡介 
這是一個爲了方便畫圖而寫的 python 工具，主要是針對圖層資料的一個欄位(連續數字，例如統計值之類)來作資料的分層，以及根據這個分層來加入顏色。

舉例來說，我們有一個面資料圖層的 geodataframe，其中有一個欄位記錄着各個區塊的人口密度，而我們想要繪製一個人口密度的分布圖，也就是每一個面區塊用一個顏色來繪製，而這個顏色是人口密度越高則越深。
所以，第一步要做的就是針對這連續數字所組成的人口密度欄位去作分層，值最高的那些區塊一層 ... 最低的那些區塊一層，然後同一層用一個顏色來繪製。這就是分層設色圖。
常用的分層方法包括: natural break, quantile，標註差分組， head-tail break。至於顏色，主要會用的是單色的漸層，2色的漸層，以及3色的漸層。

而這個工具的目標就是提供以下兩個主要的功能來滿足上述提到的工作：
1. 針對欄位進行分層
2. 依據分層結果來上色

這兩個功能在工具中被寫成兩個 python function:
1. 其一會回傳一個跟資料長度一樣長的 list，每一個 element 表示各個面區塊的層級；
2. 其二會吃進一個分層的 list，可以是前面的 function 所產生，或是使用者自行準備好的，然後會回傳一個一樣長的 list， 每一個 element 是一個 color hex code (類似 #FFFF00)，提供用來畫圖。

這兩個 list 的順序與喂進去的 geodataframe 的順序一致。

除此之外，還有一個簡單的畫圖 function，叫做 simple_mapping，這會吃進 geodataframe, 顏色的 list，一個 matplotlib ax，以及一個顏色組的 list (供產生圖例)。
這 function 可以用來繪製分層設色圖，是一種面圖層的呈現方式。

其實，前述兩個 function 會回傳出兩個 list，而若資料不是面資料，也可以應用這兩個 list 來產生其他的主題圖，包括變換點的大小的 gruaduated symbol 圖 (點圖層)，或是改變點或線顏色，並不限於用 matplotlib 畫分層設色的面圖層地圖。

ps: 這工具主要是爲了 vmapper 而設計， vmapper 是一個方便的畫地圖小工具，功能特點在於吃進 geodataframe，然後產出 svg 地圖。
不過後來想到其實「分層」，及「設色」兩個動作在畫地圖時很常會用到，所以就將這工具獨立出來。後續會再花點時間把功能加入到 vmapper 中。

### dependencies
- numpy: quantile breaks 
- jenkspy: natural break 
- palettable: 調色盤，這小工具會用這調色盤來獲取顏色的值

### 安裝

這套件還在 alpha 階段, 推薦用 editable mode (-e)
```sh
git clone https://github.com/wcchin/colouringmap.git
cd colouringmap/
pip install -e .

```

或是直接從網路上裝下來  

```sh
pip install git+https://github.com/wcchin/colouringmap.git#egg=colouringmap

```


### 使用

```python
import geopandas as gpd
from colouringmap import theme_mapping as tm 

## 讀取資料
gdf = gpd.read_file('testdata/county.shp') ## a polygon file, encoding is utf-8, projection Twd1997/TM2
#gdf = gdf.to_crs(crs) ## reproject to a valid projection's crs

## 準備 level_list(分層 list), colour_list (設色 list), 及 colour_tuples
level_list, colour_list, colour_tuples = tm.colouring_sequence(gdf, colorbysequence='area', break_method='natural_break', break_N=7, color_group='cmocean_sequential', color_name='Turbid_10')

## 準備好 matplotlib fig and ax
fig,ax = plt.subplots(figsize=(7,7))
ax.set_facecolor('cornflowerblue') # set the background to a blue color

## 產生面的分層設色圖
ax = tm.simple_mapping(gdf, colour_list, ax, colour_tuples=colour_tuples, title='area')
plt.show()
```

colouringmap.theme_mapping 有四個主要的 functions: colouring_sequence 及 colouring_list (針對連續的統計數字的欄位作分層設色,前者的輸入爲一個 gdf 及 一個欄位, 後者需要輸入一個 list), colouring_category (應用預先準備好的分層、或是列別變項，若是後者建議用 category 類的調色盤), and simple_mapping (繪製簡單的分層設色圖)。 

colouringmap.breaking_levels 有一個主要的 function: get_levels, 這會針對一個欄位來進行分層，需要提供的 argument 包括分層方法、分幾層、或預先設定的分層切點，並且會產生兩個 list : 分層的 list (level_list) 及 切點值的 list (cuts point values)。 

colouringmap.get_colours 則有一個主要 function: colour_list, 針對分層 list (一個用整數來反映分層順序的 list)， 及分層顏色的設定 (color_group, colour_name, reverse)，並且回傳一樣長的 list， 其中記錄每一個面空間單元所對應的顏色， 及一個跟分層數(例如分 5層，就是5)一樣長的 list 記錄着顏色及分層所對應的意義，供製作圖例。 


### 其他資訊
#### 關於顏色
顏色都是從 palettable 中取得，目前其版本爲 3.0.0。 

可用的 color_group 包括:
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

可用的 color_name 請查看: https://jiffyclub.github.io/palettable/


#### 關於分層方法

可用的分層方法包括：
- 'manual' # 需要提供切點 list (類似 [20, 40, 60, 70, 100] 如果欄位的值在 0 到 100 之間)，最大的值應該要大於或等於欄位中的最大值，否則也會自動被加到最後。
- 'equal_interval' # 需要提供想要分幾組
- 'quantile' # 需要提供切點的數量 (例如 4 則會產生 .25,.50,.75, 1.)，或是預設的分幾層的列表, 例如 [.25, .50, .75, 1.]。
- 'standard_deviation' # 必須提供要分幾組, 若 len(alist)%2==0, 則最初的平均值也會放在這裏面。
- 'natural_break' # 必須提供切點的數量
- 'head_tail_break' # 必須提供切點數量, 已進行簡化，以讓分組的數量可以被控制。

