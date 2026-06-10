import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from kino_logic import KinoLogic
from kino_db import KinoDB
from kino_gui import KinoGUI 

class MainController:
    def __init__(self, root):
        self.root = root
        
        # Ξεκινάμε και κάνουμε αρχικοποίηση των modules που έχουμε εισάγει με το import
        self.logic = KinoLogic()
        self.db = KinoDB()
        
        """ Δημιουργούμε το γραφικό περιβάλλον του χρήστη, όπως το έχουμε ορίσει το kino_gui.py
        Περνάμε το root έτσι ώστε κάθε στοιχείο του GUI να ξέρει που να εμφανίζεται, και το self για να 
        μπορεί να καλεί τις μεθόδους του MainController από το GUI (π.χ. όταν ο χρήστης πατάει ένα κουμπί) """
        self.ui = KinoGUI(self.root, self)

        # Καλείται η ask_initial_wallet για να ζητήσει από τον χρήστη να κάνει την αρχική του κατάθεση στο πορτοφόλι
        self.ask_initial_wallet()

        # Ύστερα καλείται η ask_initial_time_between_draws για να ζητήσει από τον χρήστη να ορίσει τον 
        # χρόνο μεταξύ των κληρώσεων, και να ενημερώσει το UI με αυτόν τον χρόνο
        self.ask_initial_time_between_draws()

        """ Τέλος, καλούμε τη μέθοδο load_payouts_table για να φορτώσει τον πίνακα κερδών από το payouts.json
        και να τον αποθηκεύσει στη μεταβλητή self.payouts_table. Χρησιμοποείται η εντολή try έτσι ώστε
        σε περίπτωση που υπάρξει κάποιο σφάλμα κατά τη φόρτωση του αρχείου (π.χ. το αρχείο δεν υπάρχει, ή έχει λάθος μορφή),
        να εμφανιστεί ένα μήνυμα σφάλματος στον χρήστη και να κλείσει η εφαρμογή με ασφάλεια. """
        try:
            """ Βρίσκει δυναμικά το path του αρχείου, έτσι ώστε να δημιουργούνται τα λιγότερα δυνατά
            προβλήματα κατά το άνοιγμα του. Ήταν απαραίτητο διότι όταν τρέχει το πρόγραμμα από διαφορετικό 
            σημείο (π.χ. από ένα IDE ή από το terminal), το σχετικό path μπορεί να μην λειτουργεί σωστά."""
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Δημιουργεί το σωστό, πλήρες μονοπάτι για το payouts.json
            payouts_path = os.path.join(current_dir, "payouts.json")

            # Εφόσον βρεθεί το path, ανοίγει το αρχείο και φορτώνει το περιεχόμενο του ως JSON, 
            # αποθηκεύοντας το στη μεταβλητή self.payouts_table
            with open(payouts_path, "r", encoding="utf-8") as f:
                self.payouts_table = json.load(f)

        except Exception as e: # Εάν υπάρξει οποιοδήποτε σφάλμα κατά τη διαδικασία φόρτωσης του αρχείου,
            # εμφανίζεται ένα μήνυμα σφάλματος στον χρήστη με πληροφορίες για το σφάλμα, και η εφαρμογή κλείνει.
            messagebox.showerror(
                "Κρίσιμο Σφάλμα",
                f"Αποτυχία φόρτωσης πίνακα κερδών (ψάξαμε στο: {payouts_path}):\n{e}")
            self.root.destroy()


    def ask_initial_wallet(self):
        """Εμφανίζει pop-up για να εισάγει  ο χρήστης τα χρήματα που έχει στο πορτοφόλι.
        Αν δεν βάλει χρήματα, κλείνει το παιχνίδι."""
        deposit = 0.0 #Το αρχικό ποσό του χρήστη είναι 0
        
        while deposit == None or deposit <= 0: # Αμυντικός προγραμματισμός: Επαναλαμβάνουμε το pop-up μέχρι να εισαχθεί ένα έγκυρο ποσό (μεγαλύτερο δηλαδή του 0)
            deposit = simpledialog.askfloat(
                "Αρχική Κατάθεση", 
                "Καλώς ήρθατε στο KINO!\n\nΠαρακαλώ εισάγετε το ποσό κατάθεσης (€):",
                minvalue=1.0,
                parent=self.root
            ) 
            
            # Αν ο χρήστης πατήσει "Cancel" ή κλείσει το παράθυρο, το deposit θα είναι None, οπότε εμφανίζεται ένα μήνυμα και κλείνει η εφαρμογή.
            if deposit is None:
                messagebox.showinfo("Έξοδος", "Πρέπει να κάνετε κατάθεση για να παίξετε. Κλείσιμο εφαρμογής.")
                self.root.destroy()
                raise SystemExit # Εξασφαλίζει ότι το πρόγραμμα θα σταματήσει ακόμα και αν για κάποιο λόγο δεν κλείσει το παράθυρο έτσι ώστε να μη κρασάρει η εφαρμογή
                # κατά το κλείσιμο της

            
        # Ενημερώνουμε τη βάση δεδομένων
        self.db.wallet = deposit
        # Και ύστερα ενημερώνουμε το UI για να εμφανίσει το νέο ποσό στο πορτοφόλι
        self.ui.update_wallet_display(self.db.wallet)

    def ask_initial_time_between_draws(self):
        """Εμφανίζει pop-up για να ρυθμίσει ο χρήστης τον χρόνο μεταξύ των κληρώσεων."""
        timer_seconds = 0 # Αρχική τιμή 0 για να μπει στο while και να ζητήσει την τιμή από τον χρήστη (αμυντικός προγραμματισμός)
        while timer_seconds is None or timer_seconds <= 0: # Έναρξη της δομής επανάληψης για την εισαγωγή του χρόνου μεταξύ των κληρώσεων. Επαναλαμβάνεται μέχρι να δοθεί μια έγκυρη τιμή (μεγαλύτερη του 0)
            timer_seconds = simpledialog.askinteger(
                "Ρύθμιση Χρόνου", 
                "Εισάγετε τον χρόνο μεταξύ των κληρώσεων (σε δευτερόλεπτα):",
                minvalue=1,       
                initialvalue=5,   
                parent=self.root
            )
            
            # Σε περίπτωση που ο χρήστης πατήσει "Cancel" ή κλείσει το παράθυρο, το timer_seconds θα 
            # είναι None, ξανα ζητάει την τιμή
            if timer_seconds is None:
                messagebox.showinfo("Έξοδος", "Ο ορισμός χρόνου είναι υποχρεωτικός. Εισάγετε μια έγκυρη τιμή.")

        
        # Ενημερώνουμε το λευκό κουτάκι στο UI για τον χρόνο
        self.ui.timer_entry.delete(0, tk.END)
        self.ui.timer_entry.insert(0, str(timer_seconds))

    def random_pick(self, count, draws=1): 
        # Είναι η συνάρτηση που καλείται για να δημιουργήσει ένα τυχαίο δελτίο όταν ο χρήστης 
        # πατάει το κουμπί "Τυχαία Επιλογή"
        # Παίρνουμε νέους αριθμούς από το script kino_logic
        self.ui.selected_numbers = self.logic.get_random_numbers(count)
        # Τους αποθηκεύουμε και καταχωρούμε το δελτίο στο UI με την add_ticket_to_sidebar
        self.ui.add_ticket_to_sidebar(self.ui.selected_numbers, draws)

    def on_start_click(self):
        # Είναι η συνάρτηση που καλείται όταν ο χρήστης πατήσει το κουμπί ΕΝΑΡΞΗ ΚΛΗΡΩΣΕΩΝ
        try:
            # Διαβάζουμε τις ρυθμίσεις που έχει δώσει ο χρήστης και είναι πλέον καταχωρημένες στο UI
            self.total_draws_to_play = int(self.ui.draws_entry.get()) # Ο αριθμός των κληρώσεν που θα παιχτούν
            self.timer_seconds = int(self.ui.timer_entry.get()) # Ο χρόνος μεταξύ των κληρώσεων
            self.bet_amount = float(self.ui.bet_entry.get()) # Το bet amount (παραμένει 1 ευρώ)
            
            # Έλεγος για το αν έχουν παιχτεί δελτία απο τον χρήστη. Αν δεν έχουν παιχτεί, επιστρέφει σφάλμα
            if not self.ui.paigmena_deltia:
                messagebox.showwarning("Προσοχή", "Πρέπει να δημιουργήσετε τουλάχιστον ένα δελτίο!")
                return
            
            # Ελέγχος αν το υπόλοιπο που υπάρχει στο πορτοφόλι επαρκεί για να παιχτούν τα δελτία που έχουν 
            # δημιουργηθεί, με βάση το bet amount και τον αριθμό των κληρώσεων που έχουν επιλέξει. Αν δεν 
            # επαρκεί, εμφανίζει προειδοποίηση.
            total_cost = 0
            for ticket_data in self.ui.paigmena_deltia.values():
                total_cost += self.bet_amount * ticket_data["draws"]
            if self.db.wallet < total_cost:
                messagebox.showwarning("Υπόλοιπο", f"Δεν έχετε αρκετά χρήματα!\nΑπαιτούνται {total_cost:.2f}€")
                return

            # Αφαιρούμε τα χρήματα του πάικτη απο το πορτοφόλι κατά την έναρξη του πονταρίσματος 
            self.db.wallet -= total_cost
            # Ενημερώνουμε το UI για να εμφανίσει το νέο υπόλοιπο του πορτοφολιού
            self.ui.update_wallet_display(self.db.wallet)

            # Κλειδώνουμε το κουμπί έναρξης για να μην πατηθεί ξανά και του αλλάζουμε το χρώμα σε γκρι
            # για να είναι εμφανές το κλείδωμα και στον χρήστη
            self.ui.start_btn.config(state="disabled", bg="#555555")
            # Όταν πατηθεί το κουμπί έναρξη, οι κληρώσεις που έχουν απομείνει να παιχτούν είναι ίδιες
            # με τις συνολικές που πρέπει να παιχτούν
            self.remaining_draws = self.total_draws_to_play
            
            # Σε αυτό το σημείο, ξεκινάμε τον κύκλο των κληρώσεων
            self.run_lottery_cycle()

        # Σε περίπτωση που ο χρήστης έχει εισάγει μη έγκυρες τιμές (π.χ. γράμματα αντί για αριθμούς), εμφανίζεται μήνυμα σφάλματος.
        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ ελέγξτε αν οι τιμές στα πεδία είναι σωστές.")

    #Υπολογισμός των κερδών με βάση τα νούμερα που κερδίζουν επί τον πολλαπλασιαστή στο json
    def calculate_win(self, played_count, hits, bet_amount):
        # Παίνριε τον πολλαπλασιαστή απο το payouts.json
        multiplier = (
            self.payouts_table
            .get(str(played_count), {})
            .get(str(hits), 0)
        )
        return multiplier * bet_amount # Επιστρέφει το κέρδος που προκύπτει από τον πολλαπλασιασμό του bet_amount με τον αντίστοιχο πολλαπλασιαστή από το payouts.json

    def run_lottery_cycle(self):
        # Συνάρτηση για την αρχή μιας κλήρωσης καθώς και προετοιμασία για την επόμενη 
        if self.remaining_draws > 0: # Αν οι κληρώσεις που απομένουν είναι περισσότερες απο 0

            # Αλλαγή της background εικόνας για τους αριθμούς που έχουν επιλεγεί (διότι όταν επιλέγονται 
            # αλλάζουν σε πορτοκαλί χρώμα)
            for i in range(1, 81):
                self.ui.buttons[i].configure(image=self.ui.icons.get("blue-circle"), bg="#001a33", fg="white")

            # Εκτέλεση κλήρωσης
            self.ui.win_list = self.logic.draw_winning_numbers() 
            self.ui.lottery_animation()

            # Αποθήκευση της κλήρωσης στη βάση δεδομένων για να έχουμε ιστορικό των κληρώσεων και να μπορούμε να 
            # βγάλουμε στατιστικά για τους λιγότερο επιλεμένους αριθμούς
            self.db.save_draw(self.ui.win_list)
            
            # Παίρνουμε το έτοιμο κείμενο με τους λιγότερο επιλεγμένους αριθμούς
            stats_info = self.db.get_top_20_delayed_numbers()
            
            # Το εμφανίζουμε στο δεξιά κάτω κουτί της εφαρμογής
            self.ui.update_statistics(stats_info)
            
            # Το κείμενου που θα εμφανιστεί στο ιστορικό των κληρώσεων για αυτή την κλήρωση.
            # Ξεκινάει με μια επικεφαλίδα 

            draw_results_text = "--- ΑΠΟΤΕΛΕΣΜΑΤΑ ΚΛΗΡΩΣΗΣ ---\n"
            total_draw_win = 0.0

            # Και μετά προστίθενται τα αποτελέσματα κάθε δελτίου
            for ticket_id, ticket_data in self.ui.paigmena_deltia.items():
                # Ελέγχουμε μόνο τα δελτία που έχουν ακόμα κληρώσεις που απομένουν και έχουν κληρώσεις
                if ticket_data["draws"] > 0:
                    # Μετατρέπουμε σε σύνολα τους αριθμούς του κάθε δελτίου και τους αριθμούς που 
                    # κέρδισαν για να χρησιμοποιήσουμε την τομή συνόλων και να βρούμε πόσους 
                    # αριθμούς έχει πετύχει το δελτίο
                    played_nums = set(ticket_data["arithmoi"])
                    winning_nums = set(self.ui.win_list)
                    
                    # Παίρνουμε την τομή τους και αποθηκεύουμε τον αριθμό των επιτυχιών
                    hits = played_nums.intersection(winning_nums)
                    num_hits = len(hits)
                    
                    # Μειώνουμε τις κληρώσεις του δελτίου
                    ticket_data["draws"] -= 1

                    # Ο αριθμός των παιγμένων αριθμών είναι το μήκος του συνόλου των αριθμών που έχει 
                    # παίξει ο χρήστης στο συγκεκριμένο δελτίο, και χρησιμοποιείται για τον υπολογισμό των κερδών 
                    # με βάση τον πίνακα κερδών στο payouts.json
                    played_count = len(played_nums)

                    # Καλείται η calculate_win για να υπολογίσει το ποσό που κερδίζει ο χρήστης 
                    # με βάση τον αριθμό των παιγμένων αριθμών, των επιτυχιών και του bet_amount
                    win_amount = self.calculate_win(
                        played_count,
                        num_hits,
                        self.bet_amount
                    )

                    # Αν ο χρήστης κέρδισε καποιο ποσό (άρα το win_amount > 0)
                    if win_amount > 0:
                        draw_results_text += f"Δελτίο {ticket_id}: {num_hits}/{len(played_nums)} επιτυχίες! ΚΕΡΔΟΣ: {win_amount:.2f}€\n"
                        total_draw_win += win_amount
                        self.db.wallet += win_amount # Ενημέρωση του πορτοφολιού με τα κέρδη
                    else: # Σε περίπτωση που δεν κέρδισε τίποτα
                        draw_results_text += f"Δελτίο {ticket_id}: {num_hits}/{len(played_nums)} επιτυχίες. (Χωρίς Κέρδος)\n"

            # Ενημέρωση UI του πορτοφολιού με τα κέρδη
            if total_draw_win > 0:
                self.ui.update_wallet_display(self.db.wallet)

            # Τοποθετεί νέα γραμμή και κάνει scroll στο τέλος του ιστορικού των κληρώσεων για να φανούν 
            # τα νέα αποτελέσματα
            draw_results_text += "\n"
            self.ui.history_text.insert(tk.END, draw_results_text)
            self.ui.history_text.see(tk.END) # Scroll στο τέλος

            # Ανανέωση του Sidebar όπου τηρούνται τα δελτία, για να μειωθούν οι κληρώσεις που απομένουν σε κάθε
            # δελτίο 
            self.ui.refresh_sidebar_tickets()
            
            # Μείωση κληρώσεων
            self.remaining_draws -= 1
            
            # Αν υπάρχουν κι άλλες κληρώσεις, ξεκινάει την αντίστροφη μέτρηση
            if self.remaining_draws > 0:
                self.start_countdown(self.timer_seconds) # Έναρξη της αντίστροφης μέτρησης
            else: # Αν δεν υπάρχουν άλλες κληρώσεις, εμφανίζει το μήνυμα ΟΛΟΚΛΗΡΩΘΗΚΕ στη θέση της αντίστροφης
                # μέτρησης, επιστρέφει το κουμπί ΕΝΑΡΞΗ ΚΛΗΡΩΣΕΩΝ στο αρχικό του χρώμα και εμφανίζει μήνυμα
                # στον χρήστη ότι όλες οι κληρώσεις ολοκληρώθηκαν
                self.ui.countdown_label.config(text="ΟΛΟΚΛΗΡΩΘΗΚΕ!")
                self.ui.start_btn.config(state="normal", bg="#28a745")
                messagebox.showinfo("Ολοκλήρωση", "Όλες οι κληρώσεις ολοκληρώθηκαν!")

    def start_countdown(self, seconds_left):
        #Η συνάρτηση που ενημερώνει το UI κάθε δευτερόλεπτο μέχρι την επόμενη κλήρωση
        if seconds_left > 0:
            # Ενημέρωση του κειμένου στο UI
            self.ui.countdown_label.config(text=f"Επόμενη κλήρωση σε: {seconds_left}")
            
            # Προγραμματισμός του επόμενου δευτερολέπτου (1000ms = 1sec)
            self.root.after(1000, lambda: self.start_countdown(seconds_left - 1))
        else:
            # Όταν ο χρόνος τελειώσει, καθάρισε το κείμενο και τρέξε τον κύκλο κλήρωσης
            self.ui.countdown_label.config(text="ΚΛΗΡΩΣΗ ΣΕ ΕΞΕΛΙΞΗ...")
            self.run_lottery_cycle()

if __name__ == "__main__": # Εδώ ξεκινάει το πρόγραμμα του ΚΙΝΟ
    root = tk.Tk()
    app = MainController(root)
    root.mainloop()