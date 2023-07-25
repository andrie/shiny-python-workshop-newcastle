from shiny import App, render, ui, reactive
import pandas as pd
from plotnine import ggplot, geom_density, aes, theme_light, geom_point, stat_smooth
from pathlib import Path
from plots import scatter_plot, dist_plot

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider(
                "mass",
                "Mass",
                2000,
                8000,
                6000,
            ),
            ui.input_checkbox("smoother", "Add Smoother"),
        ),
        ui.panel_main(
            ui.output_plot(id="scatter"),
            ui.output_plot(id="mass_distribution"),
        ),
    )
)


def server(input, output, session):
    @output
    @render.plot
    def mass_distribution():
        filt_df = penguins.copy()
        filt_df = filt_df.loc[filt_df["Body Mass (g)"] < input.mass()]
        return dist_plot(filt_df)

    @output
    @render.plot
    def scatter():
        filt_df = penguins.copy()
        filt_df = filt_df.loc[filt_df["Body Mass (g)"] < input.mass()]
        return scatter_plot(filt_df, input.smoother())


app = App(app_ui, server)