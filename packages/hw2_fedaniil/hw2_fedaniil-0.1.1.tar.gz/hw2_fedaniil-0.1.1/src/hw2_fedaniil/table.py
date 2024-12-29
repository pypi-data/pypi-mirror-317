import textwrap
from typing import List, Optional


# I try to be concise, so no error handling or other fluff
def generate_latex_table(data: List[List[str]], spread: Optional[List[int]] = None) -> str:
    """
    Generates LaTeX snippet of a table made from fixed size NxM double-dimensional list.
    Table width is \\linewidth, by default spread evenly across columns, but this
    can be overriden by passing a list of M custom coefficients `spread`.
    """
    cols = len(data[0])
    if not spread:
        spread = [1. / cols] * cols
    return (textwrap.dedent("""\
        \\begin{table}[h]
            \\centering
            \\begin{tabular}{|""" + "|".join(f"p{{{c}\\linewidth}}" for c in spread) + """|}
                \\hline
        """) + 
            " \\\\ \\hline\n".join(" " * 8 + " & ".join(row) for row in data + ['']).rstrip() +
        textwrap.dedent(f"""
            \\end{{tabular}}
        \\end{{table}}
        """)
    )

