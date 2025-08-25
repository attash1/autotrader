#Setup
Create an Ngrok and Alpaca account and put your authentication tokens/API keys in .env, using the variable names shown in [example env.txt](https://github.com/attash1/autotrader/blob/main/example%20env.txt)
To use webhooks in TradingView, a paid account is needed. Alternatively, you can start a free trial

#TradingView Integration
Run the program. You should see a line in the output looking something like:
```
Ingress established at: https://e817fe5d8dc1.ngrok-free.app
```
Copy the link. This is the public endpoint for the autotrader, as Tradingview can't send alerts to localhost.

In TradingView, assuming you already have a strategy, create an alert for a stock of your choice, and have it set to go off on the conditions of your strategy.
In the notifications tab, check the box for Webhook URL and paste the link copied earlier from the program output.
