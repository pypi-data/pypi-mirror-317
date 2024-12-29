import textwrap
from tests.example_data import *
from hw2_fedaniil.table import generate_latex_table

def test_simple_table():
    latex_table = generate_latex_table(example_table)
    assert example_table_str == latex_table[:-1]

def test_table_with_custom_spread():
    example_data = [["head 1", "head 2", "head 3"]]
    example_spread = [0.5, 0.25, 0.25]

    expected_table = textwrap.dedent(r"""
    \begin{table}[h]
        \centering
        \begin{tabular}{|p{0.5\linewidth}|p{0.25\linewidth}|p{0.25\linewidth}|}
            \hline
            head 1 & head 2 & head 3 \\ \hline
        \end{tabular}
    \end{table}
    """).lstrip()

    latex_table = generate_latex_table(example_data, example_spread)
    print(latex_table)
    assert expected_table == latex_table
