import MetaTrader5 as mt5
from datetime import datetime
from typing import Optional, Tuple, Union
from google.protobuf.timestamp_pb2 import Timestamp
from mt5_grpc_proto.common_pb2 import Error
from mt5_grpc_proto.order_pb2 import (
    OrdersGetRequest,
    OrdersGetResponse,
    OrdersTotalRequest,
    OrdersTotalResponse,
    Order
)
from mt5_grpc_proto.order_pb2_grpc import OrdersServiceServicer


class OrdersServiceImpl(OrdersServiceServicer):
    """Implementation of Orders service for MetaTrader 5."""

    def __init__(self):
        pass

    def _to_timestamp(self, time_value: Union[int, datetime, None]) -> Optional[Timestamp]:
        """Convert various time formats to Protobuf Timestamp.

        Args:
            time_value: Time value as Unix timestamp (int) or datetime object

        Returns:
            Optional[Timestamp]: Protobuf timestamp or None if input is None
        """
        if time_value is None:
            return None

        timestamp = Timestamp()
        if isinstance(time_value, int):
            # Handle Unix timestamp (seconds since epoch)
            timestamp.FromSeconds(time_value)
        elif isinstance(time_value, datetime):
            # Handle datetime object
            timestamp.FromDatetime(time_value)
        return timestamp

    def _convert_order_to_proto(self, mt5_order) -> Order:
        """Convert MT5 order object to protobuf Order message.

        Args:
            mt5_order: Order information from MT5

        Returns:
            Order: Protobuf Order message
        """
        order = Order(
            ticket=mt5_order.ticket,
            time_setup_msc=mt5_order.time_setup_msc,
            time_done_msc=mt5_order.time_done_msc,
            type=mt5_order.type,
            type_time=mt5_order.type_time,
            type_filling=mt5_order.type_filling,
            state=mt5_order.state,
            magic=mt5_order.magic,
            volume_current=float(mt5_order.volume_current),
            price_open=float(mt5_order.price_open),
            stop_loss=float(mt5_order.sl),
            take_profit=float(mt5_order.tp),
            price_current=float(mt5_order.price_current),
            symbol=mt5_order.symbol,
            comment=mt5_order.comment,
            external_id=mt5_order.external_id
        )

        # Convert timestamp fields
        time_setup = self._to_timestamp(mt5_order.time_setup)
        if time_setup:
            order.time_setup.CopyFrom(time_setup)

        time_done = self._to_timestamp(mt5_order.time_done)
        if time_done:
            order.time_done.CopyFrom(time_done)

        time_expiration = self._to_timestamp(mt5_order.time_expiration)
        if time_expiration:
            order.time_expiration.CopyFrom(time_expiration)

        return order

    def GetOrders(self, request: OrdersGetRequest, context) -> OrdersGetResponse:
        """Get orders from MT5 based on specified filters."""
        response = OrdersGetResponse()

        try:
            # Apply filters according to MT5 reference
            if request.HasField('ticket'):
                orders = mt5.orders_get(ticket=request.ticket)
            elif request.HasField('symbol'):
                orders = mt5.orders_get(symbol=request.symbol)
            elif request.HasField('group'):
                orders = mt5.orders_get(group=request.group)
            else:
                # If no filters specified, get all orders
                orders = mt5.orders_get()

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

    def GetOrdersTotal(self, request: OrdersTotalRequest, context) -> OrdersTotalResponse:
        """Get total number of active orders."""
        response = OrdersTotalResponse()

        try:
            total = mt5.orders_total()
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
