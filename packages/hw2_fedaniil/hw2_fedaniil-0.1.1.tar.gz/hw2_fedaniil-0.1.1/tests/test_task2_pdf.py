import pytest
import subprocess
from tests.example_data import *
from hw2_fedaniil.image import generate_latex_image
from hw2_fedaniil.article import generate_latex_article
from hw2_fedaniil.preamble import generate_latex_usepackage
from hw2_fedaniil.table import generate_latex_table
from hw2_fedaniil.pdf import generate_latex_pdf

no_pdflatex = True
try:
    subprocess.run(["pdflatex", "--version"], shell=True)
    no_pdflatex = False
except:
    pass

@pytest.mark.skipif(no_pdflatex, reason="This test requires pdflatex installed in system")
def test_pdf_output():
    artifact_path = os.path.join(os.path.dirname(__file__), "..", "task_2_2.pdf")
    generate_latex_pdf(generate_latex_article(generate_latex_usepackage(["graphicx"]), generate_latex_table(example_table) + generate_latex_image(example_image)), artifact_path)

