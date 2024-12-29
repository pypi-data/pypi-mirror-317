from typing import List

def generate_latex_usepackage(packages: List[str]) -> str:
    """
    Generates LaTeX preamble snippet to use a list of packages
    """
    return "\n".join(r"\usepackage{" + p + "}" for p in packages) + "\n"

