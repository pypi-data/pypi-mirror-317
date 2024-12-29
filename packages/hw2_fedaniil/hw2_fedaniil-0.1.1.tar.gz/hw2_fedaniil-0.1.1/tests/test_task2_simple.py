import textwrap
import os
from tests.example_data import *
from hw2_fedaniil.image import generate_latex_image
from hw2_fedaniil.article import generate_latex_article
from hw2_fedaniil.preamble import generate_latex_usepackage
from hw2_fedaniil.table import generate_latex_table

def test_image_simple():
    assert r"\includegraphics[width=\textwidth]{path/to/image}" == generate_latex_image("path/to/image")[:-1]

def test_latex_usepackage():
    assert "\\usepackage{graphicx}\n\\usepackage{fontspec}\n" == generate_latex_usepackage(["graphicx", "fontspec"])

def test_article_simple():
    expected_article = textwrap.dedent(r"""
    \documentclass{article}

    \usepackage{graphicx}

    \begin{document}
    
    Test body
    
    \end{document}""").lstrip()

    assert expected_article == generate_latex_article(generate_latex_usepackage(["graphicx"]), "Test body\n")
    
def test_table_wtih_image():
    expected_article = textwrap.dedent("""\
    \\documentclass{article}

    \\usepackage{graphicx}

    \\begin{document}
    
    """) + example_table_str + "\n" + textwrap.dedent(f"""\
    \\includegraphics[width=\\textwidth]{{{os.path.join(os.path.dirname(__file__), "images", "1068070.png")}}}
    
    \\end{{document}}""").lstrip()

    assert expected_article == generate_latex_article(generate_latex_usepackage(["graphicx"]), generate_latex_table(example_table) + generate_latex_image(example_image))

