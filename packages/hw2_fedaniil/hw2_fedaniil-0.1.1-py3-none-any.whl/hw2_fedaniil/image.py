def generate_latex_image(image_path: str) -> str:
    """
    Generates LaTeX snippet to include the image at specified path with width=\\linewidth
    """
    return r"\includegraphics[width=\textwidth]{" + image_path + "}\n"

