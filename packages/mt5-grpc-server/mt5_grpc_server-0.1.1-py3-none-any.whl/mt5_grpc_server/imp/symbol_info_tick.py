import MetaTrader5 as mt5
from google.protobuf.timestamp_pb2 import Timestamp
from mt5_grpc_proto.symbol_info_tick_pb2 import SymbolInfoTick, SymbolInfoTickResponse
from mt5_grpc_proto.symbol_info_tick_pb2_grpc import SymbolInfoTickServiceServicer


class SymbolInfoTickServiceImpl(SymbolInfoTickServiceServicer):
    def GetSymbolInfoTick(self, request, context):
        """
        Implements the GetSymbolInfoTick RPC method.
        Returns the last tick information for a specified symbol from MetaTrader 5.
        """
        # Initialize the response
        response = SymbolInfoTickResponse()

        try:
            # Get symbol info tick from MT5
            tick_info = mt5.symbol_info_tick(request.symbol)
            
            if tick_info is None:
                error_code, error_message = mt5.last_error()
                response.error.code = error_code
                response.error.message = error_message
                return response

            # Create SymbolInfoTick message and populate it with MT5 data
            tick = SymbolInfoTick()
            
            # Create and set timestamp
            timestamp = Timestamp()
            timestamp.FromSeconds(int(tick_info.time))
            tick.time.CopyFrom(timestamp)
            
            # Set numeric fields
            tick.bid = tick_info.bid
            tick.ask = tick_info.ask
            tick.last = tick_info.last
            tick.volume = tick_info.volume
            tick.time_msc = tick_info.time_msc
            tick.flags = tick_info.flags
            tick.volume_real = tick_info.volume_real

            # Set the tick field in the response
            response.tick.CopyFrom(tick)
            
            return response

        except Exception as e:
            response.error.code = -1  # Generic error code for exceptions
            response.error.message = str(e)
            return response