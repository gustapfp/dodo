from report.models import (
    ONAFormAnswered,
    FormSubsectionAnswered,
    FormSectionAnswered,
    QuestionAnswer,
    ONAFormDistribution
)
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import pandas as pd
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import QuerySet, Q
from reportlab.platypus import Image
from reportlab.platypus import Table, TableStyle, PageBreak
from django.forms.models import model_to_dict

import matplotlib.dates as mdates

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
        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()  # Close the figure to free memory
        buf.seek(0)
        return buf

    def plot_line_graph_from_queryset(self, queryset, title):
        # Define the hard-coded colors from the Set1 palette
        colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#FF7F00']  # Set1 colors: red, blue, green, orange

        # Prepare data containers
        dates = []
        conforme = []
        nao_conforme = []
        parcial_conforme = []
        supera = []
  

        # Collect data from the queryset
        for record in queryset:
            dates.append(record.date)
            distribution = self.awnser_distribution_by_percentage(record.ona_answer_total_distribution)
            conforme.append(distribution.get('conforme', 0))
            nao_conforme.append(distribution.get('não conforme', 0))
            parcial_conforme.append(distribution.get('parcial conforme', 0))
            supera.append(distribution.get('supera', 0))


        # Create a DataFrame from the data
        df = pd.DataFrame({
            "Date": dates,
            "Conforme": conforme,
            "Não conforme": nao_conforme,
            "Parcial conforme": parcial_conforme,
            "Supera": supera,

        })

        # Set up the figure
        plt.figure(figsize=(12, 6))

        # Plot each category as a line with dots at the data points
        plt.plot(df['Date'], df['Conforme'], label='Conforme', marker='o', linestyle='-', color=colors[1])
        plt.plot(df['Date'], df['Não conforme'], label='Não conforme', marker='o', linestyle='-', color=colors[0])
        plt.plot(df['Date'], df['Parcial conforme'], label='Parcial conforme', marker='o', linestyle='-', color=colors[2])
        plt.plot(df['Date'], df['Supera'], label='Supera', marker='o', linestyle='-', color=colors[3])

        # Customize the plot
        plt.title(title, fontsize=16)
        plt.xlabel('Data', fontsize=14)
        plt.ylabel('Quantidade de Respostas', fontsize=14)



        # Set the x-axis ticks to only show the dates where data exists
        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())  # Optional: to show ticks for each week
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))

        # Set the x-ticks to only display the dates in the dataset
        plt.xticks(df['Date'], rotation=45)

        plt.grid(True)

        # Create custom legend handles
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[i], markersize=10, label=status.capitalize())
                for i, status in enumerate(['supera', 'conforme', 'parcial conforme', 'não conforme'])]

        # Add the custom legend
        plt.legend(handles=handles, title='Categorias', loc='upper right')

        # Show the plot
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
        print(answer_distribution)
        total = sum(answer_distribution.values())
        for key, value in answer_distribution.items():
            answer_distribution[key] = round((value / total) * 100, 2)

        return answer_distribution

    def sections_distribution_by_percentage(self, sections_distribution: dict) -> dict:
        # For each section, apply the answer distribution function

        for key, value in sections_distribution.items():
            sections_distribution[key] = self.awnser_distribution_by_percentage(value)

        return sections_distribution

class PDFReportGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename=f"{filename}.pdf", 
            pagesize=letter
        )
        self.story = []  # This will hold the content of the PDF
        self.metrics = MetricsCalculator()
        self.graphs = GraphsGenerator()

    def create_pdf_report_for_subsection(self, evaluator_name: str, answers: ONAFormAnswered):
        # Add title to the PDF
        self.add_title(evaluator_name)

        # Get metrics for the form
        metrics = self.metrics.get_ona_form_average_distribution(ona_form=answers)

        # Add the plot image for the form distribution
        form_distribution_img = self.graphs.plot_bar_plot(
            data=metrics["ONA answer Distribution"],
            title="Distribuição das Respostas no formulario",
        )
        
        # Insert the image into the PDF
        self.insert_image_center(image=form_distribution_img)

        # Display answers with comments
        self.display_answers_with_comments(questions_answers=metrics["Answers with comments"])

        # Build the PDF
        self.doc.build(self.story)

    def add_title(self, evaluator_name: str) -> None:
        title = f"Relatório de Preenchimento do Formulário por {evaluator_name}"
        styles = getSampleStyleSheet()
        title_paragraph = Paragraph(title, styles['Title'])
        self.story.append(title_paragraph)

    def display_answers_with_comments(self, questions_answers):
        self.story.append(PageBreak())
        styles = getSampleStyleSheet()

    
        for question in questions_answers:
            data = []

            # Add header row (with column names)
            header = ['Descrição da Questão', 'Core', "Resposta", "Comentario"]
            data.append(header)
            page_width, page_height = letter
            left_margin, right_margin = 4 , 4   
            table_width = page_width - left_margin - right_margin
        
            question_desc = f"{question.question.description}"
            core = "Sim" if question.question.core else "Não"
            core_info = f"{core}"
            answer_info = f"{question.answer}"
            comment_info = f"{question.comment}"

            
            row = [
                Paragraph(question_desc, styles['Normal']),
                Paragraph(core_info, styles['Normal']),
                Paragraph(answer_info, styles['Normal']),
                Paragraph(comment_info, styles['Normal'])
            ]
            data.append(row)
            col_widths = [table_width * 0.20, table_width * 0.20, table_width * 0.20, table_width * 0.20]
        
            table = Table(data, colWidths=col_widths, spaceAfter=20) 
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  
                ('BACKGROUND', (0, 0), (-1, 0), colors.blue), 
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), 
                ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'), 
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12), 
                ('TOPPADDING', (0, 1), (-1, -1), 8),  
                ('LEFTPADDING', (0, 0), (-1, -1), 5), 
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                # ('SPACEAFTER', (0, 0), (-1, -1), 50)
            ]))

            # Add the table to the story (content of the PDF)
            self.story.append(table)
            self.story.append(Paragraph("<br />", styles['Normal']))
    def insert_image_center(self, image: BytesIO) -> None:
        # The width and height for the image in the PDF
        img_width, img_height = 400, 400
     
        
        # Use the Image flowable to insert the image into the story
        img = Image(image, width=img_width, height=img_height)
        img.hAlign = 'CENTER'  # This centers the image in the PDF
        
        # Add the image flowable to the story
        self.story.append(img)

