import json
import os

class KinoDB:
    def __init__(self):
        self.wallet = 0.0
        self.history_file = "kino_draw_history.json" # Το αρχείο που θα σώζονται οι κληρώσεις
        self.draws = self.load_draws() # Φορτώνει το ιστορικό αν υπάρχει ήδη

    def load_draws(self):
        """Διαβάζει τις παλιές κληρώσεις από το αρχείο, αν υπάρχει"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def save_draw(self, winning_numbers):
        """Αποθηκεύει τη νέα κλήρωση στη μνήμη και στο αρχείο"""
        self.draws.append(winning_numbers)
        with open(self.history_file, 'w') as f:
            json.dump(self.draws, f)

    def get_top_20_delayed_numbers(self):
        """Υπολογίζει τους 20 αριθμούς με τη μεγαλύτερη καθυστέρηση εμφάνισης"""
        total_draws = len(self.draws)
        
        # Αν δεν έχει γίνει ακόμα καμία κλήρωση
        if total_draws == 0:
            return "Αναμονή για την 1η κλήρωση..."

        # 1. Αρχικοποιούμε όλους τους αριθμούς (1-80) στο 0 (ότι δηλαδή τους είδαμε στην "0" κλήρωση)
        last_seen = {i: 0 for i in range(1, 81)}
        
        # 2. Σαρώνουμε όλο το ιστορικό κληρώσεων
        for draw_index, numbers in enumerate(self.draws, start=1):
            for num in numbers:
                last_seen[num] = draw_index # Ενημερώνουμε την τελευταία φορά που εμφανίστηκε
                
        # 3. Υπολογίζουμε την καθυστέρηση (Συνολικές κληρώσεις - Τελευταία εμφάνιση)
        delays = {}
        for num in range(1, 81):
            delays[num] = total_draws - last_seen[num]
            
        # 4. Ταξινομούμε τα αποτελέσματα με φθίνουσα σειρά (από τη μεγαλύτερη καθυστέρηση στη μικρότερη)
        sorted_delays = sorted(delays.items(), key=lambda item: item[1], reverse=True)
        
        # 5. Κρατάμε μόνο τους πρώτους 20
        top_20 = sorted_delays[:20]
        
        # 6. Φτιάχνουμε το κείμενο που θα πάει στο UI
        stats_text = "--- 20 ΛΙΓΟΤΕΡΟ ΕΠΙΛΕΓΜΕΝΟΙ ΑΡΙΘΜΟΙ ---\n\n"
        stats_text += " ΝΟΥΜΕΡΟ | ΑΠΟΥΣΙΑΖΕΙ (ΚΛΗΡΩΣΕΙΣ)\n"
        stats_text += "-" * 35 + "\n"
        
        for num, delay in top_20:
            stats_text += f" No {num:02d}    | {delay}\n"
            
        return stats_text