from numpy import nan

from .drop_dataframe_slice_greedily import drop_dataframe_slice_greedily


def clean_and_write_dataframe_to_tsv(dataframe, index_name, tsv_file_path):

    assert not dataframe.index.hasnans

    assert not dataframe.columns.hasnans

    assert not dataframe.index.has_duplicates

    assert not dataframe.columns.has_duplicates

    dataframe = dataframe.fillna(nan)

    dataframe = drop_dataframe_slice_greedily(dataframe, min_n_not_na_unique_value=1)

    dataframe = dataframe.sort_index().sort_index(axis=1)

    dataframe.index.name = index_name

    dataframe.to_csv(tsv_file_path, sep="\t")

    return dataframe
