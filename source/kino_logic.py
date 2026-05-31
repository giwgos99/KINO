import random

class KinoLogic:
    @staticmethod
    def get_random_numbers(count=6):
        """Επιστρέφει τυχαίους αριθμούς για το δελτίο"""
        return random.sample(range(1, 81), count)

    @staticmethod
    def draw_winning_numbers():
        """Κληρώνει τους 20 νικητήριους αριθμούς"""
        return random.sample(range(1, 81), 20)

