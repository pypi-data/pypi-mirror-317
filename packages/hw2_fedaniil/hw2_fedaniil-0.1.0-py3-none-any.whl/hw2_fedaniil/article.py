import textwrap

def generate_latex_article(preamble: str, document: str) -> str:
    """
    Generates LaTeX article with specified preamble (placed after documentclass) and document
    (placed after \\begin{document}).
    """
    return "\\documentclass{article}\n\n" + preamble + "\n\\begin{document}\n\n" + document + "\n\\end{document}"

