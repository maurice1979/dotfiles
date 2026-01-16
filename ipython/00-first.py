import os

# Data Analysis Essentials
try:
    import duckdb
    import numpy as np
    import pandas as pd

    # Configure Pandas for better terminal/notebook display
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", 100)
    pd.set_option("display.width", 1000)

    # Check if we are in a Jupyter environment for JupySQL
    try:
        from IPython import get_ipython

        shell = get_ipython()
        if shell:
            # Auto-load SQL magic for DuckDB
            shell.run_line_magic("load_ext", "sql")
            # Set JupySQL to use the DuckDB connection by default
            shell.run_line_magic("config", "SqlMagic.autopandas = True")
            shell.run_line_magic("config", "SqlMagic.feedback = False")
            shell.run_line_magic("config", "SqlMagic.displaycon = False")
    except Exception:
        pass

    print("🚀 Data Science environment ready (pd, np, duckdb loaded)")
except ImportError as e:
    print(f"⚠️  Startup import failed: {e}")


# Handy helper to see what's in the current dir
def ll():
    for file in sorted(os.listdir(".")):
        print(file)
