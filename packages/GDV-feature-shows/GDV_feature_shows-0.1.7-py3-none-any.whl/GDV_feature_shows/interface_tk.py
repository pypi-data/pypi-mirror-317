# coding: utf-8

import tkinter as tk
from tkinter import ttk
from ksupk import save_json, restore_json

from GDV_feature_shows.resource_manager import ResourceManager
from GDV_feature_shows.name_volume import get_settings, get_visualization
from GDV_feature_shows.process import update_feature_extractor_with_settings, fill_visualizations, define_paths
from GDV_feature_shows.feature_extraction import KImage


class ImageFTK(tk.Label):
    def __init__(self, root):
        super().__init__(root)
        self.kimg = None
        self.img_tk = None

    def set_img(self, kimg: KImage):
        self.kimg = kimg
        self.img_tk = self.kimg.get_as_tk()
        self.config(image=self.img_tk)


class VisualizationFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Left: Placeholder for the image
        # self.image_label = tk.Label(self, width=20, height=10)
        self.image_frame = ImageFTK(self)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)

        # Right: Table with features
        self.feature_table = ttk.Treeview(self, columns=("Feature", "Value"), show="headings")
        self.feature_table.heading("Feature", text="Feature")
        self.feature_table.heading("Value", text="Value")

        self.feature_table.grid(row=0, column=1, padx=10, pady=10)

    def set_pic(self, kimg: KImage):
        # self.image_label.config(bg=image_color)
        self.image_frame.set_img(kimg)

    def set_features(self, features):
        for feature, value in features.items():
            self.feature_table.insert("", "end", values=(feature, value))


