import lzma
import pickle
from os.path import join
import pandas as pd
import matplotlib as mpl
import seaborn as sns

survey_folder = "sources"
schema_folder = "schemas"


def xzsave(obj, filename):
    """ compressed pickle save """
    with lzma.open(filename, "wb") as f:
        pickle.dump(obj, f)


def xzload(filename):
    """ compressed pickle load """
    with lzma.open(filename, "rb") as f:
        return pickle.loads(f.read())


def load(year, csvfile, skiprows):
    """
    load and standardise survey columns, and add survey year column
    year : (int) survey year
    csvfile : (string) csv file
    skiprows : (int) rows to skip
    """
    print(year, end=' ')
    fin = join(survey_folder, csvfile)
    schema = join(schema_folder, f"{year}.csv")
    names = pd.read_csv(schema, header=None)[0]
    df = pd.read_csv(
        fin,
        skiprows=skiprows,
        engine='python',  # utf-8 errors with default engine
        names=names,
        header=None
    )
    df['survey_year'] = year
    print(f"respondents: {df.shape[0]}, columns: {df.shape[1]}")
    return df


def prep_label_standardisation(dfs, cols, split=";"):
    """
    prepare dict for manual common labeling across datasets
    dfs : (list of dataframes) surveys
    cols : (list of strings) columns of interest
    split : (string) split multicategory string entries
    """
    print('{')
    for col in cols:
        unique = []
        for df in dfs:
            if col in df.columns and df[col].dtype == object:
                unique.extend(list(pd.unique(df[col].dropna())))
        unique = sorted(list(set(unique)))
        if split:
            unique = [u.split(';') for u in unique]
            unique = [v.strip() for s in unique for v in s]
            unique = sorted(list(set(unique)))
        print(f'    "{col}": {{')
        for u in unique:
            print(f'        "{u}" : ,')
        print("    },")
    print('}')


def stackplot(df, title, baseline='zero', cmap="mako", lw=0.5, ax=None):
    """ creates a stackplot with preferred defaults """
    if ax is None:
        fig, ax = mpl.pyplot.subplots()
    ax.stackplot(
        df.index,
        df.values.T,
        baseline=baseline,
        colors=sns.color_palette(cmap, df.shape[1]),
        labels=df.columns,
        edgecolor='k',
        linewidth=lw
    )
    ax.legend(frameon=True)
    ax.set_title(title)
    ax.set_xticks(range(2011,2021))
    ax.margins(0,0)
    return ax


def mpl_defs(width=1, height=1):
    """ set preferred default matplotlib settings and colours """
    c = [
        "#010595",
        "#0095FF",
        "#FF4500",
        "#00BE68",
        "#FF9000",
        "#484554",
        "#f24e7c",
        "#8938a8",
        "#197c5d",
        "#60dd49",
        "#A50021",
    ]
    mpl.rcParams["font.sans-serif"] = "Helvetica"
    mpl.rcParams["mathtext.fontset"] = "custom"
    mpl.rcParams["mathtext.rm"] = "Helvetica"
    mpl.rcParams["mathtext.it"] = "Helvetica:italic"
    mpl.rcParams["mathtext.bf"] = "Helvetica:bold"
    mpl.rcParams["mathtext.sf"] = "Helvetica"
    mpl.rcParams["mathtext.tt"] = "Helvetica"
    mpl.rcParams["mathtext.cal"] = "Helvetica:italic"
    mpl.rcParams["figure.figsize"] = 3.375 * width, 2.8 * height
    mpl.rcParams["figure.constrained_layout.use"] = True
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=c)
    mpl.rcParams["figure.subplot.left"] = 0.12
    mpl.rcParams["figure.subplot.right"] = 0.98
    mpl.rcParams["figure.subplot.bottom"] = 0.10
    mpl.rcParams["figure.subplot.top"] = 0.98
    mpl.rcParams["figure.subplot.wspace"] = 0.2
    mpl.rcParams["figure.subplot.hspace"] = 0.2
    mpl.rcParams["savefig.dpi"] = 300
    mpl.rcParams["figure.dpi"] = 140
    mpl.rcParams["lines.markersize"] = 4.0
    mpl.rcParams["lines.linewidth"] = 0.75
    mpl.rcParams["hatch.linewidth"] = 0.1
    mpl.rcParams["font.size"] = 7.0
    mpl.rcParams["axes.labelsize"] = 7.0
    mpl.rcParams["axes.labelpad"] = 3.0
    mpl.rcParams["axes.titlesize"] = 7.0
    mpl.rcParams["axes.linewidth"] = 0.5
    mpl.rcParams["patch.linewidth"] = 0.5
    mpl.rcParams["xtick.top"] = True
    mpl.rcParams["ytick.right"] = True
    mpl.rcParams["xtick.direction"] = "in"
    mpl.rcParams["ytick.direction"] = "in"
    mpl.rcParams["xtick.labelsize"] = 7.0
    mpl.rcParams["ytick.labelsize"] = 7.0
    mpl.rcParams["xtick.major.size"] = 2.0
    mpl.rcParams["ytick.major.size"] = 2.0
    mpl.rcParams["xtick.minor.size"] = 1.5
    mpl.rcParams["ytick.minor.size"] = 1.5
    mpl.rcParams["xtick.major.width"] = 0.4
    mpl.rcParams["ytick.major.width"] = 0.4
    mpl.rcParams["xtick.minor.width"] = 0.4
    mpl.rcParams["ytick.minor.width"] = 0.4
    mpl.rcParams["legend.frameon"] = False
    mpl.rcParams["legend.fontsize"] = 6.0
    mpl.rcParams["legend.borderpad"] = 0.4
    mpl.rcParams["legend.handlelength"] = 1.2
    mpl.rcParams["legend.handletextpad"] = 0.6
    mpl.rcParams["legend.labelspacing"] = 0.4
    mpl.rcParams["legend.columnspacing"] = 1.2
    mpl.rcParams["grid.linewidth"] = 0.2

    return c
