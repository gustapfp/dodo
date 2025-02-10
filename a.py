import matplotlib
from pylatex import Document, Figure, NoEscape, Section
import matplotlib.pyplot as plt  # noqa

matplotlib.use("Agg")  # Not to use X server. For TravisCI.

def main(fname, width, *args, **kwargs):
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options)

    doc.append("Introduction.")

    with doc.create(Section("I am a section")):
        doc.append("Take a look at this beautiful plot:")

        # Save the plot to an image file first
        plot_filename = "plot_image.png"
        plt.savefig(plot_filename, *args, **kwargs)

        with doc.create(Figure(position="htbp")) as plot:
            # Add the image from the file
            plot.add_image(plot_filename, width=NoEscape(width))
            plot.add_caption("I am a caption.")

        doc.append("Created using matplotlib.")

    doc.append("Conclusion.")

    # Generate the PDF
    doc.generate_pdf(clean_tex=False, compiler='pdflatex')



if __name__ == "__main__":
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]

    plt.plot(x, y)

    # Generate PDF with plot and LaTeX
    main("matplotlib_ex-dpi", r"1\textwidth", dpi=300)
    main("matplotlib_ex-facecolor", r"0.5\textwidth", facecolor="b")
