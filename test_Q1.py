import pandas as pd

import Q1 as Q1

def test_fn():
    dfs={'oztour':Q1.oztour,
         'PoT':Q1.PoT,
         'State':Q1.State,
         'corr_mat':Q1.corr_mat,
         'PoT_State_By_Year':Q1.PoT_State_By_Year}

    for df in dfs.keys():
        df_chk = pd.read_hdf('Tourism.h5',df)
        assert (df_chk.index.sort_values() == dfs[df].index.sort_values()).all(), 'Index not set correctly: ' + df
        assert (df_chk.columns.sort_values() == dfs[df].columns.sort_values()).all(), 'Columns not set correctly: '+ df
        assert (df_chk.sort_index(axis=0).sort_index(axis=1).values == dfs[df].sort_index(axis=0).sort_index(axis=1).values).all(), \
                                                                                'Values incorrect: ' + df