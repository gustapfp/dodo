from pptx import Presentation
from pptx.util import Inches
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO


class GraphsGenerator:
    def plot_bar_plot(self, data, title):
        data = self.awnser_distribution_by_percentage(data)

        colors = ["#E41A1C", "#377EB8", "#4DAF4A", "#FF7F00"]

        df = pd.DataFrame(list(data.items()), columns=["Status", "Percentage"])
        df["Status"] = df["Status"].str.capitalize()

        plt.figure(figsize=(10, 6))

        ax = sns.barplot(
            x="Status", y="Percentage", data=df, palette=colors, edgecolor="black"
        )

        plt.ylabel("Conformidade (%)")
        plt.xlabel("Respostas", labelpad=15)
        plt.title(title)

        plt.grid(True, axis="y", linestyle="--", alpha=0.7)

        plt.ylim(0, 100)

        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.1f}%",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                fontsize=12,
                color="black",
                fontweight="bold",
                xytext=(0, 10),
                textcoords="offset points",
            )

        colors = ax.patches

        handles = []
        categories = df["Status"].tolist()
        for color, status in zip(colors, categories):
            handles.append(
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor=color.get_facecolor(),
                    markersize=10,
                    label=status,
                )
            )

        plt.legend(handles=handles, title="Legenda")
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()  # Close the figure to free memory
        buf.seek(0)
        return buf

    def plot_grouped_bar(self, data, title):
        data = self.sections_distribution_by_percentage(data)
        colors = [
            "#E41A1C",
            "#377EB8",
            "#4DAF4A",
            "#FF7F00",
        ]  # Red, Blue, Green, Orange

        df = pd.DataFrame(data).T
        df = df[["conforme", "não conforme", "supera", "parcial conforme"]]
        df = df.reset_index()

        df_melted = df.melt(
            id_vars=["index"],
            value_vars=["supera", "conforme", "parcial conforme", "não conforme"],
            var_name="Categoria",
            value_name="Quantidade",
        )

        df_melted = df_melted.rename(columns={"index": "Setor"})

        plt.figure(figsize=(18, 6))

        sns.barplot(
            x="Setor",
            y="Quantidade",
            hue="Categoria",
            data=df_melted,
            palette=colors,
            edgecolor="black",
        )
        plt.grid(True, axis="y", linestyle="--", alpha=0.7)

        # Customize the plot
        plt.title(title, fontsize=16)
        plt.ylabel("Quantidade de Respostas")
        plt.xlabel("Seção")

        # Create custom legend handles using plt.Line2D with hard-coded colors
        handles = []
        categories = ["supera", "conforme", "parcial conforme", "não conforme"]

        # Iterate through the bars and create a custom legend entry for each
        for i, status in enumerate(categories):
            # Use the corresponding color from the hard-coded colors list
            color = colors[i]
            # Create the legend entry using a square marker ('o')
            handles.append(
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor=color,
                    markersize=10,
                    label=status.capitalize(),
                )
            )

        # Add the custom legend
        plt.legend(handles=handles, title="Categorias", loc="upper right")

        # Adjust layout for better spacing
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()  # Close the figure to free memory
        buf.seek(0)
        return buf

    def plot_grouped_bar_split_section_1(self, data, title):
        # Define the hard-coded colors from the Set1 palette
        colors = [
            "#E41A1C",
            "#377EB8",
            "#4DAF4A",
            "#FF7F00",
        ]  # Set1 colors: red, blue, green, orange

        # Convert the dictionary into a DataFrame
        df = pd.DataFrame(data).T  # Transpose to have sections as rows
        df = df[
            ["conforme", "não conforme", "supera", "parcial conforme"]
        ]  # Ensure correct column order
        df = df.reset_index()  # Reset the index to have a 'Setor' column for seaborn

        # Melt the dataframe for seaborn
        df_melted = df.melt(
            id_vars=["index"],
            value_vars=["supera", "conforme", "parcial conforme", "não conforme"],
            var_name="Categoria",
            value_name="Quantidade",
        )

        # Rename 'index' column to 'Setor'
        df_melted = df_melted.rename(columns={"index": "Setor"})

        # Split the dataset into two halves
        mid_point = len(df_melted["Setor"].unique()) // 2
        first_half = df_melted[df_melted["Setor"].isin(df["index"][:mid_point])]
        second_half = df_melted[df_melted["Setor"].isin(df["index"][mid_point:])]

        # Set up the figure with two subplots
        fig, axes = plt.subplots(2, 1, figsize=(15, 10), sharey=True)

        # First subplot
        sns.barplot(
            x="Setor",
            y="Quantidade",
            hue="Categoria",
            data=first_half,
            palette=colors,
            edgecolor="black",
            ax=axes[0],
        )
        axes[0].grid(True, axis="y", linestyle="--", alpha=0.7)
        axes[0].set_title(title + " (Parte 1)", fontsize=16)
        axes[0].set_ylabel("Quantidade de Respostas")
        axes[0].set_xlabel("Seção")

        # Second subplot
        sns.barplot(
            x="Setor",
            y="Quantidade",
            hue="Categoria",
            data=second_half,
            palette=colors,
            edgecolor="black",
            ax=axes[1],
        )
        axes[1].grid(True, axis="y", linestyle="--", alpha=0.7)
        axes[1].set_title(title + " (Parte 2)", fontsize=16)
        axes[1].set_ylabel("Quantidade de Respostas")
        axes[1].set_xlabel("Seção")

        # Create custom legend handles
        handles = [
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor=colors[i],
                markersize=10,
                label=status.capitalize(),
            )
            for i, status in enumerate(
                ["supera", "conforme", "parcial conforme", "não conforme"]
            )
        ]

        # Add the custom legend to the first plot only
        axes[0].legend(handles=handles, title="Legenda", loc="upper right")
        axes[1].legend(handles=handles, title="Legenda", loc="upper right")

        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()  # Close the figure to free memory
        buf.seek(0)
        return buf

    def plot_grouped_bar_split_section_2(self, data, title):
        # Define the hard-coded colors from the Set1 palette
        colors = [
            "#E41A1C",
            "#377EB8",
            "#4DAF4A",
            "#FF7F00",
        ]  # Set1 colors: red, blue, green, orange

        # Convert the dictionary into a DataFrame
        df = pd.DataFrame(data).T  # Transpose to have sections as rows
        df = df[
            ["conforme", "não conforme", "supera", "parcial conforme"]
        ]  # Ensure correct column order
        df = df.reset_index()  # Reset the index to have a 'Setor' column for seaborn

        # Melt the dataframe for seaborn
        df_melted = df.melt(
            id_vars=["index"],
            value_vars=["supera", "conforme", "parcial conforme", "não conforme"],
            var_name="Categoria",
            value_name="Quantidade",
        )

        # Rename 'index' column to 'Setor'
        df_melted = df_melted.rename(columns={"index": "Setor"})

        # Split the dataset into two halves
        first_point = len(df_melted["Setor"].unique()) // 3
        second_point = first_point * 2 + 1
        first_part = df_melted[df_melted["Setor"].isin(df["index"][:first_point])]
        second_part = df_melted[
            df_melted["Setor"].isin(df["index"][first_point:second_point])
        ]
        third_part = df_melted[df_melted["Setor"].isin(df["index"][second_point:])]

        # Set up the figure with two subplots
        fig, axes = plt.subplots(3, 1, figsize=(20, 10), sharey=True)

        # First subplot
        sns.barplot(
            x="Setor",
            y="Quantidade",
            hue="Categoria",
            data=first_part,
            palette=colors,
            edgecolor="black",
            ax=axes[0],
        )
        axes[0].grid(True, axis="y", linestyle="--", alpha=0.7)
        axes[0].set_title(title + " (Parte 1)", fontsize=16)
        axes[0].set_ylabel("Quantidade de Respostas")
        axes[0].set_xlabel("Seção")

        # Second subplot
        sns.barplot(
            x="Setor",
            y="Quantidade",
            hue="Categoria",
            data=second_part,
            palette=colors,
            edgecolor="black",
            ax=axes[1],
        )
        axes[1].grid(True, axis="y", linestyle="--", alpha=0.7)
        axes[1].set_title(title + " (Parte 2)", fontsize=16)
        axes[1].set_ylabel("Quantidade de Respostas")
        axes[1].set_xlabel("Seção")

        # Second subplot
        sns.barplot(
            x="Setor",
            y="Quantidade",
            hue="Categoria",
            data=third_part,
            palette=colors,
            edgecolor="black",
            ax=axes[2],
        )
        axes[2].grid(True, axis="y", linestyle="--", alpha=0.7)
        axes[2].set_title(title + " (Parte 2)", fontsize=16)
        axes[2].set_ylabel("Quantidade de Respostas")
        axes[2].set_xlabel("Seção")
        # Create custom legend handles
        handles = [
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor=colors[i],
                markersize=10,
                label=status.capitalize(),
            )
            for i, status in enumerate(
                ["supera", "conforme", "parcial conforme", "não conforme"]
            )
        ]

        # Add the custom legend to the first plot only
        axes[0].legend(handles=handles, title="Legenda", loc="upper right")
        axes[1].legend(handles=handles, title="Legenda", loc="upper right")
        axes[2].legend(handles=handles, title="Legenda", loc="upper right")

        # Adjust layout
        plt.tight_layout()
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()  # Close the figure to free memory
        buf.seek(0)
        return buf

    def awnser_distribution_by_percentage(self, answer_distribution: dict) -> dict:
        # Remove 'não aplicável' if it exists
        if "não aplicável" in answer_distribution.keys():
            del answer_distribution["não aplicável"]

        # Calculate the percentage distribution
        total = sum(answer_distribution.values())
        for key, value in answer_distribution.items():
            answer_distribution[key] = round((value / total) * 100, 2)

        return answer_distribution

    def sections_distribution_by_percentage(self, sections_distribution: dict) -> dict:
        # For each section, apply the answer distribution function
        for key, value in sections_distribution.items():
            sections_distribution[key] = self.awnser_distribution_by_percentage(value)

        return sections_distribution


