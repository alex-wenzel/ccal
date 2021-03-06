from numpy import full, nan
from pandas import DataFrame, concat

from .call_function_with_multiprocess import call_function_with_multiprocess
from .single_sample_gsea import single_sample_gsea
from .split_dataframe import split_dataframe


def _single_sample_gseas(gene_x_sample, gene_sets, statistic):

    print("Running single-sample GSEA with {} gene sets ...".format(gene_sets.shape[0]))

    score__gene_set_x_sample = full((gene_sets.shape[0], gene_x_sample.shape[1]), nan)

    for sample_index, (sample_name, gene_score) in enumerate(gene_x_sample.items()):

        for gene_set_index, (gene_set_name, gene_set_genes) in enumerate(
            gene_sets.iterrows()
        ):

            score__gene_set_x_sample[gene_set_index, sample_index] = single_sample_gsea(
                gene_score, gene_set_genes, statistic=statistic, plot=False
            )

    score__gene_set_x_sample = DataFrame(
        score__gene_set_x_sample, index=gene_sets.index, columns=gene_x_sample.columns
    )

    return score__gene_set_x_sample


def single_sample_gseas(
    gene_x_sample, gene_sets, statistic="ks", n_job=1, file_path=None
):

    score__gene_set_x_sample = concat(
        call_function_with_multiprocess(
            _single_sample_gseas,
            (
                (gene_x_sample, gene_sets_, statistic)
                for gene_sets_ in split_dataframe(
                    gene_sets, 0, min(gene_sets.shape[0], n_job)
                )
            ),
            n_job,
        )
    )

    if file_path is not None:

        score__gene_set_x_sample.to_csv(file_path, sep="\t")

    return score__gene_set_x_sample
