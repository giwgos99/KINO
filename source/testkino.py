import tkinter as tk
from tkinter import messagebox


class KinoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KINO System - Module 1 (GUI)")
        self.root.geometry("1100x950")
        self.root.configure(bg="#001a33")

        # Δεδομένα Κατάστασης (State)
        self.selected_numbers = []
        self.buttons = {}
        self.remaining_draws = 0
        self.total_draws_to_play = 0

        self.setup_ui()

    def setup_ui(self):
        # --- Header ---
        header = tk.Frame(self.root, bg="#001a33")
        header.pack(pady=10)
        tk.Label(header, text="KINO", font=("Arial", 55, "bold"), fg="#ffcc00", bg="#001a33").pack()

        # --- Settings Panel ---
        settings_frame = tk.Frame(self.root, bg="#003366", padx=15, pady=15, highlightbackground="#ffcc00",
                                  highlightthickness=1)
        settings_frame.pack(pady=10, fill="x", padx=40)

        # Πορτοφόλι
        tk.Label(settings_frame, text="Πορτοφόλι (€):", fg="white", bg="#003366", font=("Arial", 9, "bold")).grid(row=0,
                                                                                                                  column=0)
        self.wallet_entry = tk.Entry(settings_frame, width=10)
        self.wallet_entry.insert(0, "100.00")
        self.wallet_entry.grid(row=0, column=1, padx=5)

        # Ποντάρισμα
        tk.Label(settings_frame, text="Ποντάρισμα (€):", fg="#ffcc00", bg="#003366", font=("Arial", 9, "bold")).grid(
            row=0, column=2)
        self.bet_entry = tk.Entry(settings_frame, width=10)
        self.bet_entry.insert(0, "1.00")
        self.bet_entry.grid(row=0, column=3, padx=5)

        # Χρόνος
        tk.Label(settings_frame, text="Sec/Κλήρωση:", fg="white", bg="#003366", font=("Arial", 9, "bold")).grid(row=0,
                                                                                                                column=4)
        self.timer_entry = tk.Entry(settings_frame, width=8)
        self.timer_entry.insert(0, "5")
        self.timer_entry.grid(row=0, column=5, padx=5)

        # Πλήθος Παιχνιδιών
        tk.Label(settings_frame, text="Παιχνίδια:", fg="white", bg="#003366", font=("Arial", 9, "bold")).grid(row=0,
                                                                                                              column=6)
        self.draws_entry = tk.Entry(settings_frame, width=8)
        self.draws_entry.insert(0, "1")
        self.draws_entry.grid(row=0, column=7, padx=5)

        # --- Πλέγμα Αριθμών (1-80) ---
        grid_container = tk.Frame(self.root, bg="#001a33")
        grid_container.pack(pady=10)
        for i in range(1, 81):
            btn = tk.Button(grid_container, text=str(i), width=4, height=2,
                            font=("Arial", 10, "bold"), bg="#004488", fg="white",
                            relief="flat", cursor="hand2",
                            command=lambda n=i: self.toggle_number(n))
            row = (i - 1) // 10
            col = (i - 1) % 10
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.buttons[i] = btn

        # --- Buttons ---
        actions = tk.Frame(self.root, bg="#001a33")
        actions.pack(pady=10)
        tk.Button(actions, text="ΤΥΧΑΙΑ ΕΠΙΛΟΓΗ", font=("Arial", 11, "bold"), bg="#ffcc00", width=18,
                  command=self.random_pick).pack(side="left", padx=10)
        self.start_btn = tk.Button(actions, text="ΕΝΑΡΞΗ ΚΛΗΡΩΣΕΩΝ", font=("Arial", 11, "bold"), bg="#28a745",
                                   fg="white", width=22, command=self.on_start_click)
        self.start_btn.pack(side="left", padx=10)

        # --- Output ---
        output_frame = tk.Frame(self.root, bg="#001a33")
        output_frame.pack(fill="both", expand=True, padx=40, pady=10)
        self.history_text = tk.Text(output_frame, height=12, bg="#002244", fg="#00ffcc", font=("Consolas", 11))
        self.history_text.pack(side="left", fill="both", expand=True, padx=5)
        self.stats_text = tk.Text(output_frame, height=12, width=40, bg="#002244", fg="#ffcc00", font=("Consolas", 11))
        self.stats_text.pack(side="left", fill="both", expand=True, padx=5)

    # --- ΜΕΘΟΔΟΙ ΔΙΕΠΑΦΗΣ (Interface Methods) ---

    def toggle_number(self, num):
        if num in self.selected_numbers:
            self.selected_numbers.remove(num)
            self.buttons[num].configure(bg="#004488", fg="white")
        elif len(self.selected_numbers) < 12:
            self.selected_numbers.append(num)
            self.buttons[num].configure(bg="#ffcc00", fg="black")

    def random_pick(self):
        # Υλοποίηση τυχαίας επιλογής (Μέρος του Module 1)
        import random
        for n in list(self.selected_numbers): self.buttons[n].configure(bg="#004488", fg="white")
        self.selected_numbers = random.sample(range(1, 81), 6)
        for n in self.selected_numbers: self.buttons[n].configure(bg="#ffcc00", fg="black")

    def on_start_click(self):
        """
        Εδώ καλούνται οι μέθοδοι των άλλων modules.
        ΣΗΜΕΙΟ ΣΥΝΔΕΣΗΣ ΜΕ MODULE 2: Έλεγχος Πορτοφολιού και Κόστους.
        ΣΗΜΕΙΟ ΣΥΝΔΕΣΗΣ ΜΕ MODULE 3: Έναρξη Χρονοπρογραμματιστή Κληρώσεων.
        """
        if not self.selected_numbers:
            messagebox.showwarning("Προσοχή", "Επιλέξτε αριθμούς!")
            return

        # Εδώ θα μπει η κλήση: module2.validate_bet(self.wallet_entry.get(), self.bet_entry.get())
        # Και στη συνέχεια: module3.start_process(self.remaining_draws, self.timer_entry.get())
        pass

    def update_wallet_display(self, new_balance):
        """Καλούμενο από Module 2 & 4 για ενημέρωση του υπολοίπου"""
        self.wallet_entry.delete(0, tk.END)
        self.wallet_entry.insert(0, f"{new_balance:.2f}")

    def display_draw_results(self, winning_numbers, profit_info):
        """
        Καλούμενο από Module 3 & 4.
        winning_numbers: list με 20 αριθμούς.
        profit_info: string με το κέρδος (π.χ. '+5.00€').
        """
        # Reset χρωμάτων και φωτισμός νέων αριθμών
        for n, btn in self.buttons.items():
            if n not in self.selected_numbers: btn.configure(bg="#004488", fg="white")

        for num in winning_numbers:
            color = "#28a745" if num in self.selected_numbers else "#dc3545"
            self.buttons[num].configure(bg=color, fg="white")

        self.history_text.insert("1.0", f"Κλήρωση: {sorted(winning_numbers)} | {profit_info}\n")

    def update_statistics(self, stats_data):
        """Καλούμενο από Module 4 για ενημέρωση των καθυστερήσεων"""
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, stats_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = KinoGUI(root)
    root.mainloop()