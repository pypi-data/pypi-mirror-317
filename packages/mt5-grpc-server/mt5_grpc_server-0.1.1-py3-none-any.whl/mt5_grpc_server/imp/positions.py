import MetaTrader5 as mt5
from datetime import datetime
from typing import Optional, Tuple, Union
from google.protobuf.timestamp_pb2 import Timestamp
from mt5_grpc_proto.common_pb2 import Error
from mt5_grpc_proto.position_pb2 import (
    PositionsGetRequest,
    PositionsGetResponse,
    PositionsTotalRequest,
    PositionsTotalResponse,
    Position
)
from mt5_grpc_proto.position_pb2_grpc import PositionsServiceServicer


class PositionsServiceImpl(PositionsServiceServicer):
    """Implementation of Positions service for MetaTrader 5."""

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

    def _convert_position_to_proto(self, mt5_position) -> Position:
        """Convert MT5 position object to protobuf Position message.

        Args:
            mt5_position: Position information from MT5

        Returns:
            Position: Protobuf Position message
        """
        position = Position(
            ticket=mt5_position.ticket,
            symbol=mt5_position.symbol,
            type=mt5_position.type,
            magic=mt5_position.magic,
            identifier=mt5_position.identifier,
            reason=mt5_position.reason,
            volume=float(mt5_position.volume),
            price_open=float(mt5_position.price_open),
            stop_loss=float(mt5_position.sl),
            take_profit=float(mt5_position.tp),
            price_current=float(mt5_position.price_current),
            swap=float(mt5_position.swap),
            profit=float(mt5_position.profit),
            comment=mt5_position.comment
        )

        # Convert time field
        time = self._to_timestamp(mt5_position.time)
        if time:
            position.time.CopyFrom(time)

        return position

    def GetPositions(self, request: PositionsGetRequest, context) -> PositionsGetResponse:
        """Get open positions from MT5 based on specified filters.

        According to MT5 reference, we can filter positions by:
        1. Symbol name
        2. Symbol group
        3. Position ticket

        Args:
            request: PositionsGetRequest containing filter criteria
            context: gRPC context

        Returns:
            PositionsGetResponse containing matched positions or error
        """
        response = PositionsGetResponse()

        try:
            # Apply filters according to MT5 reference
            if request.HasField('ticket'):
                positions = mt5.positions_get(ticket=request.ticket)
            elif request.HasField('symbol'):
                positions = mt5.positions_get(symbol=request.symbol)
            elif request.HasField('group'):
                positions = mt5.positions_get(group=request.group)
            else:
                # If no filters specified, get all positions
                positions = mt5.positions_get()

            if positions is None:
                error_code, error_message = mt5.last_error()
                response.error.code = error_code
                response.error.message = f"Failed to get positions: {error_message}"
                return response

            # Convert MT5 positions to protobuf messages
            for mt5_position in positions:
                position_proto = self._convert_position_to_proto(mt5_position)
                response.positions.append(position_proto)

            return response

        except Exception as e:
            response.error.code = -1  # RES_E_FAIL
            response.error.message = f"Internal error processing positions: {str(e)}"
            return response

    def GetPositionsTotal(self, request: PositionsTotalRequest, context) -> PositionsTotalResponse:
        """Get total number of open positions.

        Args:
            request: PositionsTotalRequest
            context: gRPC context

        Returns:
            PositionsTotalResponse containing total count or error
        """
        response = PositionsTotalResponse()

        try:
            total = mt5.positions_total()
            if total is None:
                error_code, error_message = mt5.last_error()
                response.error.code = error_code
                response.error.message = f"Failed to get positions total: {error_message}"
                return response

            response.total = total
            return response

        except Exception as e:
            response.error.code = -1  # RES_E_FAIL
            response.error.message = f"Internal error getting positions total: {str(e)}"
            return response
