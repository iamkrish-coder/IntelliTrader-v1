import json

class Orders:
    def __init__(self, params):
        self.prop = params

    # Place a market order for a stock with given quantity
    def create_market_order(self, variety, exchange, symbol, transaction, quantity, product, order_type):
        if transaction == 'buy':
            transaction_type = self.prop['kite'].TRANSACTION_TYPE_BUY
        elif transaction == 'sell':
            transaction_type = self.prop['kite'].TRANSACTION_TYPE_SELL
        else:
            print("The order placement does not have a specified action to buy or sell.")
            exit()

        try:
            response = self.prop['kite'].place_order(
                variety=variety, 
                exchange=self.prop['kite'].EXCHANGE_NSE,
                tradingsymbol=symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                product=product, 
                order_type=order_type 
            )
            if "order_id" in response:
                order_id = response["order_id"]
                print("Market order placed successfully. Order ID:", order_id)
            else:
                error_message = response["error_type"] + ": " + response["message"]
                print("Market order placement failed. Error:", error_message)
        except Exception as e:
            print("An exception occurred while placing the market order:", e)

