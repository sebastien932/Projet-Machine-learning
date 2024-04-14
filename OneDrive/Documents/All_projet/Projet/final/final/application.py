import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import webbrowser
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas.api.types import is_numeric_dtype
import locale
import matplotlib.colors as mcolors
import sys


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style()
        self.style.configure(
            "Custom.TFrame", background="darkred", margin=0, foreground="white"
        )

        self.title("Best Auto")
        self.notebook = ttk.Notebook(self, style="Custom.TFrame")
        self.tab1 = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.tab2 = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.tab3 = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(self.tab1, text="Tableau à filtre")
        self.notebook.add(self.tab2, text="Graphiques")
        self.notebook.add(self.tab3, text="Analyse descriptive")
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure_onglet1()
        self.configure_onglet2()
        self.configure_onglet3()
        self.protocol("WM_DELETE_WINDOW", self.quit_application)

    def configure_onglet1(self):
        self.onglet1_content = Onglet1Content(self.tab1)

    def configure_onglet2(self):
        self.onglet2_content = Onglet2Content(self.tab2)

    def configure_onglet3(self):
        self.onglet3_content = Onglet3Content(self.tab3)

    def quit_application(self):
        self.destroy()
        sys.exit()


class Onglet1Content:
    def __init__(self, root):
        self.root = root
        self.df = pd.read_json("donnees.json", orient="records", lines=True)
        self.choice_var1 = tk.StringVar()
        self.choice_var2 = tk.StringVar()
        self.choice_var3 = tk.StringVar()
        self.choice_var_marque = tk.StringVar()
        self.choice_var_modele = tk.StringVar()
        self.min_value_var = tk.DoubleVar()
        self.max_value_var = tk.DoubleVar()
        self.min_price_var = tk.DoubleVar()
        self.max_price_var = tk.DoubleVar()
        self.min_annee_var = tk.DoubleVar()
        self.max_annee_var = tk.DoubleVar()
        self.min_puissance_var = tk.DoubleVar()
        self.max_puissance_var = tk.DoubleVar()

        self._create_gui(root)

    def _create_gui(self, root):
        self.create_dropdowns(root)
        self.create_interval_filters()
        self.create_filter_button(root)
        self.create_treeview()
        self.configure_layout()

    def create_dropdowns(self, root):
        label1 = ttk.Label(
            self.root, text="Carrosserie:", background="darkred", foreground="white"
        )
        label1.grid(row=0, column=0)
        self.dropdown1 = ttk.Combobox(
            self.root,
            textvariable=self.choice_var1,
            values=["Tous"] + self.get_unique_values("Carrosserie"),
        )
        self.dropdown1.grid(row=0, column=1)
        self.dropdown1.set("Tous")

        label2 = ttk.Label(
            self.root, text="Transmission:", background="darkred", foreground="white"
        )
        label2.grid(row=1, column=0)
        self.dropdown2 = ttk.Combobox(
            self.root,
            textvariable=self.choice_var2,
            values=["Tous"] + self.get_unique_values("Transmission"),
        )
        self.dropdown2.grid(row=1, column=1)
        self.dropdown2.set("Tous")

        label3 = ttk.Label(
            self.root, text="Carburant:", background="darkred", foreground="white"
        )
        label3.grid(row=2, column=0)
        self.dropdown3 = ttk.Combobox(
            self.root,
            textvariable=self.choice_var3,
            values=["Tous"] + self.get_unique_values("Carburant"),
        )
        self.dropdown3.grid(row=2, column=1)
        self.dropdown3.set("Tous")

        label_marque = ttk.Label(
            root, text="Marque:", background="darkred", foreground="white"
        )
        label_marque.grid(row=0, column=2)
        self.dropdown_marque = ttk.Combobox(
            root,
            textvariable=self.choice_var_marque,
            values=["Tous"] + self.get_unique_values("Marque"),
        )
        self.dropdown_marque.grid(row=0, column=3)
        self.dropdown_marque.set("Tous")

        self.marques_uniques = self.get_unique_values("Marque")
        label_modele = ttk.Label(
            root, text="Modèle:", background="darkred", foreground="white"
        )
        label_modele.grid(row=1, column=2)
        self.dropdown_modele = ttk.Combobox(
            root,
            textvariable=self.choice_var_modele,
            values=["Tous"] + self.get_modeles_for_marque(self.marques_uniques[0]),
        )
        self.dropdown_modele.grid(row=1, column=3)
        self.dropdown_modele.set("Tous")

        self.choice_var_marque.trace_add("write", self.update_options_modele)

    def get_modeles_for_marque(self, marque):
        modeles_for_marque = self.df.loc[self.df["Marque"] == marque, "Modele"].unique()
        return list(modeles_for_marque)

    def update_options_modele(self, *args):
        selected_marque = self.choice_var_marque.get()
        new_modeles = self.get_modeles_for_marque(selected_marque)
        self.dropdown_modele["values"] = ["Tous"] + new_modeles

    def create_interval_filters(self):
        label_min = ttk.Label(
            self.root, text="Kilomètre min:", background="darkred", foreground="white"
        )
        label_min.grid(row=0, column=4)
        entry_min = ttk.Entry(self.root, textvariable=self.min_value_var)
        entry_min.grid(row=0, column=5)

        label_max = ttk.Label(
            self.root, text="Kilomètre max:", background="darkred", foreground="white"
        )
        label_max.grid(row=1, column=4)
        entry_max = ttk.Entry(self.root, textvariable=self.max_value_var)
        entry_max.grid(row=1, column=5)

        label_price_min = ttk.Label(
            self.root, text="Prix min:", background="darkred", foreground="white"
        )
        label_price_min.grid(row=0, column=6)
        entry_price_min = ttk.Entry(self.root, textvariable=self.min_price_var)
        entry_price_min.grid(row=0, column=7)

        label_price_max = ttk.Label(
            self.root, text="Prix max:", background="darkred", foreground="white"
        )
        label_price_max.grid(row=1, column=6)
        entry_price_max = ttk.Entry(self.root, textvariable=self.max_price_var)
        entry_price_max.grid(row=1, column=7)

        label_annee_min = ttk.Label(
            self.root, text="Année min:", background="darkred", foreground="white"
        )
        label_annee_min.grid(row=2, column=6)
        entry_annee_min = ttk.Entry(self.root, textvariable=self.min_annee_var)
        entry_annee_min.grid(row=2, column=7)

        label_annee_max = ttk.Label(
            self.root, text="Année max:", background="darkred", foreground="white"
        )
        label_annee_max.grid(row=3, column=6)
        entry_annee_max = ttk.Entry(self.root, textvariable=self.max_annee_var)
        entry_annee_max.grid(row=3, column=7)

        label_puissance_min = ttk.Label(
            self.root, text="Puissance min:", background="darkred", foreground="white"
        )
        label_puissance_min.grid(row=2, column=4)
        entry_puissance_min = ttk.Entry(self.root, textvariable=self.min_puissance_var)
        entry_puissance_min.grid(row=2, column=5)

        label_puissance_max = ttk.Label(
            self.root, text="Puissance max:", background="darkred", foreground="white"
        )
        label_puissance_max.grid(row=3, column=4)
        entry_puissance_max = ttk.Entry(self.root, textvariable=self.max_puissance_var)
        entry_puissance_max.grid(row=3, column=5)

    def create_filter_button(self, root):
        filter_button = ttk.Button(self.root, text="Filtrer", command=self.filter_data)
        filter_button.grid(row=4, column=0, columnspan=4)
        clear_filters_button = ttk.Button(
            root, text="Effacer filtres", command=self.clear_filters
        )
        clear_filters_button.grid(row=4, column=1, columnspan=4)

    def clear_filters(self):
        self.choice_var1.set("Tous")
        self.choice_var2.set("Tous")
        self.choice_var3.set("Tous")
        self.choice_var_marque.set("Tous")
        self.choice_var_modele.set("Tous")
        self.min_value_var.set(0.0)
        self.max_value_var.set(0.0)
        self.min_price_var.set(0.0)
        self.max_price_var.set(0.0)
        self.min_puissance_var.set(0.0)
        self.max_puissance_var.set(0.0)
        self.min_annee_var.set(0.0)
        self.max_annee_var.set(0.0)

        self.dropdown1.set("Tous")
        self.dropdown2.set("Tous")
        self.dropdown3.set("Tous")
        self.dropdown_marque.set("Tous")
        self.dropdown_modele.set("Tous")

        self.filter_data()

    def create_treeview(self):
        columns = list(self.df.columns)
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=75)
        self.tree.grid(row=5, column=0, columnspan=8, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def configure_layout(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_columnconfigure(4, weight=1)
        self.root.grid_columnconfigure(5, weight=1)
        self.root.grid_columnconfigure(6, weight=1)
        self.root.grid_columnconfigure(7, weight=1)
        self.root.grid_rowconfigure(5, weight=3)

    def filter_data(self):
        choice1 = self.choice_var1.get()
        choice2 = self.choice_var2.get()
        choice3 = self.choice_var3.get()
        choice_marque = self.choice_var_marque.get()
        choice_modele = self.choice_var_modele.get()
        min_value = self.min_value_var.get()
        max_value = self.max_value_var.get()
        min_price = self.min_price_var.get()
        max_price = self.max_price_var.get()
        min_annee = self.min_annee_var.get()
        max_annee = self.max_annee_var.get()
        min_puissance = self.min_puissance_var.get()
        max_puissance = self.max_puissance_var.get()

        filtered_df = self.df.copy()

        if choice1 != "Tous":
            filtered_df = filtered_df[filtered_df["Carrosserie"] == choice1]

        if choice2 != "Tous":
            filtered_df = filtered_df[filtered_df["Transmission"] == choice2]

        if choice3 != "Tous":
            filtered_df = filtered_df[filtered_df["Carburant"] == choice3]

        if choice_marque != "Tous":
            filtered_df = filtered_df[filtered_df["Marque"] == choice_marque]

        if choice_modele != "Tous":
            filtered_df = filtered_df[filtered_df["Modele"] == choice_modele]

        if min_value:
            filtered_df = filtered_df[filtered_df["Km"] >= min_value]

        if max_value:
            filtered_df = filtered_df[filtered_df["Km"] <= max_value]

        if min_price:
            filtered_df = filtered_df[filtered_df["Prix"] >= min_price]

        if max_price:
            filtered_df = filtered_df[filtered_df["Prix"] <= max_price]

        if min_puissance:
            filtered_df = filtered_df[filtered_df["Puissance"] >= min_puissance]

        if max_puissance:
            filtered_df = filtered_df[filtered_df["Puissance"] <= max_puissance]

        if min_annee:
            filtered_df = filtered_df[filtered_df["Annee"] >= min_annee]

        if max_annee:
            filtered_df = filtered_df[filtered_df["Annee"] <= max_annee]

        self.display_results(filtered_df.sort_values(by="Note", ascending=False))

    def display_results(self, df):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, row in df.iterrows():
            values = tuple(row)
            str_index = str(index)
            self.tree.insert("", "end", iid=str_index, values=values, tags=(str_index,))

    def on_treeview_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]
            if values:
                link = values[0].replace("\\", "/")
                if link.startswith("http://") or link.startswith("https://"):
                    webbrowser.open(link)

    def get_unique_values(self, column_name):
        unique_values = self.df[column_name].unique()
        return list(unique_values)


class Onglet2Content:
    def __init__(self, root):
        self.root = root
        self.df = pd.read_json("donnees.json", orient="records", lines=True)
        self.selected_graph_var = tk.StringVar()
        self.create_gui()

    def create_gui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")
        self.main_frame.configure(style="Custom.TFrame")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.fig, self.axes = plt.subplots(nrows=1, ncols=2)
        self.fig.tight_layout()

        self.create_avg_price_barh(self.axes[0])
        self.create_avg_note_barh(self.axes[1])

        graph_options = [
            "Prix et note Moyenne par Marque",
            "Matrice de corrélation",
            "Histogramme prix et note par transmission",
            "Histogramme prix et note par carburant",
        ]
        graph_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.selected_graph_var, values=graph_options
        )
        graph_dropdown.grid(row=0, column=0, columnspan=2)
        graph_dropdown.bind("<<ComboboxSelected>>", self.update_graph)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def update_graph(self, event):
        selected_graph = self.selected_graph_var.get()
        self.canvas.get_tk_widget().destroy()

        if selected_graph == "Prix et note Moyenne par Marque":
            self.fig, self.axes = plt.subplots(nrows=1, ncols=2)
            self.create_avg_price_barh(self.axes[0])
            self.create_avg_note_barh(self.axes[1])
        elif selected_graph == "Histogramme prix et note par carburant":
            self.fig, self.axes = plt.subplots(nrows=1, ncols=2)
            self.create_hist_note_trans(self.axes[0])
            self.create_hist_prix_trans(self.axes[1])
        elif selected_graph == "Histogramme prix et note par transmission":
            self.fig, self.axes = plt.subplots(nrows=1, ncols=2)
            self.create_hist_note_carb(self.axes[0])
            self.create_hist_prix_carb(self.axes[1])
        elif selected_graph == "Matrice de corrélation":
            self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
            self.create_correlation_heatmap(self.axes)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def create_avg_price_barh(self, ax):
        note_moyenne_marque = self.df.groupby("Marque")["Note"].mean()
        marques_triees = note_moyenne_marque.sort_values(ascending=True).index.tolist()
        moyenne_par_marque = (
            self.df.groupby("Marque")["Prix"].mean().loc[marques_triees]
        )
        cmap = plt.get_cmap("Reds")
        vmin_adjusted = moyenne_par_marque.min() - moyenne_par_marque.min() * 6
        vmax_adjusted = moyenne_par_marque.max()
        norm = mcolors.Normalize(vmin=vmin_adjusted, vmax=vmax_adjusted)
        colors = [cmap(norm(value)) for value in moyenne_par_marque]
        moyenne_par_marque.plot(kind="barh", ax=ax, color=colors)
        max_value = moyenne_par_marque.max()
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        for index, value in enumerate(moyenne_par_marque):
            formatted_value = locale.currency(
                round(value, 0), grouping=True, symbol=True
            )
            ax.text(
                max_value,
                index,
                formatted_value.replace(",00", ""),
                ha="left",
                va="center",
                color="black",
            )
        ax.set_title("Prix Moyen par Marque")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="both", which="both", length=0)
        ax.set_xticklabels([])
        ax.set_ylabel("")
        ax.set_xlabel("")

    def create_avg_note_barh(self, ax):
        moyenne_par_marque = (
            self.df.groupby("Marque")["Note"].mean().sort_values(ascending=False)
        )
        moyenne_par_marque_sorted = moyenne_par_marque.sort_values()
        max_value = moyenne_par_marque_sorted.max()
        cmap = plt.get_cmap("RdBu")
        vmin_adjusted = moyenne_par_marque_sorted.min()
        vmax_adjusted = moyenne_par_marque_sorted.max()
        norm = mcolors.Normalize(vmin=vmin_adjusted, vmax=vmax_adjusted)
        colors = [cmap(norm(value)) for value in moyenne_par_marque]
        moyenne_par_marque_sorted.plot(kind="barh", ax=ax, color=colors)
        ax.set_xticks([])
        ax.set_yticks([])
        for index, value in enumerate(moyenne_par_marque_sorted):
            ax.text(
                max_value, index, f"{value:.2f}", ha="left", va="center", color="black"
            )
        ax.set_title("Note Moyenne par Marque")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="both", which="both", length=0)
        ax.set_ylabel("")
        ax.set_xlabel("")

    def create_hist_note_trans(self, ax):
        colors = {
            "Boîte automatique": "blue",
            "Boîte manuelle": "darkred",
            "Semi-automatique": "green",
        }
        sns.histplot(
            data=self.df,
            x="Note",
            hue="Transmission",
            element="step",
            stat="density",
            common_norm=True,
            bins=100,
            binrange=(-10, 10),
            palette=colors,
            ax=ax,
        )
        ax.set_xlabel("Note", fontsize=12, fontweight="bold")
        ax.set_ylabel("Fréquence relative", fontsize=12, fontweight="bold")
        ax.set_title(
            "Histogramme des notes en fonction de la transmission",
            fontsize=14,
            fontweight="bold",
        )

    def create_hist_prix_trans(self, ax):
        colors = {
            "Boîte automatique": "blue",
            "Boîte manuelle": "darkred",
            "Semi-automatique": "green",
        }
        sns.histplot(
            data=self.df,
            x="Prix",
            hue="Transmission",
            element="step",
            stat="density",
            common_norm=True,
            bins=100,
            binrange=(1000, 100000),
            palette=colors,
            ax=ax,
        )
        ax.set_xlabel("Prix", fontsize=12, fontweight="bold")
        ax.set_ylabel("Fréquence relative", fontsize=12, fontweight="bold")
        ax.set_title(
            "Histogramme des prix en fonction de la transmission",
            fontsize=14,
            fontweight="bold",
        )

    def create_hist_note_carb(self, ax):
        colors = {
            "Electrique": "orange",
            "Diesel": "red",
            "AUTRE": "green",
            "GPL": "darkgreen",
            "GNL": "tomato",
            "Essence": "yellow",
        }
        sns.histplot(
            data=self.df,
            x="Note",
            hue="Carburant",
            element="step",
            stat="density",
            common_norm=True,
            bins=100,
            binrange=(-10, 10),
            palette=colors,
            ax=ax,
        )
        ax.set_xlabel("Note", fontsize=12, fontweight="bold")
        ax.set_ylabel("Fréquence relative", fontsize=12, fontweight="bold")
        ax.set_title(
            "Histogramme des notes en fonction du type de carburant",
            fontsize=14,
            fontweight="bold",
        )

    def create_hist_prix_carb(self, ax):
        colors = {
            "Electrique": "orange",
            "Diesel": "red",
            "AUTRE": "green",
            "GPL": "darkgreen",
            "GNL": "tomato",
            "Essence": "yellow",
        }
        sns.histplot(
            data=self.df,
            x="Prix",
            hue="Carburant",
            element="step",
            stat="density",
            common_norm=True,
            bins=100,
            binrange=(1000, 100000),
            palette=colors,
            ax=ax,
        )
        ax.set_xlabel("Prix", fontsize=12, fontweight="bold")
        ax.set_ylabel("Fréquence relative", fontsize=12, fontweight="bold")
        ax.set_title(
            "Histogramme des prix en fonction du type de carburant",
            fontsize=14,
            fontweight="bold",
        )

    def create_correlation_heatmap(self, ax):
        numeric_columns = self.df.select_dtypes(include="number")
        corr_matrix = numeric_columns.corr().round(2)
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="seismic",
            ax=ax,
            mask=mask,
            cbar=False,
            vmin=-1,
            vmax=1,
        )
        plt.xticks(rotation=0)


