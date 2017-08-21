 # -*- coding: utf-8 -*-


def prepare_map(ax, map_context=None, background_colour=None, xlim=None, ylim=None, show_xy=False):

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
