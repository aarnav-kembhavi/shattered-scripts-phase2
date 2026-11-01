"""Render E1 figures (F1, F1b, F1c) from results/e01_cost/ into paper2/figures/."""
from shattered.plots.e01 import all_figures

if __name__ == "__main__":
    for p in all_figures():
        print(p)
