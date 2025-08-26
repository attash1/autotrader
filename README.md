# Setup
-Create a Ngrok and Alpaca account and put your authentication tokens/API keys in .env, using the variable names shown in [example env.txt](https://github.com/attash1/autotrader/blob/main/example%20env.txt)
-Create/generate a string to use as your secret. This will prevent requests made to the ngrok endpoint that aren't from you
-To use webhooks in TradingView, a paid account is needed. Alternatively, you can start a free trial

# TradingView Integration
Run the program. You should see a line in the output looking something like:
```
Ingress established at: https://e817fe5d8dc1.ngrok-free.app
```
Copy the link. This is the public endpoint for the autotrader, as Tradingview can't send alerts to localhost.

In TradingView, assuming you already have a strategy, create an alert for a stock of your choice, and have it set to go off on the conditions of your strategy.
Use the format in [example json payload.txt](https://github.com/attash1/autotrader/blob/main/example%20json%20payload.txt) as your message. In the example, if a 
variable is surrounded by braces, it will automatically be filled in by TradingView. For the secret, you will need to paste it yourself.
In the notifications tab, check the box for Webhook URL and paste the link copied earlier from the program output.

# Disclaimers
A DAY time-in-force is used. If a DAY order is placed after market hours, it will not be immediately executed. Instead, it would normally
be placed in a queue to be executed the next trading day. Prices may greatly shift during this time so for safety, after-hours orders
will be canceled