class ReportGenerator:
    def __init__(self):
        self.template_ona_path = "report/helpers/template-ona-report.pptx"
        self.section_indexes = {
            "SEÇÃO 01 - GESTÃO ORGANIZACIONAL": 1,
            "SEÇÃO 02  - ATENÇÃO AO PACIENTE": 3,
            "SEÇÃO 03 - DIAGNÓSTICO E TERAPÊUTICA": 5,
            "SEÇÃO 04 - GESTÃO DE APOIO": 7,
        }
        self.presentation = Presentation(self.template_ona_path)
        self.graphs = GraphsGenerator()

    def insert_plot_image_in_slide(self, image_buffer, slide_index, image_type):
        left, top, width, height = self.generate_images_coords(image_type)
        slide = self.presentation.slides[slide_index]
        slide.shapes.add_picture(image_buffer, left, top, width, height)
        return self.presentation

    def generate_images_coords(self, image_type):
        if image_type == "section":
            left = Inches(5.5)
            top = Inches(1)
            width = Inches(7)
            height = Inches(5)
        else:
            left = Inches(1.5)
            top = Inches(1.3)
            width = Inches(10)
            height = Inches(6)
        return left, top, width, height

    def add_section_images(self, sections_data):
        for section, resuls in sections_data.items():
            bar_plot_img = self.graphs.plot_bar_plot(resuls, section)
            slide_index = self.section_indexes[section]
            prs = self.insert_plot_image_in_slide(bar_plot_img, slide_index, "section")
        return prs

    def add_subsection_images(self, subsection_data):
        for subsection, results in subsection_data.items():
            slide_index = self.section_indexes[subsection] + 1
            if slide_index == 2:
                grouped_bar_img = self.graphs.plot_grouped_bar_split_section_1(
                    results, subsection
                )
            elif slide_index == 4:
                grouped_bar_img = self.graphs.plot_grouped_bar_split_section_2(
                    results, subsection
                )
            else:
                grouped_bar_img = self.graphs.plot_grouped_bar(results, subsection)
            prs = self.insert_plot_image_in_slide(
                grouped_bar_img, slide_index, "subsection"
            )
        return prs

    def make_report(self, data, report_name):
        subsections = data["Subsections Distribution"]
        sections = data["Sections Distribution"]
        (self.add_section_images(sections),)
        self.add_subsection_images(subsections)
        self.presentation.save(report_name)


