import MetaTrader5 as mt5
from typing import Optional, Tuple
from google.protobuf.timestamp_pb2 import Timestamp
from mt5_grpc_proto.history_orders_pb2 import (
    HistoryOrdersRequest,
    HistoryOrdersResponse,
    HistoryOrdersTotalRequest,
    HistoryOrdersTotalResponse,
    HistoryOrder
)
from mt5_grpc_proto.history_orders_pb2_grpc import HistoryOrdersServiceServicer
from mt5_grpc_proto.common_pb2 import Error


class HistoryOrdersServiceImpl(HistoryOrdersServiceServicer):
    def __init__(self):
        pass

    def _convert_timestamp(self, unix_timestamp: int) -> Timestamp:
        """Convert Unix timestamp to protobuf Timestamp."""
        timestamp = Timestamp()
        timestamp.FromSeconds(unix_timestamp)
        return timestamp

    def _convert_order_to_proto(self, mt5_order) -> HistoryOrder:
        """Convert MT5 order object to protobuf HistoryOrder message.

        Args:
            mt5_order: Order information from MT5

        Returns:
            HistoryOrder: Protobuf HistoryOrder message
        """
        return HistoryOrder(
            ticket=mt5_order.ticket,
            time_setup=self._convert_timestamp(int(mt5_order.time_setup)),
            time_setup_msc=mt5_order.time_setup_msc,
            time_done=self._convert_timestamp(int(mt5_order.time_done)),
            time_done_msc=mt5_order.time_done_msc,
            time_expiration=self._convert_timestamp(int(mt5_order.time_expiration)) if mt5_order.time_expiration else None,
            type=mt5_order.type,
            type_time=mt5_order.type_time,
            type_filling=mt5_order.type_filling,
            state=mt5_order.state,
            magic=mt5_order.magic,
            position_id=mt5_order.position_id,
            volume_initial=float(mt5_order.volume_initial),
            volume_current=float(mt5_order.volume_current),
            price_open=float(mt5_order.price_open),
            stop_loss=float(mt5_order.sl),
            take_profit=float(mt5_order.tp),
            price_current=float(mt5_order.price_current),
            price_stoplimit=float(mt5_order.price_stoplimit),
            symbol=mt5_order.symbol,
            comment=mt5_order.comment,
            external_id=mt5_order.external_id
        )

    def GetHistoryOrders(self, request: HistoryOrdersRequest, context) -> HistoryOrdersResponse:
        """Get orders from trading history based on specified filters."""
        response = HistoryOrdersResponse()

        try:
            # Handle different filter types
            if request.HasField('time_filter'):
                orders = mt5.history_orders_get(
                    request.time_filter.date_from,
                    request.time_filter.date_to,
                    group=request.group if request.HasField('group') else '*'
                )
            elif request.HasField('ticket'):
                orders = mt5.history_orders_get(ticket=request.ticket)
            elif request.HasField('position'):
                orders = mt5.history_orders_get(position=request.position)
            else:
                response.error.code = -2  # RES_E_INVALID_PARAMS
                response.error.message = "No valid filter criteria provided"
                return response

            if orders is None:
                error_code, error_message = mt5.last_error()
                response.error.code = error_code
                response.error.message = f"Failed to get orders: {error_message}"
                return response

            # Convert MT5 orders to protobuf messages
            for mt5_order in orders:
                order_proto = self._convert_order_to_proto(mt5_order)
                response.orders.append(order_proto)

            return response

        except Exception as e:
            response.error.code = -1  # RES_E_FAIL
            response.error.message = f"Internal error processing orders: {str(e)}"
            return response

    def GetHistoryOrdersTotal(self, request: HistoryOrdersTotalRequest, context) -> HistoryOrdersTotalResponse:
        """Get total number of orders in trading history within specified period."""
        response = HistoryOrdersTotalResponse()

        try:
            total = mt5.history_orders_total(
                request.date_from,
                request.date_to
            )

            if total is None:
                error_code, error_message = mt5.last_error()
                response.error.code = error_code
                response.error.message = f"Failed to get orders total: {error_message}"
                return response

            response.total = total
            return response

        except Exception as e:
            response.error.code = -1  # RES_E_FAIL
            response.error.message = f"Internal error getting orders total: {str(e)}"
            return response