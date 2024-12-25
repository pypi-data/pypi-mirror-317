from common import fetch_orders_list, add_order_to_redis


def save_bt_report(app_db_cursor, report_dict):
    """Function to Save Backtest Report in Database"""
    try:
        app_db_cursor["bt_reports"].insert_one(report_dict)
        app_db_cursor["bt_request"].update_one({"_id": report_dict["request_id"]},
                                                 {"$set": {"status": "done"}})
    except Exception as e:
        print(f"Exception in saving BT Report : {e}")
        pass


def place_bt_order(rdb_cursor, order_candle, option_type, strike_price, position_type, quantity, transaction_type, order_type, exit_type=None, quantity_left=0, params=None, market_type="cash", trade_type=None, trigger_price=None, lot_size=25, user_id=None, strategy_id=None, request_id=None, exchange="NSE"):
    """ Function to place Backtesting Order """
    try:
        order_dict = {"exchange": exchange, "user_id": str(user_id), "strategy_id": str(strategy_id),
                      "request_id": str(request_id), "order_type": order_type, "position_type": position_type, "quantity": quantity,
                      "transaction_type": transaction_type, "option_type": option_type, "strike_price": strike_price,
                      "exit_type": exit_type, "quantity_left": quantity_left, "lot_size": lot_size,
                      "trade_type": trade_type}
        if trigger_price:
            order_dict["trigger_price"] = trigger_price
        else:
            order_dict["trigger_price"] = order_candle["close"]

        order_dict["order_timestamp"] = str(order_candle["timestamp"])
        order_dict["tradingsymbol"] = order_candle["symbol"]
        order_dict["date"] = str(order_candle["date"])
        if market_type == "cash":
            order_dict["expiry"] = ""
        else:
            order_dict["expiry"] = order_candle["expiry"]

        order_dict["day"] = order_candle["date"].strftime("%A")
        if params:
            order_dict.update(params)
        # logger.info(msg="* bt_order : {}".format(order_dict))
        # orders_list.append(order_dict)

        add_order_to_redis(rdb_cursor=rdb_cursor, request_id=str(request_id), order_dict=order_dict, mode="bt")
        orders_list = fetch_orders_list(rdb_cursor=rdb_cursor, request_id=str(request_id))

        return orders_list

    except Exception as e:
        print(f"Exception in placing backtesting order : {e}")
        pass

