import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import base64
from jinja2 import Template
import os
import pkg_resources
from datetime import datetime


class Evaluator:
    def __init__(self, filler_value):
        self.filler_value = filler_value

    def boxplot(self, scores, filename):
        filtered_scores = {
            model: [score for score in scores_list if score != self.filler_value]
            for model, scores_list in scores.items()
        }

        model_names = filtered_scores.keys()
        model_scores = filtered_scores.values()
        plt.figure(figsize=(14, 7))
        sns.set_theme(style="whitegrid")

        palette = sns.color_palette("pastel", len(model_names))

        box = plt.boxplot(
            model_scores,
            labels=model_names,
            patch_artist=True,
            medianprops={"color": "black", "linewidth": 2},
            whiskerprops={"color": "gray", "linewidth": 1.5},
            capprops={"color": "gray", "linewidth": 1.5},
            flierprops={"marker": "o", "color": "gray", "alpha": 0.7},
        )

        for patch, color in zip(box["boxes"], palette):
            patch.set_facecolor(color)

        plt.grid(axis="y", linestyle="--", alpha=0.7)

        plt.title("Model performance", fontsize=16, fontweight="bold", pad=20)
        plt.xlabel("Models", fontsize=14, labelpad=10)
        plt.ylabel("Score", fontsize=14, labelpad=10)
        plt.figtext(
            0.067,
            -0.005,
            "Algorithms that failed to cluster the data\nare excluded from the plot",
            ha="left",
            fontsize=10,
        )
        plt.tight_layout()
        plt.savefig(filename, format="png", bbox_inches="tight")

    def cumulative_plot(self, scores, filename):
        filtered_scores = {
            model: [
                (i + 1, score)
                for i, score in enumerate(scores_list)
                if score != self.filler_value
            ]
            for model, scores_list in scores.items()
        }

        func = min if self.filler_value == 999999 else max
        cumulative_best_scores = {
            model: [
                func(score for _, score in filtered_scores[model][: i + 1])
                for i in range(len(filtered_scores[model]))
            ]
            for model in filtered_scores
        }

        plt.figure(figsize=(14, 7))
        sns.set_theme(style="whitegrid")

        for model, cumulative_scores in cumulative_best_scores.items():
            plt.plot(
                range(1, len(cumulative_scores) + 1),
                cumulative_scores,
                label=model,
                marker="o",
                linewidth=2,
            )

        plt.title(
            "Best Performance Over Iterations", fontsize=16, fontweight="bold", pad=20
        )
        plt.xlabel("Iteration", fontsize=14, labelpad=10)
        plt.ylabel("Best Score", fontsize=14, labelpad=10)
        plt.xticks(
            sorted(set(x for values in filtered_scores.values() for x, _ in values))
        )
        plt.legend(title="Models", loc="lower right", fontsize=12, frameon=True)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.figtext(
            0.067,
            -0.005,
            "Algorithms that failed to cluster the data\nare excluded from the plot",
            ha="left",
            fontsize=10,
        )
        if self.filler_value == 999999:
            plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(filename, format="png", bbox_inches="tight")

    def clusters_plot(self, best_model, data, filename):
        labels = best_model.fit_predict(data)
        plt.figure(figsize=(14, 7))
        if data.shape[1] == 2:
            plot_data = data
            x_label, y_label = "Feature 1", "Feature 2"
            title = "Cluster Plot"
        else:
            pca = PCA(n_components=2)
            plot_data = pca.fit_transform(data)
            x_label, y_label = "Principal Component 1", "Principal Component 2"
            title = "Cluster Plot (PCA)"

        sns.scatterplot(
            x=plot_data[:, 0], y=plot_data[:, 1], hue=labels, palette="turbo"
        )
        plt.title(title, fontsize=16, fontweight="bold", pad=20)
        plt.xlabel(x_label, fontsize=14, labelpad=10)
        plt.ylabel(y_label, fontsize=14, labelpad=10)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename, format="png", bbox_inches="tight")

    def evaluate(self, scores, report, best_model, data):
        if not os.path.exists("clustermatic_report"):
            os.makedirs("clustermatic_report")
        boxplot_file = "clustermatic_report/boxplot.png"
        cumulative_file = "clustermatic_report/cumulative.png"
        cluster_file = "clustermatic_report/clusters.png"
        logo_path = pkg_resources.resource_filename(__name__, "auxiliary/header.png")

        print(report)
        self.boxplot(scores, boxplot_file)
        self.cumulative_plot(scores, cumulative_file)
        self.clusters_plot(best_model, data, cluster_file)

        def image_to_base64(filepath):
            with open(filepath, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")

        with open(
            pkg_resources.resource_filename(__name__, "auxiliary/report_template.html"),
            "r",
        ) as file:
            html_template = Template(file.read())

        html_content = html_template.render(
            logo=image_to_base64(logo_path),
            report=report,
            boxplot=image_to_base64(boxplot_file),
            cumulative=image_to_base64(cumulative_file),
            cluster=image_to_base64(cluster_file),
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"clustermatic_report/report_{timestamp}.html"
        with open(report_filename, "w") as f:
            f.write(html_content)
