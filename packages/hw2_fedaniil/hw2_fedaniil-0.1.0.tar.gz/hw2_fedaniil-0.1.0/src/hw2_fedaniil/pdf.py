import subprocess
import os
import shutil

def generate_latex_pdf(latex: str, output_path: str = "out.pdf"):
    os.makedirs("tmp", exist_ok=True)
    os.chdir("tmp")
    with open("out.tex", "w") as f:
        print(latex, file=f)
    subprocess.run(["pdflatex", "out.tex"])
    os.chdir("..")
    os.rename(os.path.join("tmp", "out.pdf"), output_path)
    shutil.rmtree("tmp")

