from plotly.io import write_image
from plotly.offline import iplot
from plotly.offline import plot as offline_plot
from plotly.plotly import plot as plotly_plot


def plot_and_save(figure, html_file_path, plotly_html_file_path=None):

    if "layout" in figure:

        figure["layout"].update({"autosize": True, "hovermode": "closest"})

        for axis in ("xaxis", "yaxis"):

            if axis in figure["layout"]:

                figure["layout"][axis].update({"automargin": True})

    config = {"editable": True}

    if html_file_path is not None:

        html_file_path = offline_plot(
            figure, filename=html_file_path, auto_open=False, config=config
        )

        write_image(figure, html_file_path.replace(".html", ".png"), scale=10)

    if plotly_html_file_path is not None:

        plotly_plot(
            figure,
            filename=plotly_html_file_path,
            file_opt="overwrite",
            auto_open=False,
        )

    iplot(figure, config=config)
