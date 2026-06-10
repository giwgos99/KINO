import random

class KinoLogic: # Η κλάση του KinoLogic 
    @staticmethod
    def get_random_numbers(count=6): # Παίρνουμε τυχαίους αριθμούς για το δελτίο, από το 1 έως το 80, 
        # χωρίς επανάληψη αφού στο πραγματικό παιχνίδι δεν μπορεί να "παιχτεί" ένας αριθμός πάνω απο 1
        # φορά.
        return random.sample(range(1, 81), count)

    @staticmethod
    def draw_winning_numbers():
        # Κληρώνει τους τους 20 νικητήριους αριθμούς
        return random.sample(range(1, 81), 20)

