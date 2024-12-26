import MetaTrader5 as mt5
from mt5_grpc_proto.order_check_pb2 import OrderCheckResponse, OrderCheckResult
from mt5_grpc_proto.order_check_pb2_grpc import OrderCheckServiceServicer
from mt5_grpc_proto.common_pb2 import Error


class OrderCheckServiceImpl(OrderCheckServiceServicer):
    def CheckOrder(self, request, context):
        """
        Check if an order can be executed
        """
        # Check order using mt5.order_check
        result = mt5.order_check(request.trade_request)

        # Check if check was successful
        if result is None:
            error = mt5.last_error()
            return OrderCheckResponse(
                error=Error(code=error[0], message=error[1])
            )

        # Convert result to OrderCheckResult
        check_result = OrderCheckResult(
            retcode=result.retcode,
            balance=result.balance,
            equity=result.equity,
            profit=result.profit,
            margin=result.margin,
            margin_free=result.margin_free,
            margin_level=result.margin_level,
            comment=result.comment,
            request=request.trade_request
        )

        return OrderCheckResponse(
            check_result=check_result,
            error=Error(code=0, message="")
        ) 