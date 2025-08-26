from dotenv import load_dotenv
from flask import Flask, request, abort
import ngrok, os, time

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetAssetsRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.stream import TradingStream
import alpaca.common.exceptions

load_dotenv()

#creates endpoint with ngrok. TradingView can't send webhooks to localhost, so an endpoint is needed
listener = ngrok.forward("localhost:80", authtoken_from_env=True)
print(f"Ingress established at: {listener.url()}")

trading_client = TradingClient(os.getenv("API_KEY_ID"), os.getenv("API_KEY_SECRET"), paper=True)



app = Flask(__name__)

@app.route("/", methods=['GET'])
def test_func():
    return "<h1>You're supposed to send stuff here, not request it</h1>"

@app.route('/', methods=['POST'])
def webhook_response():
    account = trading_client.get_account()
    trade_info = request.json

    #prevents requests not originating from you
    if trade_info.get('secret') is None or trade_info['secret'] != os.getenv("WEBHOOK_SECRET"):
        abort(403)

    if trade_info['order_action'] == 'buy':
        try:
            buy_data = buy_setup(trade_info, account)
            buy_order = trading_client.submit_order(order_data=buy_data)

            #waits for order to be completed to get information about it
            while True:
                time.sleep(1)
                updated_buy_order = trading_client.get_order_by_id(buy_order.id)

                if updated_buy_order.status not in ['new', 'pending_new']:
                    break

            #returns information about completed order
            if updated_buy_order.status == 'filled':
                return_msg = f"{updated_buy_order.filled_qty} orders of {buy_order.symbol} filled at avg price of {updated_buy_order.filled_avg_price}"
            elif updated_buy_order.status == 'accepted':
                return_msg = "Market is currently closed. Order will not be executed"
                trading_client.cancel_order_by_id(buy_order.id)
            else:
                return_msg = f"Buy order status: {updated_buy_order.status}"

            return return_msg

        except alpaca.common.exceptions.APIError as error:
            return error.message


    elif trade_info['order_action'] == 'sell':
        try:
            sell_data = sell_setup(trade_info)
            sell_order = trading_client.submit_order(order_data=sell_data)

            # waits for order to be completed to get information about it
            while True:
                time.sleep(1)
                updated_sell_order = trading_client.get_order_by_id(sell_order.id)

                if updated_sell_order.status not in ['new', 'pending_new']:
                    break

            # returns information about completed order
            if updated_sell_order.status == 'filled':
                return_msg = f"{updated_sell_order.filled_qty} orders of {sell_order.symbol} sold at avg price of {updated_sell_order.filled_avg_price}"
            elif updated_sell_order.status == 'accepted':
                return_msg = "Market is currently closed. Order will not be executed"
                trading_client.cancel_order_by_id(sell_order.id)
            else:
                return_msg = f"Sell order status: {updated_sell_order.status}"

            return return_msg

        except alpaca.common.exceptions.APIError as error:
            return error.message

    else:
        return f"Invalid action {trade_info['order_action']}"


def buy_setup(trade_info, user_account) -> MarketOrderRequest: #purchases 5% of the account's balance worth of a security
    buy_order_data = MarketOrderRequest(
        symbol=trade_info['ticker'],
        notional=round(float(user_account.equity) * 0.05, 2),
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
    )
    return buy_order_data

def sell_setup(trade_info) -> MarketOrderRequest:
    position = trading_client.get_open_position(trade_info['ticker'])

    sell_order_data = MarketOrderRequest(
        symbol = trade_info['ticker'],
        qty = position.qty,
        side = OrderSide.SELL,
        time_in_force=TimeInForce.DAY
    )
    return sell_order_data





if __name__ == '__main__':
    app.run(port=80)




