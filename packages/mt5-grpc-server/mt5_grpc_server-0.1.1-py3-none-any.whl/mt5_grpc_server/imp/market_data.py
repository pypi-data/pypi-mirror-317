import MetaTrader5 as mt5
from datetime import datetime
import pytz

from mt5_grpc_proto.market_data_pb2 import (
    CopyRatesFromResponse, CopyRatesFromPosResponse, CopyRatesRangeResponse,
    CopyTicksFromResponse, CopyTicksRangeResponse, Rate, Tick
)
from mt5_grpc_proto.market_data_pb2_grpc import MarketDataServiceServicer
from mt5_grpc_proto.common_pb2 import Error
from google.protobuf.timestamp_pb2 import Timestamp


class MarketDataServiceImpl(MarketDataServiceServicer):
    def _convert_to_rate(self, mt5_rate):
        """Convert MT5 rate to protobuf Rate message"""
        timestamp = Timestamp()
        timestamp.FromSeconds(int(mt5_rate[0]))
        
        return Rate(
            time=timestamp,
            open=mt5_rate[1],
            high=mt5_rate[2],
            low=mt5_rate[3],
            close=mt5_rate[4],
            tick_volume=mt5_rate[5],
            spread=mt5_rate[6],
            real_volume=mt5_rate[7]
        )

    def _convert_to_tick(self, mt5_tick):
        """Convert MT5 tick to protobuf Tick message"""
        timestamp = Timestamp()
        timestamp.FromSeconds(int(mt5_tick[0]))
        
        return Tick(
            time=timestamp,
            bid=mt5_tick[1],
            ask=mt5_tick[2],
            last=mt5_tick[3],
            volume=mt5_tick[4],
            time_msc=mt5_tick[5],
            flags=mt5_tick[6],
            volume_real=mt5_tick[7]
        )

    def CopyRatesFrom(self, request, context):
        """Get bars from specified date"""
        # Convert protobuf timestamp to datetime
        date_from = datetime.fromtimestamp(request.date_from.seconds, tz=pytz.UTC)
        
        rates = mt5.copy_rates_from(
            request.symbol,
            request.timeframe,
            date_from,
            request.count
        )

        if rates is None:
            error = mt5.last_error()
            return CopyRatesFromResponse(
                error=Error(code=error[0], message=error[1])
            )

        return CopyRatesFromResponse(
            rates=[self._convert_to_rate(rate) for rate in rates],
            error=Error(code=0, message="")
        )

    def CopyRatesFromPos(self, request, context):
        """Get bars from specified position"""
        rates = mt5.copy_rates_from_pos(
            request.symbol,
            request.timeframe,
            request.start_pos,
            request.count
        )

        if rates is None:
            error = mt5.last_error()
            return CopyRatesFromPosResponse(
                error=Error(code=error[0], message=error[1])
            )

        return CopyRatesFromPosResponse(
            rates=[self._convert_to_rate(rate) for rate in rates],
            error=Error(code=0, message="")
        )

    def CopyRatesRange(self, request, context):
        """Get bars for specified date range"""
        # Convert protobuf timestamps to datetime
        date_from = datetime.fromtimestamp(request.date_from.seconds, tz=pytz.UTC)
        date_to = datetime.fromtimestamp(request.date_to.seconds, tz=pytz.UTC)
        
        rates = mt5.copy_rates_range(
            request.symbol,
            request.timeframe,
            date_from,
            date_to
        )

        if rates is None:
            error = mt5.last_error()
            return CopyRatesRangeResponse(
                error=Error(code=error[0], message=error[1])
            )

        return CopyRatesRangeResponse(
            rates=[self._convert_to_rate(rate) for rate in rates],
            error=Error(code=0, message="")
        )

    def CopyTicksFrom(self, request, context):
        """Get ticks from specified date"""
        # Convert protobuf timestamp to datetime
        date_from = datetime.fromtimestamp(request.date_from.seconds, tz=pytz.UTC)
        
        ticks = mt5.copy_ticks_from(
            request.symbol,
            date_from,
            request.count,
            request.flags
        )

        if ticks is None:
            error = mt5.last_error()
            return CopyTicksFromResponse(
                error=Error(code=error[0], message=error[1])
            )

        return CopyTicksFromResponse(
            ticks=[self._convert_to_tick(tick) for tick in ticks],
            error=Error(code=0, message="")
        )

    def CopyTicksRange(self, request, context):
        """Get ticks for specified date range"""
        # Convert protobuf timestamps to datetime
        date_from = datetime.fromtimestamp(request.date_from.seconds, tz=pytz.UTC)
        date_to = datetime.fromtimestamp(request.date_to.seconds, tz=pytz.UTC)
        
        ticks = mt5.copy_ticks_range(
            request.symbol,
            date_from,
            date_to,
            request.flags
        )

        if ticks is None:
            error = mt5.last_error()
            return CopyTicksRangeResponse(
                error=Error(code=error[0], message=error[1])
            )

        return CopyTicksRangeResponse(
            ticks=[self._convert_to_tick(tick) for tick in ticks],
            error=Error(code=0, message="")
        ) 