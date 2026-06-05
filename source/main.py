import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from kino_logic import KinoLogic
from kino_db import KinoDB
from kino_gui import KinoGUI 

class MainController:
    def __init__(self, root):
        self.root = root
        
        # Αρχικοποιούμε τα modules
        self.logic = KinoLogic()
        self.db = KinoDB()
        
        # Δημιουργούμε το γραφικό περιβάλλον και του περνάμε τον εαυτό μας (self)
        self.ui = KinoGUI(self.root, self)

        # Καλείται η ask_initial_wallet για να ζητήσει από τον χρήστη να κάνει την αρχική του κατάθεση
        self.ask_initial_wallet()
        self.ask_initial_time_between_draws()

        try:
            with open("payouts.json", "r", encoding="utf-8") as f:
                self.payouts_table = json.load(f)

        except Exception as e:
            messagebox.showerror(
                "Κρίσιμο Σφάλμα",
                f"Αποτυχία φόρτωσης πίνακα κερδών:\n{e}")
            self.root.destroy()


    def ask_initial_wallet(self):
        """Εμφανίζει pop-up για κατάθεση. Αν δεν βάλει χρήματα, κλείνει το παιχνίδι."""
        deposit = 0.0
        
        while deposit <= 0:
            deposit = simpledialog.askfloat(
                "Αρχική Κατάθεση", 
                "Καλώς ήρθατε στο KINO!\n\nΠαρακαλώ εισάγετε το ποσό κατάθεσης (€):",
                minvalue=1.0,
                parent=self.root
            )
            
            if deposit is None:
                messagebox.showinfo("Έξοδος", "Πρέπει να κάνετε κατάθεση για να παίξετε. Κλείσιμο εφαρμογής.")
                self.root.destroy()

            
        # Ενημερώνουμε τη βάση δεδομένων με το ποσό και το UI
        self.db.wallet = deposit
        self.ui.update_wallet_display(self.db.wallet)

    def ask_initial_time_between_draws(self):
        """Εμφανίζει pop-up για να ρυθμίσει ο χρήστης τον χρόνο μεταξύ των κληρώσεων."""
        timer_seconds = 0
        while timer_seconds <= 0:
            timer_seconds = simpledialog.askinteger(
                "Ρύθμιση Χρόνου", 
                "Εισάγετε τον χρόνο μεταξύ των κληρώσεων (σε δευτερόλεπτα):",
                minvalue=1,       
                initialvalue=5,   
                parent=self.root
            )
            
            if timer_seconds is None:
                messagebox.showinfo("Έξοδος", "Ο ορισμός χρόνου είναι υποχρεωτικός. Κλείσιμο εφαρμογής.")
                self.ask_initial_time_between_draws() 
                return
        
        # Ενημερώνουμε το λευκό κουτάκι στο UI για τον χρόνο
        self.ui.timer_entry.delete(0, tk.END)
        self.ui.timer_entry.insert(0, str(timer_seconds))

    def random_pick(self, count, draws=1):
        # Παίρνουμε νέους αριθμούς από το logic, τους αποθηκεύουμε και φτιάχνουμε το δελτίο
        self.ui.selected_numbers = self.logic.get_random_numbers(count)
        self.ui.add_ticket_to_sidebar(self.ui.selected_numbers, draws)

    def on_start_click(self):
        """Το σημείο εκκίνησης όταν πατιέται το κουμπί Έναρξη"""
        try:
            # 1. Διαβάζουμε τις ρυθμίσεις από το UI
            self.total_draws_to_play = int(self.ui.draws_entry.get())
            self.timer_seconds = int(self.ui.timer_entry.get())
            self.bet_amount = float(self.ui.bet_entry.get())
            
            # 2. Έλεγχος αν υπάρχουν δελτία
            if not self.ui.paigmena_deltia:
                messagebox.showwarning("Προσοχή", "Πρέπει να δημιουργήσετε τουλάχιστον ένα δελτίο!")
                return
            
            # 3. Έλεγχος υπολοίπου και αφαίρεση χρημάτων
            total_cost = 0
            for ticket_data in self.ui.paigmena_deltia.values():
                total_cost += self.bet_amount * ticket_data["draws"]
            if self.db.wallet < total_cost:
                messagebox.showwarning("Υπόλοιπο", f"Δεν έχετε αρκετά χρήματα!\nΑπαιτούνται {total_cost:.2f}€")
                return

            # Αφαιρούμε τα χρήματα ΕΦΑΠΑΞ για όλες τις κληρώσεις στην αρχή
            self.db.wallet -= total_cost
            self.ui.update_wallet_display(self.db.wallet)

            # 4. Κλειδώνουμε το κουμπί έναρξης για να μην πατηθεί ξανά
            self.ui.start_btn.config(state="disabled", bg="#555555")
            self.remaining_draws = self.total_draws_to_play
            
            # 5. Ξεκινάμε τον κύκλο κληρώσεων!
            self.run_lottery_cycle()

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ ελέγξτε αν οι τιμές στα πεδία είναι σωστές.")

    #Υπολογισμός των κερδών με βάση τα νούμερα που κερδίζουν επί τον πολλαπλασιαστή στο json
    def calculate_win(self, played_count, hits, bet_amount):

        multiplier = (
            self.payouts_table
            .get(str(played_count), {})
            .get(str(hits), 0)
        )
        return multiplier * bet_amount

    def run_lottery_cycle(self):
        """Εκτελεί μια κλήρωση και προγραμματίζει την επόμενη αντίστροφη μέτρηση"""
        if self.remaining_draws > 0:
            # 1. Καθαρισμός προηγούμενων χρωμάτων
            for i in range(1, 81):
                self.ui.buttons[i].configure(image=self.ui.icons.get("blue-circle"), bg="#001a33", fg="white")

            # 2. Εκτέλεση κλήρωσης
            self.ui.win_list = self.logic.draw_winning_numbers() 
            self.ui.lottery_animation()

            # Σώζουμε την κλήρωση στη βάση/αρχείο
            self.db.save_draw(self.ui.win_list)
            
            # Παίρνουμε το έτοιμο κείμενο με τους καθυστερημένους αριθμούς
            stats_info = self.db.get_top_20_delayed_numbers()
            
            # Το στέλνουμε στο UI (στο δεξί κουτί στατιστικών)
            self.ui.update_statistics(stats_info)
            
            draw_results_text = "--- ΑΠΟΤΕΛΕΣΜΑΤΑ ΚΛΗΡΩΣΗΣ ---\n"
            total_draw_win = 0.0

            for ticket_id, ticket_data in self.ui.paigmena_deltia.items():
                # Ελέγχουμε μόνο τα δελτία που έχουν ακόμα κληρώσεις (draws > 0)
                if ticket_data["draws"] > 0:
                    # Μετατρέπουμε σε Set για να βρούμε αμέσως τις "επαφές" (hits)
                    played_nums = set(ticket_data["arithmoi"])
                    winning_nums = set(self.ui.win_list)
                    
                    hits = played_nums.intersection(winning_nums)
                    num_hits = len(hits)
                    
                    # Μειώνουμε τις κληρώσεις του δελτίου
                    ticket_data["draws"] -= 1

                    played_count = len(played_nums)

                    win_amount = self.calculate_win(
                        played_count,
                        num_hits,
                        self.bet_amount
                    )

                    # Καταγραφή Ιστορικού & Πληρωμή
                    if win_amount > 0:
                        draw_results_text += f"Δελτίο {ticket_id}: {num_hits}/{len(played_nums)} επιτυχίες! ΚΕΡΔΟΣ: {win_amount:.2f}€\n"
                        total_draw_win += win_amount
                        self.db.wallet += win_amount # Μπαίνουν τα λεφτά στη βάση!
                    else:
                        draw_results_text += f"Δελτίο {ticket_id}: {num_hits}/{len(played_nums)} επιτυχίες. (Χωρίς Κέρδος)\n"

            # Ενημέρωση UI με τα κέρδη
            if total_draw_win > 0:
                self.ui.update_wallet_display(self.db.wallet)

            draw_results_text += "\n"
            self.ui.history_text.insert(tk.END, draw_results_text)
            self.ui.history_text.see(tk.END) # Scroll στο τέλος

            # Ανανέωση της Sidebar για να μειωθούν τα νούμερα των κληρώσεων οπτικά!
            self.ui.refresh_sidebar_tickets()
            
            # 3. Μείωση κληρώσεων
            self.remaining_draws -= 1
            
            # 4. Αν υπάρχουν κι άλλες κληρώσεις, ξεκίνα την αντίστροφη μέτρηση
            if self.remaining_draws > 0:
                self.start_countdown(self.timer_seconds)
            else:
                self.ui.countdown_label.config(text="ΟΛΟΚΛΗΡΩΘΗΚΕ!")
                self.ui.start_btn.config(state="normal", bg="#28a745")
                messagebox.showinfo("Ολοκλήρωση", "Όλες οι κληρώσεις ολοκληρώθηκαν!")

    def start_countdown(self, seconds_left):
        """Ενημερώνει το UI κάθε δευτερόλεπτο μέχρι την επόμενη κλήρωση"""
        if seconds_left > 0:
            # Ενημέρωση του κειμένου στο UI
            self.ui.countdown_label.config(text=f"Επόμενη κλήρωση σε: {seconds_left}")
            
            # Προγραμματισμός του επόμενου δευτερολέπτου (1000ms = 1sec)
            self.root.after(1000, lambda: self.start_countdown(seconds_left - 1))
        else:
            # Όταν ο χρόνος τελειώσει, καθάρισε το κείμενο και τρέξε τον κύκλο κλήρωσης
            self.ui.countdown_label.config(text="ΚΛΗΡΩΣΗ ΣΕ ΕΞΕΛΙΞΗ...")
            self.run_lottery_cycle()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainController(root)
    root.mainloop()