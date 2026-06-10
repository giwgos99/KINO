import json
import os

class KinoDB: # Η κλάση βάσης δεδομένων του ΚΙΝΟ
    def __init__(self):
        self.wallet = 0.0 # Το αρχικό ποσό του χρήστη στο πορτοφόλι είναι 0
        self.history_file = "kino_draw_history.json" # Το αρχείο που θα σώζονται οι κληρώσεις
        self.draws = self.load_draws() # Φορτώνει το ιστορικό αν υπάρχει ήδη

    def load_draws(self):
        # Διαβάζει τις παλιές κληρώσεις από το αρχείο kino_draw_history.json, αν υπάρχει
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def save_draw(self, winning_numbers):
        # Αποθηκεύει τη νέα κλήρωση στη μνήμη και στο αρχείο
        self.draws.append(winning_numbers) # Προσθέτει τα νούμερα που κέρδισαν στο history 
        with open(self.history_file, 'w') as f:
            json.dump(self.draws, f) # Τα αποθηκεύει στο αρχείο σε μορφή JSON

    def get_top_20_delayed_numbers(self):
        # Η συνάρτηση που υπολογίζει τους 20 αριθμούς που έχουν επιλεχθεί λιγότερο
        total_draws = len(self.draws) # Συνολικός αριθμός κληρώσεων που έχουν γίνει
        
        # Αν δεν έχει γίνει ακόμα καμία κλήρωση
        if total_draws == 0:
            return "Αναμονή για την 1η κλήρωση..."

        # Αρχικοποιούμε όλους τους αριθμούς (1-80) στο 0 (δεν έχουν εμφανιστεί)
        last_seen = {i: 0 for i in range(1, 81)}
        
        # Σαρώνουμε όλο το ιστορικό κληρώσεων. Για κάθε λοιπόν αριθμό που εμφανίζεται, ενημερώνουμε την 
        # τελευταία φορά που εμφανίστηκε (το index της κλήρωσης)
        for draw_index, numbers in enumerate(self.draws, start=1):
            for num in numbers:
                last_seen[num] = draw_index # Ενημερώνουμε την τελευταία φορά που εμφανίστηκε
                
        # Υπολογίζουμε την καθυστέρηση (Συνολικές κληρώσεις - Τελευταία εμφάνιση)
        delays = {}
        for num in range(1, 81): # Για κάθε αριθμό από το 1 έως το 80
            delays[num] = total_draws - last_seen[num] # Υπολογίζουμε πόσες κληρώσεις έχουν περάσει από 
            # την τελευταία εμφάνιση του αριθμού
            
        # Ταξινομούμε τα αποτελέσματα με φθίνουσα σειρά (ξεκινώντας απο τον πιο σπάνιο)
        sorted_delays = sorted(delays.items(), key=lambda item: item[1], reverse=True)
        
        # Κρατάμε μόνο τους πρώτους 20 αριθμούς 
        top_20 = sorted_delays[:20]
        
        # Φτιάχνουμε το κείμενο που θθα εμφανιστεί στο UI κάτω δεξιά
        stats_text = "--- 20 ΛΙΓΟΤΕΡΟ ΕΠΙΛΕΓΜΕΝΟΙ ΑΡΙΘΜΟΙ ---\n\n"
        stats_text += " ΝΟΥΜΕΡΟ | ΑΠΟΥΣΙΑΖΕΙ (ΚΛΗΡΩΣΕΙΣ)\n"
        stats_text += "-" * 35 + "\n"
        
        # Για κάθε αριθμό και την καθυστέρηση του, προσθέτουμε μια γραμμή στο κείμενο όπου
        # φαίνεται ο αριθμός και πόσες κληρώσεις έχει να εμφανιστεί
        for num, delay in top_20:
            stats_text += f" No {num:02d}    | {delay}\n"
            
        return stats_text