class Onglet3Content:
    def __init__(self, root):
        self.root = root
        self.df = pd.read_json("donnees.json", orient="records", lines=True)
        self.extra = pd.read_json("modele.json", orient="records", lines=True)
        self.create_gui()

    def create_gui(self):
        frame = ttk.Frame(self.root, style="Custom.TFrame")
        extra = ttk.Frame(self.root, style="Custom.TFrame")
        frame.grid(row=1, column=0, sticky="nsew")
        extra.grid(row=3, column=0, sticky="nsew")
        self.create_statistics_table()
        self.create_extra_table()
        self.configure_table()

    def create_statistics_table(self):
        self.columns = [
            "",
            "Valeur Manquante",
            "Moyenne",
            "Ecart type",
            "Min",
            "25%",
            "50%",
            "75%",
            "Max",
        ]
        self.table_data = []

        for col in self.df.columns:
            if is_numeric_dtype(self.df[col]):
                values = [
                    col,
                    f"{int((1 - self.df[col].count() / len(self.df[col])) * 100)} %",
                    f"{round(self.df[col].mean(), 1)}",
                    f"{round(self.df[col].std(), 1)}",
                    f"{int(self.df[col].min())}",
                    f"{int(self.df[col].quantile(0.25))}",
                    f"{int(self.df[col].median())}",
                    f"{int(self.df[col].quantile(0.75))}",
                    f"{int(self.df[col].max())}",
                ]

                self.table_data.append(values)

        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 12), rowheight=30)
        self.table = ttk.Treeview(
            self.root,
            columns=self.columns,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview",
        )
        style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))
        for i, row in enumerate(self.table_data):
            tags = ["odd_row" if i % 2 != 0 else "even_row"]
            self.table.insert("", "end", values=row, tags=tags)

        for col in self.columns:
            self.table.heading(col, text=col, anchor="center")
            self.table.column(col, anchor="center")

        self.table.tag_configure("odd_row", background="#f0f0f0")

        self.table.grid(row=1, column=0, sticky="nsew")

    def create_extra_table(self):
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 12))
        style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))
        columns = list(self.extra.columns)
        self.extra_tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview",
        )

        for index, row in self.extra.iterrows():
            values = tuple(row)
            str_index = str(index)
            self.extra_tree.insert(
                "", "end", iid=str_index, values=values, tags=(str_index,)
            )

        for col in columns:
            self.extra_tree.heading(col, text=col, anchor="center")
            self.extra_tree.column(col, anchor="center")

        self.extra_tree.tag_configure("odd_row", background="#f0f0f0")
        self.extra_tree.grid(row=3, column=0, sticky="nsew")

    def configure_table(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=6)
        self.root.grid_rowconfigure(1, weight=6)
        self.root.grid_rowconfigure(2, weight=6)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=6)
