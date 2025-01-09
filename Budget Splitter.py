import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Placeholder constants
FEDERAL_TAX_RATE = 0.1  # Default federal tax rate
INFLATION_RATE = 0.02  # Default inflation rate
# State tax rates
STATE_TAX_RATES = {
    "AL": 0.05, "AK": 0.0, "AZ": 0.056, "AR": 0.065,
    "AS": 0.03, "CA": 0.08, "CO": 0.046, "CT": 0.0635,
    "DE": 0.066, "FL": 0.0, "GA": 0.0575, "HI": 0.0725,
    "ID": 0.0625, "IL": 0.0495, "IN": 0.0323, "IA": 0.062,
    "KS": 0.057, "KY": 0.05, "LA": 0.06, "ME": 0.0715,
    "MD": 0.0575, "MA": 0.05, "MI": 0.0425, "MN": 0.0785,
    "MS": 0.05, "MO": 0.053, "MT": 0.065, "NE": 0.0684,
    "NV": 0.0, "NH": 0.0, "NJ": 0.0675, "NM": 0.049,
    "NY": 0.0645, "NC": 0.0495, "ND": 0.021, "OH": 0.05,
    "OK": 0.05, "OR": 0.099, "PA": 0.0307, "RI": 0.0515,
    "SC": 0.07, "SD": 0.0, "TN": 0.0, "TX": 0.0, "UT": 0.0495,
    "VT": 0.0875, "VA": 0.0575, "WA": 0.0, "WV": 0.065,
    "WI": 0.065, "WY": 0.0
}
def get_state_tax_rate(state):
    """Returns the tax rate for a given state."""
    return STATE_TAX_RATES.get(state, 0)
class BudgetSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Splitter")
        self.root.geometry("1000x600")
        self.categories = []
        self.amounts = []
        # Configure grid layout
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)
        # Left: Expense Breakdown Table
        ttk.Label(root, text="Expense Breakdown", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.breakdown_table = ttk.Treeview(root, columns=("Category", "Amount"), show="headings", height=20)
        self.breakdown_table.heading("Category", text="Category")
        self.breakdown_table.heading("Amount", text="Amount ($)")
        self.breakdown_table.column("Category", anchor="w", width=150)
        self.breakdown_table.column("Amount", anchor="e", width=100)
        self.breakdown_table.grid(row=1, column=0, rowspan=10, padx=10, sticky="ns")
        # Right: Form Fields and Buttons
        ttk.Label(root, text="Enter Your Monthly Income:").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.income_var = tk.DoubleVar()
        ttk.Entry(root, textvariable=self.income_var).grid(row=0, column=1, padx=10, pady=5, sticky="e")
        ttk.Label(root, text="Select Your State:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.state_var = tk.StringVar(value="Select State")
        states = list(STATE_TAX_RATES.keys())
        ttk.Combobox(root, textvariable=self.state_var, values=states, state="readonly").grid(row=1, column=1, padx=10, pady=5, sticky="e")
        ttk.Button(root, text="Calculate Taxes", command=self.calculate_taxes).grid(row=2, column=1, padx=10, pady=5, sticky="e")
        ttk.Label(root, text="Enter Number of Years for Inflation Prediction:").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.inflation_years_var = tk.IntVar()
        ttk.Entry(root, textvariable=self.inflation_years_var).grid(row=3, column=1, padx=10, pady=5, sticky="e")
        ttk.Button(root, text="Predict Inflation", command=self.calculate_inflation).grid(row=4, column=1, padx=10, pady=5, sticky="e")
        ttk.Label(root, text="Add Custom Budget Category:").grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.category_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.category_var).grid(row=5, column=1, padx=10, pady=5, sticky="e")
        ttk.Label(root, text="Allocate Amount for Category:").grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.amount_var = tk.DoubleVar()
        ttk.Entry(root, textvariable=self.amount_var).grid(row=6, column=1, padx=10, pady=5, sticky="e")
        ttk.Button(root, text="Add Category", command=self.add_category).grid(row=7, column=1, padx=10, pady=5, sticky="e")
        ttk.Label(root, text="Enter Number of People to Split Budget:").grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.people_var = tk.IntVar()
        ttk.Entry(root, textvariable=self.people_var).grid(row=8, column=1, padx=10, pady=5, sticky="e")
        ttk.Button(root, text="Split Budget", command=self.split_budget).grid(row=9, column=1, padx=10, pady=5, sticky="e")
        ttk.Button(root, text="Visualize Budget Distribution", command=self.visualize_budget).grid(row=10, column=1, padx=10, pady=5, sticky="e")
        # Result Display
        self.result_label = ttk.Label(root, text="", wraplength=400, font=("Arial", 12))
        self.result_label.grid(row=11, column=1, padx=10, pady=10, sticky="w")
    def calculate_taxes(self):
        income = self.income_var.get()
        state_tax_rate = get_state_tax_rate(self.state_var.get())
        federal_tax = income * FEDERAL_TAX_RATE
        state_tax = income * state_tax_rate
        total_tax = federal_tax + state_tax
        self.result_label.config(
            text=f"State Tax: ${state_tax:.2f}\nFederal Tax: ${federal_tax:.2f}\nTotal Tax: ${total_tax:.2f}"
        )
    def calculate_inflation(self):
        years = self.inflation_years_var.get()
        inflation_rate = INFLATION_RATE
        future_income = self.income_var.get() * ((1 + inflation_rate) ** years)
        self.result_label.config(
            text=f"Income after {years} year(s): ${future_income:.2f} (with {inflation_rate * 100:.2f}% inflation)."
        )
    def add_category(self):
        category = self.category_var.get()
        amount = self.amount_var.get()
        if category and amount > 0:
            self.categories.append(category)
            self.amounts.append(amount)
            self.update_breakdown_table()
        else:
            messagebox.showerror("Invalid Input", "Please enter valid category and amount.")
    def update_breakdown_table(self):
        for item in self.breakdown_table.get_children():
            self.breakdown_table.delete(item)
        for category, amount in zip(self.categories, self.amounts):
            self.breakdown_table.insert("", "end", values=(category, f"{amount:.2f}"))
    def split_budget(self):
        num_people = self.people_var.get()
        total_budget = sum(self.amounts)
        if num_people > 0 and total_budget > 0:
            per_person = total_budget / num_people
            self.result_label.config(
                text=f"Total Budget: ${total_budget:.2f}\nNumber of People: {num_people}\nAmount per Person: ${per_person:.2f}"
            )
        else:
            messagebox.showerror("Invalid Input", "Please add valid budget categories and number of people.")
    def visualize_budget(self):
        if self.categories and self.amounts:
            plt.figure(figsize=(6, 6))
            plt.pie(self.amounts, labels=self.categories, autopct="%1.1f%%", startangle=140)
            plt.title("Budget Allocation")
            plt.axis("equal")
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Budget Visualization")
            canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack()
        else:
            messagebox.showerror("Invalid Input", "Please add budget categories before visualizing.")
# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetSplitterApp(root)
    root.mainloop()