# Example usage:
if __name__ == "__main__":
    data = {
        "Subsections Distribution": {
            "SEÇÃO 01 - GESTÃO ORGANIZACIONAL": {
                "1.1 LIDERANÇA ORGANIZACIONAL": {
                    "conforme": 21,
                    "não aplicável": 10,
                    "não conforme": 6,
                    "supera": 5,
                    "parcial conforme": 3,
                },
                "1.2 GESTÃO DA QUALIDADE": {
                    "parcial conforme": 5,
                    "não conforme": 7,
                    "conforme": 14,
                    "não aplicável": 2,
                    "supera": 2,
                },
                "1.3 PREV. CONTROLE DE INFECÇÃO": {
                    "conforme": 15,
                    "não conforme": 7,
                    "supera": 2,
                    "não aplicável": 6,
                    "parcial conforme": 2,
                },
                "1.4 GESTÃO ADM FINANCEIRA": {
                    "conforme": 10,
                    "não aplicável": 5,
                    "não conforme": 3,
                    "supera": 2,
                },
                "1.5 GESTÃO DE PESSOAS": {
                    "conforme": 13,
                    "não conforme": 4,
                    "supera": 7,
                    "não aplicável": 5,
                    "parcial conforme": 2,
                },
                "1.6 GESTÃO DE SUPRIMENTOS": {
                    "não conforme": 9,
                    "conforme": 9,
                    "supera": 3,
                },
                "1.7 GESTÃO DA TEC. DA INF.": {
                    "não conforme": 8,
                    "parcial conforme": 3,
                    "supera": 3,
                    "conforme": 10,
                },
                "1.8 GESTÃO DO ACESSO": {
                    "conforme": 10,
                    "parcial conforme": 1,
                    "não conforme": 6,
                    "não aplicável": 3,
                    "supera": 1,
                },
                "1.9 GESTÃO DA SEGURANÇA": {
                    "conforme": 7,
                    "não conforme": 5,
                    "não aplicável": 2,
                    "supera": 5,
                    "parcial conforme": 1,
                },
                "1.10 GESTÃO DA COMUNICAÇÃO": {
                    "não conforme": 6,
                    "conforme": 9,
                    "não aplicável": 1,
                    "parcial conforme": 1,
                    "supera": 3,
                },
            },
            "SEÇÃO 02  - ATENÇÃO AO PACIENTE": {
                "2.1 INTERNAÇÃO": {
                    "não aplicável": 3,
                    "conforme": 15,
                    "não conforme": 10,
                    "parcial conforme": 7,
                    "supera": 2,
                },
                "2.2 ATENDIMENTO AMBULATORIAL": {
                    "supera": 3,
                    "conforme": 12,
                    "parcial conforme": 11,
                    "não conforme": 11,
                    "não aplicável": 2,
                },
                "2.3 ATENDIMENTO EMERGENCIAL": {
                    "não aplicável": 5,
                    "supera": 6,
                    "conforme": 15,
                    "não conforme": 6,
                    "parcial conforme": 5,
                },
                "2.4 ATENDIMENTO CIRÚRGICO": {
                    "conforme": 14,
                    "não conforme": 13,
                    "parcial conforme": 16,
                    "supera": 4,
                    "não aplicável": 2,
                },
                "2.5 ATENDIMENTO OBSTÉTRICO": {
                    "supera": 5,
                    "conforme": 15,
                    "parcial conforme": 23,
                    "não conforme": 11,
                },
                "2.6 ATENDIMENTO NEONATAL": {
                    "não conforme": 11,
                    "parcial conforme": 12,
                    "supera": 6,
                    "conforme": 11,
                    "não aplicável": 4,
                },
                "2.7 CUIDADOS INTENSIVOS": {
                    "não conforme": 6,
                    "parcial conforme": 13,
                    "conforme": 10,
                    "supera": 6,
                    "não aplicável": 3,
                },
                "2.8 ASSISTÊNCIA HEMOTERÁPICA": {
                    "parcial conforme": 24,
                    "não conforme": 19,
                    "conforme": 12,
                    "supera": 1,
                    "não aplicável": 8,
                },
                "2.9 ASSISTÊNCIA NEFROLÓGICA": {
                    "parcial conforme": 18,
                    "conforme": 15,
                    "não conforme": 10,
                    "supera": 1,
                    "não aplicável": 3,
                },
                "2.10 ASSISTÊNCIA ONCOLÓGICA": {
                    "parcial conforme": 17,
                    "não conforme": 13,
                    "não aplicável": 4,
                    "conforme": 12,
                    "supera": 2,
                },
                "2.11 RADIOTERAPIA": {
                    "parcial conforme": 24,
                    "conforme": 11,
                    "não conforme": 4,
                    "supera": 2,
                },
                "2.12 MED. HIPERBÁRICA": {
                    "conforme": 11,
                    "parcial conforme": 12,
                    "não aplicável": 3,
                    "não conforme": 8,
                    "supera": 2,
                },
                "2.13 ASSISTÊNCIA FARMACÊUTICA": {
                    "parcial conforme": 13,
                    "conforme": 18,
                    "supera": 6,
                    "não conforme": 7,
                },
                "2.14 ASSISTÊNCIA NUTRICIONAL ": {
                    "parcial conforme": 24,
                    "conforme": 19,
                    "não conforme": 15,
                    "supera": 2,
                    "não aplicável": 2,
                },
                "2.15 ATENDIMENTO OFTALMOLÓGICO": {
                    "parcial conforme": 21,
                    "conforme": 14,
                    "supera": 3,
                    "não aplicável": 5,
                    "não conforme": 13,
                },
                "2.16 ATEND. PRÉ HOSPITALAR": {
                    "parcial conforme": 15,
                    "conforme": 17,
                    "não conforme": 5,
                    "supera": 3,
                    "não aplicável": 1,
                },
                "2.17 ODONTOLOGIA": {
                    "conforme": 17,
                    "parcial conforme": 19,
                    "não conforme": 13,
                },
                "2.18 TELEMEDICINA": {
                    "não conforme": 13,
                    "conforme": 8,
                    "parcial conforme": 12,
                    "não aplicável": 2,
                    "supera": 1,
                },
                "2.19 ATENÇÃO PRIMÁRIA": {
                    "conforme": 28,
                    "não conforme": 9,
                    "supera": 7,
                    "parcial conforme": 10,
                },
                "2.20 ATENÇÃO DOMICILIAR": {
                    "conforme": 9,
                    "não conforme": 9,
                    "parcial conforme": 22,
                    "não aplicável": 1,
                },
            },
            "SEÇÃO 03 - DIAGNÓSTICO E TERAPÊUTICA": {
                "3.1 Análises clínicas": {
                    "conforme": 9,
                    "não conforme": 22,
                    "parcial conforme": 20,
                },
                "3.2 Anatomia Patológica e Citop": {
                    "conforme": 20,
                    "parcial conforme": 11,
                    "não conforme": 11,
                    "supera": 2,
                },
                "3.3 Met. Diagósticos. e Terap.": {
                    "conforme": 14,
                    "não conforme": 5,
                    "parcial conforme": 14,
                    "supera": 2,
                },
                "3.4 Diagósticos por imagem": {
                    "parcial conforme": 13,
                    "conforme": 15,
                    "não conforme": 9,
                    "não aplicável": 2,
                },
                "3.5 Medicina Nuclear": {
                    "conforme": 14,
                    "não conforme": 16,
                    "parcial conforme": 13,
                    "não aplicável": 5,
                    "supera": 2,
                },
                "3.6 Radiologia Interv.": {
                    "parcial conforme": 20,
                    "não aplicável": 2,
                    "não conforme": 14,
                    "conforme": 7,
                    "supera": 1,
                },
                "3.7 Mét. endoscópicos e vid.": {
                    "não aplicável": 3,
                    "parcial conforme": 14,
                    "conforme": 14,
                    "não conforme": 14,
                    "supera": 1,
                },
            },
            "SEÇÃO 04 - GESTÃO DE APOIO": {
                "4.1 Gestão de equipamentos": {
                    "parcial conforme": 13,
                    "conforme": 7,
                    "não conforme": 11,
                    "não aplicável": 2,
                },
                "4.2 Gestão de Infraestrutura": {
                    "parcial conforme": 6,
                    "não conforme": 7,
                    "conforme": 6,
                    "supera": 1,
                    "não aplicável": 1,
                },
                "4.3 Limpeza e Desinf. de superf": {
                    "conforme": 7,
                    "parcial conforme": 6,
                    "não conforme": 8,
                },
                "4.4 Process. de produtos ": {
                    "parcial conforme": 11,
                    "supera": 3,
                    "não conforme": 6,
                    "conforme": 12,
                    "não aplicável": 2,
                },
                "4.5 Process. de Roupas": {
                    "conforme": 11,
                    "parcial conforme": 12,
                    "supera": 1,
                    "não conforme": 3,
                },
            },
        },
        "Sections Distribution": {
            "SEÇÃO 01 - GESTÃO ORGANIZACIONAL": {
                "não aplicável": 37,
                "conforme": 125,
                "não conforme": 66,
                "supera": 36,
                "parcial conforme": 18,
            },
            "SEÇÃO 02  - ATENÇÃO AO PACIENTE": {
                "parcial conforme": 325,
                "não conforme": 209,
                "supera": 64,
                "conforme": 289,
                "não aplicável": 48,
            },
            "SEÇÃO 03 - DIAGNÓSTICO E TERAPÊUTICA": {
                "conforme": 96,
                "não conforme": 96,
                "parcial conforme": 108,
                "supera": 9,
                "não aplicável": 18,
            },
            "SEÇÃO 04 - GESTÃO DE APOIO": {
                "não conforme": 40,
                "parcial conforme": 55,
                "conforme": 49,
                "não aplicável": 5,
                "supera": 5,
            },
        },
        "ONA awnser Distribution": {
            "não aplicável": 108,
            "conforme": 559,
            "não conforme": 411,
            "supera": 114,
            "parcial conforme": 506,
        },
    }
    subsections = data["Subsections Distribution"]
    sections = data["Sections Distribution"]
    ona_awnser = data["ONA awnser Distribution"]
    # graph = GraphsGenerator()
    # bar_plot_img = graph.plot_bar_plot(sections['SEÇÃO 01 - GESTÃO ORGANIZACIONAL'], 'SEÇÃO 01 - GESTÃO ORGANIZACIONAL')

    rg = ReportGenerator()
    prs = rg.make_report(data, "TEST06.pptx")
