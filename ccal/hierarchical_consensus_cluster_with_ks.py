from os.path import join

from numpy import sort
from pandas import DataFrame, Index, concat
from scipy.spatial.distance import pdist, squareform

from .call_function_with_multiprocess import call_function_with_multiprocess
from .establish_path import establish_path
from .hierarchical_consensus_cluster import hierarchical_consensus_cluster
from .plot_and_save import plot_and_save
from .plot_heat_map import plot_heat_map
from .RANDOM_SEED import RANDOM_SEED


def hierarchical_consensus_cluster_with_ks(
    dataframe,
    ks,
    axis,
    n_job=1,
    distance__element_x_element=None,
    distance_function="euclidean",
    n_clustering=10,
    random_seed=RANDOM_SEED,
    linkage_method="ward",
    plot_dataframe=True,
    directory_path=None,
):

    if directory_path is None:

        k_directory_paths = tuple(None for k in ks)

    else:

        k_directory_paths = tuple(join(directory_path, str(k)) for k in ks)

        for k_directory_path in k_directory_paths:

            establish_path(k_directory_path, "directory")

    k_return = {}

    if axis == 1:

        dataframe = dataframe.T

    if distance__element_x_element is None:

        print(
            "Computing distance__element_x_element distance with {} ...".format(
                distance_function
            )
        )

        distance__element_x_element = DataFrame(
            squareform(pdist(dataframe.values, distance_function)),
            index=dataframe.index,
            columns=dataframe.index,
        )

        if directory_path is not None:

            distance__element_x_element.to_csv(
                join(directory_path, "distance.element_x_element.tsv"), sep="\t"
            )

    if axis == 1:

        dataframe = dataframe.T

    for (k, (element_cluster, element_cluster__ccc)) in zip(
        ks,
        call_function_with_multiprocess(
            hierarchical_consensus_cluster,
            (
                (
                    dataframe,
                    k,
                    axis,
                    distance__element_x_element,
                    None,
                    n_clustering,
                    random_seed,
                    linkage_method,
                    plot_dataframe,
                    k_directory_path,
                )
                for k, k_directory_path in zip(ks, k_directory_paths)
            ),
            n_job=n_job,
        ),
    ):

        k_return["K{}".format(k)] = {
            "element_cluster": element_cluster,
            "element_cluster.ccc": element_cluster__ccc,
        }

    keys = Index(("K{}".format(k) for k in ks), name="K")

    file_name = "ccc.html"

    if directory_path is None:

        html_file_path = None

    else:

        html_file_path = join(directory_path, file_name)

    plot_and_save(
        {
            "layout": {
                "title": {"text": "HCC Cophenetic Correlation Coefficient"},
                "xaxis": {"title": "K"},
                "yaxis": {"title": "CCC"},
            },
            "data": [
                {
                    "type": "scatter",
                    "x": ks,
                    "y": tuple(k_return[key]["element_cluster.ccc"] for key in keys),
                    "mode": "lines+markers",
                    "marker": {"color": "#20d9ba"},
                }
            ],
        },
        html_file_path,
    )

    k_x_element = concat([k_return[key]["element_cluster"] for key in keys], axis=1).T

    k_x_element.index = keys

    if directory_path is not None:

        k_x_element.to_csv(join(directory_path, "k_x_element.tsv"), sep="\t")

    if plot_dataframe:

        file_name = "k_x_element.cluster_distribution.html"

        if directory_path is None:

            html_file_path = None

        else:

            html_file_path = join(directory_path, file_name)

        plot_heat_map(
            DataFrame(sort(k_x_element.values, axis=1), index=keys),
            title="HCC Cluster Distribution",
            xaxis_title="Element",
            yaxis_title=k_x_element.index.name,
            html_file_path=html_file_path,
        )

    return k_return
