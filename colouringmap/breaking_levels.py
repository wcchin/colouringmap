 # -*- coding: utf-8 -*-

import numpy as np # percentile, ceil, mean, std
import jenkspy # jenk's natural break

def get_levels(alist, method='equal_interval', N=5, cuts=[], vmin=None, vmax=None):
    #assert N<=10, 'number of groups should be less than 10'
    methods_list = ['manual','equal_interval','quantile','standard_deviation','natural_break','head_tail_break'  ]
    #assert method in methods_list, "method not implemented."
    alist = [ float(i) for i in alist ]
    if method=='manual':
        level_list, cuts = manual(alist, cuts=cuts)
    elif method=='equal_interval':
        level_list, cuts = equal_interval(alist, vmin=vmin, vmax=vmax, N=N)
    elif method=='quantile':
        level_list, cuts = quantile(alist, N=N, cuts=cuts)
        ## the variable cuts is changed to values, not quartiles
    elif method=='standard_deviation':
        level_list, cuts = standard_deviation(alist, N=N)
    elif method=='natural_break':
        level_list, cuts = natural_break(alist, N=N)
    elif method=='head_tail_break':
        level_list, cuts = head_tail_break(alist, N=N)
    else:
        print 'method not implemented:', method
        level_list, cuts = None,None
        ## should change to raise Exception and exit
        ## should not return any things
    cuts2 = [min(alist)]+cuts
    return level_list, cuts2

def manual(alist, cuts):
    #assert len(cuts)>0, 'please check the list, should be more than 1 element'
    if max(cuts)<max(alist):
        cuts.append(max(alist))
    level_list = list_convert_to_level(alist, cuts)
    return level_list, cuts

def equal_interval(alist, vmin=None, vmax=None, N=5):
    amin = min(alist)
    amax = max(alist)
    cut = float(amax - amin) / N
    cuts = [ (c+1)*cut+amin for c in range(N) ]
    level_list = list_convert_to_level(alist, cuts)
    return level_list, cuts

def quantile(alist, N=4, cuts=[]):
    # to do: assert max(cuts) <=1
    if len(cuts)==0:
        cuts = []
        q = 1./N
        cuts = [ (i+1)*q for i in range(N) ]
    #assert max(cuts) <= 1., "cuts must be float number within 0.~1."
    vcuts = [ np.percentile(alist, c*100.) for c in cuts ]
    level_list = list_convert_to_level(alist, vcuts)
    return level_list, vcuts ## use vcuts instead of cuts

def standard_deviation(alist, N=5):
    #se = pd.Series(alist)
    miu = np.mean(alist, dtype=np.float64)#se.mean()
    std = np.std(alist, dtype=np.float64) #se.std()
    micro_cut = float(np.ceil(float(N)/2.))-1. # denominator of the std
    cuts1 = [ -(i+1.)/micro_cut for i in range(int(micro_cut)) ]
    cuts1 = sorted(cuts1)
    cuts2 = [ (i+1.)/micro_cut for i in range(int(micro_cut)) ]
    if N%2==0:
        cuts_middle = [ 0 ]
    else:
        cuts_middle = []
    cuts_both = cuts1 + cuts_middle + cuts2
    cuts_bothv = [ c*std + miu for c in cuts_both ]
    cuts_bothv.append(max(alist))
    level_list = list_convert_to_level(alist, cuts_bothv)
    return level_list, cuts_bothv

def natural_break(alist, N=5):
    cuts = jenkspy.jenks_breaks(alist, nb_class=N)
    cuts = cuts[1:]
    #print len(cuts)
    level_list = list_convert_to_level(alist, cuts)
    return level_list, cuts

def head_tail_break(alist, N=5):
    # simplified to return the exact number of groups
    # ori paper: https://arxiv.org/ftp/arxiv/papers/1209/1209.2801.pdf
    cuts = []
    alist2 = [ v for v in alist ] # copy.copy(alist)
    for i in range(N-1):
        miu = float(sum(alist2))/len(alist2)
        head = [ v for v in alist2 if v>miu ]
        cuts.append(miu)
        alist2 = head
    cuts.append(max(alist))
    level_list = list_convert_to_level(alist, cuts)
    return level_list, cuts

def list_convert_to_level(alist, cuts):
    level_list = []
    for a in alist:
        i = 0
        while (a>cuts[i]):
            i+=1
        level_list.append(i)
    return level_list

if __name__ == '__main__':
    import random
    print 'generated a list of random values'
    alist = [ float(random.randint(0,100)) for i in range(100) ]
    print alist
    """
    print 'tested equal interval'
    levels,cuts = get_levels(alist, N=5, method='equal_interval')
    print levels, cuts

    print 'test quantile'
    levels,cuts = get_levels(alist, N=4, method='quantile')
    print levels, cuts

    print 'tested head tail break'
    levels,cuts = get_levels(alist, N=6, method='head_tail_break')
    print levels, cuts

    print 'test natural break'
    levels,cuts = get_levels(alist, N=6, method='natural_break')
    print levels, cuts
    """

    print 'test standard deviation'
    levels,cuts = get_levels(alist, N=6, method='standard_deviation')
    print levels, cuts