class PowerPointReportGenerator:
    def __init__(self):
        self.template_ona_path = "report/helpers/template-ona-report.pptx"
        self.section_indexes = {
            "1 SEÇÃO - GESTÃO ORGANIZACIONAL": 1,
            "2 SEÇÃO - ATENÇÃO AO PACIENTE": 4,
            "3 SEÇÃO - DIAGNÓSTICO E TERAPÊUTICA": 7,
            "4 SEÇÃO - GESTÃO DE APOIO": 10,
        }
        self.presentation = Presentation(self.template_ona_path)
        self.graphs = GraphsGenerator()

    def insert_plot_image_in_slide(self, image_buffer, slide_index, image_type):
        left, top, width, height = self.generate_images_coords(image_type)
        slide = self.presentation.slides[slide_index]
        slide.shapes.add_picture(image_buffer, left, top, width, height)
        return self.presentation

    def generate_images_coords(self, image_type):
        
        left = Inches(1.5)
        top = Inches(1.3)
        width = Inches(10)
        height = Inches(6)
        return left, top, width, height

    def add_section_images(self, sections_data):
        for section, resuls in sections_data.items():
            bar_plot_img = self.graphs.plot_bar_plot(resuls, section)
            section = section.strip()
            
            slide_index = self.section_indexes[section]
 
            prs = self.insert_plot_image_in_slide(bar_plot_img, slide_index, "section")
        return prs

    def add_subsection_images(self, subsection_data):
        for subsection, results in subsection_data.items():
            slide_index = self.section_indexes[subsection] + 2
            if slide_index == 3:
                grouped_bar_img = self.graphs.plot_grouped_bar_split_section_1(
                    results, subsection
                )
            elif slide_index == 6:
                grouped_bar_img = self.graphs.plot_grouped_bar_split_section_2(
                    results, subsection
                )
            else:
                grouped_bar_img = self.graphs.plot_grouped_bar(results, subsection)
            prs = self.insert_plot_image_in_slide(
                grouped_bar_img, slide_index, "subsection"
            )
        return prs

    def add_plot_line_image(self, hospital):
        queryset = ONAFormDistribution.objects.filter(
            hospital=hospital
        )
        self.graphs.plot_line_graph_from_queryset(
            queryset=queryset,
            title="Evolução das Respostas"
        )
        plot_line_img = self.graphs.plot_line_graph_from_queryset(
            queryset=queryset,
            title="Evolução das Respostas"
        )
        prs = self.insert_plot_image_in_slide(
            image_buffer=plot_line_img,
            slide_index=13,
            image_type="plot-line"
        )
        return prs


        

    def make_report(self, data, report_name, hospital):
        subsections = data["Subsections Distribution"]
        sections = data["Sections Distribution"]
        self.add_section_images(sections)
        self.add_subsection_images(subsections)
        self.add_plot_line_image(hospital)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"report/presentations_report/{report_name}_{timestamp}.pptx"
        self.presentation.save(path)
        # self.send_email(path, "gustavopfpereira30@gmail.com")

    def send_email(self, report_path, recipient_email):
        subject = "Generated Report"
        body = "Please find attached the generated report."

        # Create the email message
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email="gustavopfpereira30@gmail.com",  # Use the sender email from settings
            to=["gustavopfpereira30@gmail.com"],
        )

        # Attach the report file
        with open(report_path, "rb") as file:
            email.attach_file(report_path)

        # Send the email
        try:
            email.send()  # This sends the email using Django's configured email backend
            print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Error sending email: {e}")


