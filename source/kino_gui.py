import tkinter as tk
import os
from tkinter import *
from tktooltip import ToolTip # Εξωτερική βιβλιοθήκη για tooltips, εγκατάσταση με: pip install tkinter-tooltip

class KinoGUI: # Η κλάση του KinoGui
    def __init__(self, root, controller):
        self.root = root # root είναι το main.py 
        self.controller = controller # controller επίσης είναι το main.py
        self.root.title("KINO") # Ο τίτλος του παραθύρου
        self.root.geometry("1100x700") # Το ύψος και το πάχος του παραθύρου που εμφανίζεται η εφαρμογή
        self.root.configure(bg="#001a33") # Το background χρώμα της εφαρμογής

        self.selected_numbers = [] # Αρχικοποίηση της λίστας των επιλεγμένων αριθμών

        self.buttons = {} # Τα κουμπιά του UI
        self.remaining_draws = 0 # Οι κληρώσεις που απομένουν
        self.total_draws_to_play = 0  # Οι συνολικές κληρώσεις για να παιχτούν με την έναρξη του παιχνιδιού
        self.win_list = [] # Η λίστα των αριθμών που κέρδισαν
        self.icons = {} # Τα εικονίδια που έχουμε εισα
        self.paigmena_deltia = {} # Τα δελτία που έχει παίξει ο χρήστης (λεξικό)
        
        self.setup_ui() # Καλείται η συνάρτηση για να "σχεδιαστεί" το αρχικό UI

    def setup_ui(self):
        # Αρχκά εισάγονται τα εικονίδια που θα χρησιμοποιηθούν στην εφαρμογη έτσι ώστε να 
        # χρησιμοποιείται εύκολα και γρήγορα και να μη χρειάζεται κάθε φορά να γράφουμε το path 
        # Βρίσκουμε το απόλυτο μονοπάτι του φακέλου που περιέχει αυτό το αρχείο Python
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Φτιάχνουμε το δυναμικό μονοπάτι για τον φάκελο "icons"
        icons_dir = os.path.join(current_dir, "icons")

        try:
            self.icons["wallet"] = tk.PhotoImage(file=os.path.join(icons_dir, "icon-wallet.png")).subsample(15, 15)
            self.icons["bet"] = tk.PhotoImage(file=os.path.join(icons_dir, "icon-bet.png")).subsample(12, 12)
            self.icons["clock"] = tk.PhotoImage(file=os.path.join(icons_dir, "icon-clock.png")).subsample(17, 17)
            self.icons["number_of_games"] = tk.PhotoImage(file=os.path.join(icons_dir, "icon-number_of_games.png")).subsample(15, 15)
            self.icons["yellow_circle"] = tk.PhotoImage(file=os.path.join(icons_dir, "icon-yellow-circle.png")).subsample(11, 11)
            self.icons["blue-circle"] = tk.PhotoImage(file=os.path.join(icons_dir, "icon-blue-circle.png")).subsample(13, 13)
            
        except tk.TclError as e:
            #  To error που θα εμφανιστεί σε περίπτωση που δεν βρεθούν τα εικονίδια ή υπάρχει 
            # πρόβλημα με την φόρτωσή τους
            print(f"Προσοχή: Αποτυχία φόρτωσης εικονιδίων. {e}")

        self.aorato_pixel = tk.PhotoImage(width=1, height=1) # Τοποθετούμε ένα "αόρατο" pixel που θα 
        #χρησιμοποιηθεί αργότερα για να καλύψει μέρος των εικονιδίων

        # Δημιουργούμε το Frame όπου θα γράφεται ο τίτλος της εφαρμογής (ΚΙΝΟ) και αλλάζουμε και τη 
        # γραμματοσειρά που θα χρησιμοποιηθεί
        header = tk.Frame(self.root, bg="#001a33")
        header.pack(pady=0)
        tk.Label(header, text="KINO", font=("Times New Roman", 45, "bold"), fg="#ffcc00", bg="#001a33").pack()

        settings_frame = tk.Frame(self.root, bg="#003366", padx=15, pady=15, highlightbackground="#ffcc00", highlightthickness=1)
        settings_frame.pack(pady=5, fill="x", padx=40)

        # Δημιουργώ ένα εσωτερικό frame για να κεντράρουμε τα στοιχεία που βρίσκονται απο κάτω (Πορτοφόλι,
        # Το ποντάρισμα, ο χρόνος και το πλήθος των παιχνιδιών που θα παιχτούν)
        eswteriko_settings_frame = tk.Frame(settings_frame, bg="#003366")
        eswteriko_settings_frame.pack(anchor="center")

        # ---  Πορτοφόλι ---
        self.wallet_icon_label = tk.Label(eswteriko_settings_frame, image=self.icons.get("wallet"), bg="#003366")
        self.wallet_icon_label.grid(row=0, column=0, padx=(0, 5)) # Μικρό κενό ανάμεσα σε εικόνα και κουτάκι
        
        self.wallet_entry = tk.Entry(eswteriko_settings_frame, width=7, font=("Arial", 11, "bold"), justify="center")
        self.wallet_entry.insert(0, f"{self.controller.db.wallet:.2f}") 
        self.wallet_entry.grid(row=0, column=1, padx=(0, 40)) # Μεγάλο κενό δεξιά για να χωρίσει από την επόμενη κατηγορία
        ToolTip(self.wallet_icon_label, msg=" Πορτοφόλι (€)", delay=0.4)

        # --- Ποντάρισμα ---
        self.bet_icon_label = tk.Label(eswteriko_settings_frame, image=self.icons.get("bet"), bg="#003366")
        self.bet_icon_label.grid(row=0, column=2, padx=(0, 5))
        
        self.bet_entry = tk.Entry(eswteriko_settings_frame, width=7, font=("Arial", 11, "bold"), justify="center")
        self.bet_entry.insert(0, "1.00")
        self.bet_entry.grid(row=0, column=3, padx=(0, 40))
        ToolTip(self.bet_icon_label, msg=" Ποντάρισμα (€)", delay=0.4)

        # --- Χρόνος μεταξύ κληρώσεων ---
        self.timer_icon_label = tk.Label(eswteriko_settings_frame, image=self.icons.get("clock"), bg="#003366")
        self.timer_icon_label.grid(row=0, column=4, padx=(0, 5))
        
        self.timer_entry = tk.Entry(eswteriko_settings_frame, width=7, font=("Arial", 11, "bold"), justify="center")
        self.timer_entry.insert(0, "5")
        self.timer_entry.grid(row=0, column=5, padx=(0, 40))
        ToolTip(self.timer_icon_label, msg=" Sec/Κλήρωση", delay=0.4)

        # --- Πλήθος Παιχνιδιών ---
        self.draws_icon_label = tk.Label(eswteriko_settings_frame, image=self.icons.get("number_of_games"), bg="#003366")
        self.draws_icon_label.grid(row=0, column=6, padx=(0, 5))
        
        self.draws_entry = tk.Entry(eswteriko_settings_frame, width=7, font=("Arial", 11, "bold"), justify="center")
        self.draws_entry.insert(0, "5")
        self.draws_entry.grid(row=0, column=7)
        ToolTip(self.draws_icon_label, msg=" Παιχνίδια", delay=0.4)

        self.countdown_label = tk.Label(eswteriko_settings_frame, text="", font=("Arial", 14, "bold"), 
                                        fg="#ffcc00", bg="#001a33", width=20, justify="center")
        self.countdown_label.grid(row=1, column=0, columnspan=8, pady=(15, 0))


        # --- ΚΕΝΤΡΙΚΟΣ ΧΩΡΟΣ (Διαχωρίζομυε και σε δύο μέρη: Αριστερά - Δεξιά) ---
        main_content_frame = tk.Frame(self.root, bg="#001a33")
        main_content_frame.pack(pady=5, fill="x", padx=40)

        # 1. Αριστερό κομμάτι (Το μεγάλο Grid προβολής)
        left_panel = tk.Frame(main_content_frame, bg="#001a33")
        left_panel.pack(side="left", expand=True)

        grid_container = tk.Frame(left_panel, bg="#001a33")
        grid_container.pack()
        
        # Δομή επανάληψης για τον κάθε αριθμό απο το 1 έως το 80. Για κάθε αριθμό, φτιάχνει ένα κουμπί
        # με συγκεκριμένο background χρώμα. Επίσης τους προσθέτουμε background εικονίδιο ο γαλάζιο μπλε
        # εφόσον ακόμα σε αυτό το σημείο δεν έχει γίνει κλήρωση
        for i in range(1, 81):
            btn = tk.Button(grid_container, 
                            text=str(i), 
                            image=self.icons.get("blue-circle"), # Βάζουμε το background εικονίδιο
                            compound="center",         
                            width=30, height=30,       
                            font=("Arial", 10, "bold"), 
                            bg="#001a33", 
                            fg="white",
                            relief="flat")
            # Φτιάχνουμε το grid με γραμμές και στύλες
            row = (i - 1) // 10
            col = (i - 1) % 10
            btn.grid(row=row, column=col, padx=4, pady=2)
            self.buttons[i] = btn

        actions = tk.Frame(left_panel, bg="#001a33")
        actions.pack(pady=20)

        # Τα κουμπιά συνδέονται με τον controller που έχουμε αρχικοποιήσει κατά το ξεκίνημα του προγράμματος
        self.random_btn = tk.Button(actions, text="ΤΥΧΑΙΑ ΕΠΙΛΟΓΗ", font=("Arial", 11, "bold"), bg="#ffcc00", width=18,
                                    command=self.toggle_random_options)
        self.random_btn.pack(side="left", padx=10)

        # Δημιουργούμε και ένα ακόμα κουμπί το οποίο όμως ΔΕΝ του κάνουμε .pack() ακόμα και άρα δεν εμφανίζονται
        self.random_opt_frame = tk.Frame(actions, bg="#001a33")
        
        tk.Label(self.random_opt_frame, text="Αριθμοί:", font=("Arial", 10, "bold"), fg="white", bg="#001a33").pack(side="left")
        
        # Δημιουργούμε κουτί με βελάκια πάνω και κάτω έτσι ώστε να είναι ευκολότερη η επιλογή του πόσους
        # αριθμούς θέλουμε να επιλέξουμε τυχαία
        self.random_spinbox = tk.Spinbox(self.random_opt_frame, from_=1, to=12, width=3, font=("Arial", 11, "bold"), justify="center")
        self.random_spinbox.pack(side="left", padx=5)

        # Δημιουργούμε επίσης κουτί με βελάκια πάνω και κάτω έτσι ώστε να είναι ευκολότερη η επιλογή του 
        # πόσες κληρώσεις θέλουμε να ισχύει το τυχαίο δελτίο που φτιάχνεται
        tk.Label(self.random_opt_frame, text="Κληρώσεις:", font=("Arial", 10, "bold"), fg="white", bg="#001a33").pack(side="left", padx=5)
        self.random_opt_draws_spinbox = tk.Spinbox(self.random_opt_frame, from_=1, to=200, width=5, font=("Arial", 11, "bold"), justify="center")
        self.random_opt_draws_spinbox.pack(side="left", padx=5)

        # Το κουμπί OK (Το πράσινο τικ) που καταχωρεί το δελτίο
        tk.Button(self.random_opt_frame, text="✓", font=("Arial", 11, "bold"), bg="#28a745", fg="white", 
                  command=self.confirm_random_pick).pack(side="left")
                  
        tk.Button(actions, text="RESET", font=("Arial", 11, "bold"), bg="#ffcc00", width=18,
                  command=self.reset_button).pack(side="left", padx=10)
                  
        self.start_btn = tk.Button(actions, text="ΕΝΑΡΞΗ ΚΛΗΡΩΣΕΩΝ", font=("Arial", 11, "bold"), bg="#28a745",
                                   fg="white", width=22, command=self.controller.on_start_click)
        self.start_btn.pack(side="left", padx=10)

        # Δεξί κομμάτι (Sidebar για Δελτία)
        right_panel = tk.Frame(main_content_frame, bg="#002244", highlightbackground="#ffcc00", highlightthickness=1)
        right_panel.pack(side="right", fill="y", ipadx=20, ipady=20, padx=20)

        tk.Label(right_panel, text="ΤΑ ΔΕΛΤΙΑ ΜΟΥ", font=("Arial", 14, "bold"), fg="#ffcc00", bg="#002244").pack(pady=(0, 15))

        # Το κουμπί για τη δημιουργία νέου δελτίου που ανοίγει το pop-up παράθυρο
        tk.Button(right_panel, text="Δημιουργία Δελτίου +", font=("Arial", 12, "bold"), bg="#28a745", fg="white",
                  cursor="hand2", command=self.open_ticket_popup).pack(fill="x", pady=5)
                  
        # Εδώ εμφανίζονται τα δελτία μόλις τα φτιάχνουμε
        self.tickets_display = tk.Frame(right_panel, bg="#002244")
        self.tickets_display.pack(fill="both", expand=True, pady=10)

        output_frame = tk.Frame(self.root, bg="#001a33")
        output_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        self.history_text = tk.Text(output_frame, height=10, bg="#002244", fg="#00ffcc", font=("Consolas", 11))
        self.history_text.pack(side="left", fill="both", expand=True, padx=5)
        self.stats_text = tk.Text(output_frame, height=10, width=40, bg="#002244", fg="#ffcc00", font=("Consolas", 11))
        self.stats_text.pack(side="left", fill="both", expand=True, padx=5)

    def toggle_lot_number(self, num): # Συνάρτηση που αλλάζει το background των αριθμών που
        # έχουν επιλεγεί σε κίτρινο - πορτοκαλί background
        self.buttons[num].configure(image=self.icons.get("yellow_circle"), bg="#001a33", fg="black")
        
    def lottery_animation(self): # Συνάρτηση που καλείται για να εμφανίσει ένα μικρό "animation" με τους 
        # αριθμούς που έχουν επιλεγεί. Έπρεπε να προσομοιάζει τις αναπηδήσεις που κάνει το πορτοκαλί
        # κυκλάκι σε τυχαίος αριθμούς μέχρι να επιλεγεί ο τελικός
        for number in self.win_list:
            self.toggle_lot_number(number)

    def reset_button(self): # Συνάρτηση που καθαρίζει τα δελτία που έχουν παιχτεί καθώς και τους αριθμούς που έχουν 
        # επιλεγεί
        self.paigmena_deltia.clear()
        for widget in self.tickets_display.winfo_children():
            widget.destroy()

        for button in self.buttons: # Αλλάζει τα background
            self.buttons[button].configure(image=self.icons.get("blue-circle"), bg="#001a33", fg="white")


    def toggle_random_options(self):
        # Εμφανίζει ή κρύβει το μενού της τυχαίας επιλογής
        # Το winfo_ismapped() μας λέει αν το frame φαίνεται αυτή τη στιγμή
        if not self.random_opt_frame.winfo_ismapped():
            # Αν δεν φαίνεται, το βάζουμε να εμφανιστεί δεξιά του κουμπιού ΤΥΧΑΙΑ ΕΠΙΛΟΓΗ
            self.random_opt_frame.pack(side="left", after=self.random_btn, padx=(0, 10))
        else:
            # Αν φαίνεται ήδη, το κρύβει
            self.random_opt_frame.pack_forget()

    def confirm_random_pick(self):
        # Διαβάζει τον αριθμό και δίνει εντολή στον controller να φτιάξει ένα τυχαίο δελτίο με βάση τις επιλογές του χρήστη
        try:
            count = int(self.random_spinbox.get())
            if count < 1 or count > 12: # Σε περίπτωση που ο χρήστης έχει δώσει τιμή εκτός ορίων, 
                #εμφανίζει προειδοποίηση και επιστρέφει χωρίς να κάνει τίποτα
                raise ValueError
        except ValueError: # Το μήνυμα που θα εμφανίζει αν ο χρήστης έκανε το παραπάνω σφάλμα
            from tkinter import messagebox
            messagebox.showwarning("Προσοχή", "Επιλέξτε από 1 έως 12 αριθμούς.")
            return
        
        try: # Ελέγχουμε αν οι κληρώσεις που έχει δώσει ο χρήστης είναι έγκυρος αριθμός 
            # και αν είναι μέσα στα όρια (1-200)
            draws = int(self.random_opt_draws_spinbox.get())
            if draws < 1 or draws > 200:
                raise ValueError
        except ValueError: # Αλλιώς επιστρέφει error
            from tkinter import messagebox
            messagebox.showwarning("Προσοχή", "Επιλέξτε από 1 έως 200 κληρώσεις.")
            return
            
        # Στέλνουμε τον αριθμό (π.χ. 6) και τις κληρώσεις (π.χ. 10) στον Controller
        self.controller.random_pick(count, draws)
        
        # Κρύβουμε πάλι το μενού στο γραφικό περιβάλλον
        self.random_opt_frame.pack_forget()

    def add_ticket_to_sidebar(self, numbers, draws=1):
        # Κεντρική συνάρτηση που προσθέτει ένα έτοιμο δελτίο στη δεξιά μπάρα
        # Αποθηκεύουμε το δελτίο στη λίστα μας
        
        deltio = {"arithmoi": sorted(numbers), "draws": draws}
        self.paigmena_deltia[len(self.paigmena_deltia) + 1] = deltio
        ticket_number = len(self.paigmena_deltia)
        
        # Φτιάχνουμε το κείμενο που θα εμφανίζεται στο δελτίο(π.χ. 4 - 15 - 22 - 67)
        nums_str = " - ".join(str(n) for n in sorted(numbers))
        
        # Το εμφανίζει στο sidebar των δελτίων
        tk.Label(self.tickets_display, text=f"Δελτίο {ticket_number} (Κληρώσεις που απομένουν: {draws} ):\n{nums_str}", 
                 font=("Arial", 10, "bold"), bg="#003366", fg="#00ffcc", 
                 relief="solid", borderwidth=1, padx=5, pady=5).pack(fill="x", pady=5)

    def refresh_sidebar_tickets(self):
        # Καθαρίζει το sidebar και εμφανίζει τα ενεργά δελτία
        # Καθαρίζουμε τα παλιά δελτία
        for widget in self.tickets_display.winfo_children():
            widget.destroy()
            
        # Φτιάχνουμε τα νέα δελτία (όσα έχουν ακόμα κληρώσεις)
        for ticket_number, ticket_draws in self.paigmena_deltia.items():
            if ticket_draws["draws"] > 0:
                nums_str = " - ".join(str(n) for n in self.paigmena_deltia[ticket_number]["arithmoi"])
                tk.Label(self.tickets_display, text=f"Δελτίο {ticket_number} (Κληρώσεις που απομένουν: {ticket_draws["draws"]} ):\n{nums_str}", 
                         font=("Arial", 10, "bold"), bg="#003366", fg="#00ffcc", 
                         relief="solid", borderwidth=1, padx=5, pady=5).pack(fill="x", pady=5)

    def update_wallet_display(self, new_balance): # Ενημερώνει το πορτοφόλι με το νέο υπόλοιπο μετά 
        # από κάθε κλήρωση
        self.wallet_entry.delete(0, tk.END)
        self.wallet_entry.insert(0, f"{new_balance:.2f}")

    def update_statistics(self, stats_data): # Ενημερώνει τα στατιστικά με τα νέα δεδομένα που υπολογίζει
        # ο controller μετά από κάθε κλήρωση
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, stats_data)

    def open_ticket_popup(self): # Συνάρτηση που ανοίγει το παράθυρο για τη δημιουργία νέου δελτίου
        # Δημιουργία του αναδυόμενου παραθύρου
        popup = tk.Toplevel(self.root)
        popup.title("Νέο Δελτίο") # Τίτλος του νέου παραθύρου
        popup.geometry("800x500")
        popup.configure(bg="#001a33")
        
        # Αυτό το κάνει "Modal" και ο χρήστης δεν μπορεί αν πατήσει πουθενά αλλού μέχρι να το κλείσει
        popup.grab_set() 

        tk.Label(popup, text="Επιλέξτε έως 12 αριθμούς", font=("Arial", 16, "bold"), fg="#ffcc00", bg="#001a33").pack(pady=15)

        # Τοπικές μεταβλητές ΜΟΝΟ για αυτό το pop-up
        temp_selected = []
        temp_buttons = {}

        # Εσωτερική συνάρτηση για τα κλικ στο μικρό grid
        def toggle_popup_num(num):
            if num in temp_selected:
                temp_selected.remove(num)
                temp_buttons[num].configure(bg="#004488", fg="white")
            elif len(temp_selected) < 12:
                temp_selected.append(num)
                temp_buttons[num].configure(bg="#ffcc00", fg="black")

        # Το μικρό πλέγμα
        small_grid = tk.Frame(popup, bg="#001a33")
        small_grid.pack(pady=10)

        for i in range(1, 81):
            # Χρησιμοποιούμε μικρότερο μέγεθος για να χωράει το grid στο μικρότερο pop-up
            btn = tk.Button(small_grid, text=str(i), width=3, height=1,
                            font=("Arial", 9, "bold"), bg="#004488", fg="white",
                            relief="flat", cursor="hand2",
                            command=lambda n=i: toggle_popup_num(n))
            row = (i - 1) // 10
            col = (i - 1) % 10
            btn.grid(row=row, column=col, padx=2, pady=2)
            temp_buttons[i] = btn
        draws_frame = tk.Frame(popup, bg="#001a33")
        draws_frame.pack(pady=5)
        
        tk.Label(draws_frame, text="Συνεχόμενες Κληρώσεις:", font=("Arial", 11, "bold"), fg="white", bg="#001a33").pack(side="left", padx=5)
        
        ticket_draws_spinbox = tk.Spinbox(draws_frame, from_=1, to=200, width=5, font=("Arial", 11, "bold"), justify="center")
        ticket_draws_spinbox.pack(side="left")

        # Εσωτερική συνάρτηση για αποθήκευση
        def save_ticket(): 
            # Ελέγχουμε αν ο χρήστης έχει επιλέξει τουλάχιστον έναν αριθμό και αν έχει δώσει έγκυρο 
            # αριθμό κληρώσεων
            if not temp_selected: # Αν δεν έχει επιλέξει κανέναν αριθμό, εμφανίζει προειδοποίηση και 
                # επιστρέφει χωρίς να κάνει τίποτα
                from tkinter import messagebox
                messagebox.showwarning("Προσοχή", "Επιλέξτε τουλάχιστον έναν αριθμό!", parent=popup)
                return
        
            try: # Ελέγχουμε αν οι κληρώσεις που έχει δώσει ο χρήστης είναι έγκυρος αριθμός και 
                # αν είναι μέσα στα όρια (1-200)
                draws_chosen = int(ticket_draws_spinbox.get())
                if draws_chosen < 1: # Αν ο χρήστης ΔΕΝ έχει εισάγει έγκυρο αριθμό κληρώσεων
                    raise ValueError
            except ValueError: # Εμφανίζει το error της παραπάνω περίπτωσης
                from tkinter import messagebox
                messagebox.showwarning("Προσοχή", "Εισάγετε έναν έγκυρο αριθμό κληρώσεων!", parent=popup)
                return
                
            # Δημιουργούμε το δελτίο με τους επιλεγμένους αριθμούς, τον αριθμό κληρώσεων και το περνάμε
            # στο δεξιά sidebar με τα δελτία
            self.add_ticket_to_sidebar(temp_selected, draws=draws_chosen)
            
            popup.destroy() # Κλείνει το pop-up παράθυρο

        # Κουμπιά ελέγχου του pop-up
        popup_actions = tk.Frame(popup, bg="#001a33")
        popup_actions.pack(pady=20)
        
        tk.Button(popup_actions, text="ΑΚΥΡΟ", font=("Arial", 10, "bold"), bg="#dc3545", fg="white", 
                  width=10, command=popup.destroy).pack(side="left", padx=10)
                  
        tk.Button(popup_actions, text="ΚΑΤΑΧΩΡΗΣΗ", font=("Arial", 10, "bold"), bg="#28a745", fg="white", 
                  width=15, command=save_ticket).pack(side="left", padx=10)