class App(tk.Tk):
    def __init__(self, gdv_folder_path: str, settings_path: str):
        super().__init__()

        rm = ResourceManager()
        self.iconphoto(False, tk.PhotoImage(file=ResourceManager().ico_path()))

        self.title("GDV_feature_shows")

        # Top-level variables
        self.items, self.paths = define_paths(gdv_folder_path)
        self.current_item_index = 0
        self.settings_file = settings_path
        self.visualization_options = list(get_visualization())

        self.visualizations = {}

        (self.filter, self.top_frame, self.item_label, self.left_button, self.right_button,
         self.tab_control, self.settings_tab, self.showing_tab) = None, None, None, None, None, None, None, None

        self.settings, self.settings_table, self.save_button = None, None, None

        self.combobox, self.visualization_frame = None, None

        self.initialize_ui()

    def update_visualizations(self):
        # cur_folder = self.item_label.cget("text")

        for k_i in self.visualization_options:
            if k_i in self.visualizations:
                if self.visualizations[k_i].winfo_exists():
                    self.visualizations[k_i].destroy()
                self.visualizations[k_i] = VisualizationFrame(self.showing_tab)
            else:
                self.visualizations[k_i] = VisualizationFrame(self.showing_tab)

        fill_visualizations(self.paths[self.current_item_index], self.visualizations)

    def initialize_ui(self):
        # Top Label with Navigation

        self.top_frame = tk.Frame(self)
        self.top_frame.grid(row=0, column=0, pady=10)

        self.filter = tk.Entry(self.top_frame, width=30)
        self.filter.pack(padx=5)

        self.left_button = tk.Button(self.top_frame, text="<", command=self.prev_item)
        self.left_button.pack(side=tk.LEFT, padx=5)
        self.bind("<Left>", lambda e: self.prev_item())

        self.item_label = tk.Label(self.top_frame, text=self.items[self.current_item_index])
        self.item_label.pack(side=tk.LEFT, padx=5)

        self.right_button = tk.Button(self.top_frame, text=">", command=self.next_item)
        self.right_button.pack(side=tk.LEFT, padx=5)
        self.bind("<Right>", lambda e: self.next_item())

        # Tabs (Settings and Showing)
        self.tab_control = ttk.Notebook(self)
        self.tab_control.grid(row=1, column=0, padx=10, pady=10)

        # Settings Tab
        self.settings_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.settings_tab, text="Settings")
        self.initialize_settings_tab()

        # Showing Tab
        self.showing_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.showing_tab, text="Showing")
        self.update_visualizations()
        self.initialize_showing_tab()

    def prev_item(self):
        before = self.current_item_index
        self.current_item_index = (self.current_item_index - 1) % len(self.items)
        filtered_text = self.filter.get().lower()
        if filtered_text != "":
            while (not (filtered_text in self.items[self.current_item_index].lower())
                   and before != self.current_item_index):
                self.current_item_index = (self.current_item_index - 1) % len(self.items)
        self.update_all()

    def next_item(self):
        before = self.current_item_index
        self.current_item_index = (self.current_item_index + 1) % len(self.items)
        filtered_text = self.filter.get().lower()
        if filtered_text != "":
            while (not (filtered_text in self.items[self.current_item_index].lower())
                   and before != self.current_item_index):
                self.current_item_index = (self.current_item_index + 1) % len(self.items)
        self.update_all()

    def update_all(self):
        self.update_item_label()
        self.update_visualizations()
        self.update_visualization_frame()

    def update_item_label(self):
        self.item_label.config(text=self.items[self.current_item_index])

    def initialize_settings_tab(self):
        # Load settings from JSON
        try:
            self.settings = restore_json(self.settings_file)
        except FileNotFoundError:
            self.settings = get_settings()
            self.save_settings()

        # Table for settings
        self.settings_table = ttk.Treeview(self.settings_tab, columns=("Name", "Value"), show="headings")
        self.settings_table.heading("Name", text="Setting")
        self.settings_table.heading("Value", text="Value")

        for name, value in self.settings.items():
            self.settings_table.insert("", "end", values=(name, value))

        self.settings_table.grid(row=0, column=0, padx=10, pady=10)

        # Enable editing for the second column
        self.settings_table.bind("<Double-1>", self.edit_cell)

        # Save Button
        self.save_button = tk.Button(self.settings_tab, text="Save Settings", command=self.save_settings_from_table)
        self.save_button.grid(row=1, column=0, pady=10)

    def edit_cell(self, event):
        region = self.settings_table.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.settings_table.identify_row(event.y)
            column = self.settings_table.identify_column(event.x)

            if column == "#2":  # Only allow editing the Value column
                x, y, width, height = self.settings_table.bbox(row_id, column)
                entry = tk.Entry(self.settings_table)
                entry.place(x=x, y=y, width=width, height=height)
                entry.insert(0, self.settings_table.set(row_id, column))

                def save_edit(event):
                    self.settings_table.set(row_id, column, entry.get())
                    entry.destroy()

                entry.bind("<Return>", save_edit)
                entry.bind("<FocusOut>", lambda e: entry.destroy())
                entry.focus()

        update_feature_extractor_with_settings(self.get_settings_from_table())
        self.update_all()

    def get_settings_from_table(self):
        d = {}
        for row in self.settings_table.get_children():
            name, value = self.settings_table.item(row, "values")
            d[name] = int(value)
        return d

    def save_settings_from_table(self):
        for row in self.settings_table.get_children():
            name, value = self.settings_table.item(row, "values")
            self.settings[name] = int(value)
        update_feature_extractor_with_settings(self.settings)
        self.save_settings()
        self.update_all()

    def save_settings(self):
        save_json(self.settings_file, self.settings)

    def initialize_showing_tab(self):
        # Combobox for visualization options
        self.combobox = ttk.Combobox(self.showing_tab, values=self.visualization_options, state="readonly")
        self.combobox.grid(row=0, column=0, padx=10, pady=10)
        self.combobox.bind("<<ComboboxSelected>>", self.update_visualization_frame)

        # Default Frame
        self.visualization_frame = None
        self.combobox.set(self.visualization_options[0])
        self.update_visualization_frame()

    def update_visualization_frame(self, event=None):
        selected_option = self.combobox.get()

        if self.visualization_frame is not None and self.visualization_frame.winfo_exists():
            self.visualization_frame.grid_forget()
        self.visualization_frame = self.visualizations[selected_option]

        self.visualization_frame.grid(row=1, column=0, padx=10, pady=10)
