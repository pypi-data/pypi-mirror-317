import MetaTrader5 as mt5
from mt5_grpc_proto.order_calc_pb2 import OrderCalcMarginResponse, OrderCalcProfitResponse
from mt5_grpc_proto.order_calc_pb2_grpc import OrderCalcServiceServicer
from mt5_grpc_proto.common_pb2 import Error


class OrderCalcServiceImpl(OrderCalcServiceServicer):
    def CalcMargin(self, request, context):
        """
        Calculate margin required for a trading operation
        """
        # Calculate margin using mt5.order_calc_margin
        margin = mt5.order_calc_margin(
            request.action,
            request.symbol,
            request.volume,
            request.price
        )

        # Check if calculation was successful
        if margin is None:
            error = mt5.last_error()
            return OrderCalcMarginResponse(
                margin=0,
                error=Error(code=error[0], message=error[1])
            )

        return OrderCalcMarginResponse(
            margin=margin,
            error=Error(code=0, message="")
        )

    def CalcProfit(self, request, context):
        """
        Calculate potential profit for a trading operation
        """
        # Calculate profit using mt5.order_calc_profit
        profit = mt5.order_calc_profit(
            request.action,
            request.symbol,
            request.volume,
            request.price_open,
            request.price_close
        )

        # Check if calculation was successful
        if profit is None:
            error = mt5.last_error()
            return OrderCalcProfitResponse(
                profit=0,
                error=Error(code=error[0], message=error[1])
            )

        return OrderCalcProfitResponse(
            profit=profit,
            error=Error(code=0, message="")
        ) 