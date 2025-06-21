import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SchoolDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Data Interactive Viewer")
        self.root.geometry("1200x720")

        self.df = None
        self.filtered_df = None
        self.filter_entries = {}

        # Load Button
        tk.Button(root, text="📂 Load Data", command=self.load_data, bg="#007acc", fg="white").pack(pady=10)

        # Filter Frame
        self.filter_frame = tk.LabelFrame(root, text="🔎 Filter by Any Field")
        self.filter_frame.pack(fill="x", padx=10, pady=5)

        # Treeview
        self.tree = ttk.Treeview(root)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        vsb = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        # Action Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Apply Filters", command=self.apply_filters, bg="green", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="💾 Export Filtered Data", command=self.export_data, bg="#ff8800", fg="white").pack(side="left", padx=10)

    def load_data(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if not path:
            return

        try:
            if path.endswith('.xlsx'):
                self.df = pd.read_excel(path)
            else:
                self.df = pd.read_csv(path)

            self.filtered_df = self.df.copy()
            self.setup_filter_widgets()
            self.display_data(self.df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def setup_filter_widgets(self):
        for widget in self.filter_frame.winfo_children():
            widget.destroy()
        self.filter_entries.clear()

        for col in self.df.columns:
            frame = tk.Frame(self.filter_frame)
            frame.pack(side="left", padx=5)
            tk.Label(frame, text=col, font=("Arial", 8)).pack()
            ent = tk.Entry(frame, width=15)
            ent.pack()
            self.filter_entries[col] = ent

    def display_data(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        for col in df.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, width=150, anchor='w')

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def apply_filters(self):
        if self.df is None:
            return

        df = self.df.copy()
        for col, entry in self.filter_entries.items():
            val = entry.get().strip()
            if val:
                df = df[df[col].astype(str).str.contains(val, case=False, na=False)]

        self.filtered_df = df
        if df.empty:
            messagebox.showinfo("Notice", "No matching records found.")
        self.display_data(df)

    def sort_column(self, col):
        if self.filtered_df is not None:
            try:
                self.filtered_df = self.filtered_df.sort_values(by=col, ascending=True)
                self.display_data(self.filtered_df)
            except Exception as e:
                messagebox.showerror("Sort Error", str(e))

    def export_data(self):
        if self.filtered_df is None or self.filtered_df.empty:
            messagebox.showwarning("Export Warning", "No data to export.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if not path:
            return

        try:
            if path.endswith('.xlsx'):
                self.filtered_df.to_excel(path, index=False)
            else:
                self.filtered_df.to_csv(path, index=False)
            messagebox.showinfo("Success", f"Data exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolDataApp(root)
    root.mainloop()