class MetricsCalculator:
    def __get_subsection_questions(
        self, subsection: FormSubsectionAnswered
    ) -> list[QuestionAnswer]:
        leve1_questions = subsection.answered_questions_level_1.all()
        level2_questions = subsection.answered_questions_level_2.all()

        questions_answers = leve1_questions.union(level2_questions)
        return questions_answers

    def __get_questions_average_distribution(
        self, questions_list: list[QuestionAnswer]
    ) -> dict[str, int]:
        questions_answers = [question.answer for question in questions_list]
        answers_distribution = Counter(questions_answers)
        return answers_distribution

    def __get_subsection_average_distribution(
        self, subsection_questions: list[QuestionAnswer]
    ) -> dict[str, dict[str, int]]:
        subsection_distribution = self.__get_questions_average_distribution(
            questions_list=subsection_questions
        )
        return dict(subsection_distribution)

    def __get_section_and_subsection_answers_distribution(
        self, section: FormSectionAnswered
    ) -> dict[str, int]:
        subsections = section.answered_subsections.all()
   
        level3_questions = section.answered_questions_level_3.all()

        subsection_answers = level3_questions
        
        subsection_distribution = {}
        for subsction in subsections:
            subsection_title = subsction.form_subsection.subsection_title
            subsection_questions_level_1_and_level_2 = self.__get_subsection_questions(
                subsction
            )
            subsection_distribution[subsection_title] = (
                self.__get_subsection_average_distribution(
                    subsection_questions_level_1_and_level_2
                )
            )

            subsection_answers = subsection_answers.union(
                subsection_questions_level_1_and_level_2
            )
        subsection_answers_with_comments = subsection_answers
        section_distribution = self.__get_questions_average_distribution(
            subsection_answers
        )

        return section_distribution, subsection_distribution, subsection_answers_with_comments

    def __get_ona_form_total_metrics(
        self, distribution_by_section: dict
    ) -> dict[str, int]:
        total_counts = Counter()
        for section, counts in distribution_by_section.items():
            total_counts.update(counts)
        return dict(total_counts)

    def get_ona_form_average_distribution(
        self, ona_form: ONAFormAnswered
    ) -> dict[str, dict[str, int]]:
        sections = ona_form.answered_sections.all()

        distribution_by_section = {}
        distribution_by_subsections = {}
        for section in sections:
            section_name = section.form_section.section_title
            section_distribution, subsection_distribution, section_answers_with_comments = (
                self.__get_section_and_subsection_answers_distribution(section)
            )

            distribution_by_section[section_name] = dict(section_distribution)

            distribution_by_subsections[section_name] = dict(subsection_distribution)

        total_distribution = self.__get_ona_form_total_metrics(distribution_by_section)

        metrics = {
            "Subsections Distribution": distribution_by_subsections,
            "Sections Distribution": distribution_by_section,
            "ONA answer Distribution": total_distribution,
            "Answers with comments" : section_answers_with_comments
        }

        return metrics
    

    def create_unified_form_metrics(self, ona_form_queryset: QuerySet):
        combined_distribution = {
            'não conforme': 0,
            'parcial conforme': 0,
            'conforme': 0,
            'supera': 0
        }
        combined_sections_distribution = {}
        combined_subsections_distribution = {}
        for ona_form in ona_form_queryset:
        
            metrics = self.get_ona_form_average_distribution(ona_form)
            combined_distribution = self.update_combined_distribution(
                ona_answer_distribution=metrics['ONA answer Distribution'],
                combined_distribution=combined_distribution
            )
            combined_sections_distribution = self.update_combine_sections_distribution(
                sections_distribution=metrics["Sections Distribution"],
                combined_sections_distribution=combined_sections_distribution,
            )
            combined_subsections_distribution = self.update_combine_subsections_distribution(
                subsections_distribution_by_sections = metrics["Subsections Distribution"],
                combined_sections_distribution = combined_subsections_distribution
            )
        combined_metrics = {
            "Subsections Distribution": dict(sorted(combined_subsections_distribution.items())),
            "Sections Distribution": dict(sorted(combined_sections_distribution.items())),
            "ONA answer Distribution": dict(sorted(combined_distribution.items())),
        }
        return combined_metrics 
            
    def update_combined_distribution(self, ona_answer_distribution: dict, combined_distribution:dict) -> dict:
        for key, value in ona_answer_distribution.items():
            if key in combined_distribution:
                combined_distribution[key] += value
            else:
                combined_distribution[key] = value
        return combined_distribution
    
    def update_combine_sections_distribution(self,  sections_distribution:dict, combined_sections_distribution:dict):
        for section_name, distribution in sections_distribution.items():
            if section_name in combined_sections_distribution.keys():
                
                combined_sections_distribution[section_name] = dict(Counter(distribution) +Counter(combined_sections_distribution[section_name]))
            else:
                combined_sections_distribution[section_name] = distribution
        return combined_sections_distribution
    
    def update_combine_subsections_distribution(self, subsections_distribution_by_sections: dict, combined_sections_distribution: dict):
        for section_name, subsection_distribution in subsections_distribution_by_sections.items():
            if section_name in combined_sections_distribution:
                # If the section exists in the combined dictionary, update its subsections
                for subsection_name, distribution in subsection_distribution.items():
                    if subsection_name in combined_sections_distribution[section_name]:
                        # Use Counter to sum the values of matching subsections
                        combined_sections_distribution[section_name][subsection_name] = dict(
                            Counter(combined_sections_distribution[section_name][subsection_name]) + Counter(distribution)
                        )
                    else:
                        # If the subsection does not exist in the combined section, add it
                        combined_sections_distribution[section_name][subsection_name] = distribution
            else:
                # If the section does not exist in the combined dictionary, add it directly
                combined_sections_distribution[section_name] = subsection_distribution

        return combined_sections_distribution





