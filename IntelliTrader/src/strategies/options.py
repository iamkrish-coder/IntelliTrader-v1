from src.helper import Helper
import src.strategies.shared as shared

def nifty_scalper(dataset):
    if dataset:
        common_utils = dataset['common_utils']
        user_input = dataset['user_input']

        option_chain = shared.get_option_chain()
    


