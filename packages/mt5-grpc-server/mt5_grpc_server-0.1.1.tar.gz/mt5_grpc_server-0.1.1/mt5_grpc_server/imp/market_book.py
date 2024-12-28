import MetaTrader5 as mt5
from mt5_grpc_proto.market_book_pb2 import (
    MarketBookAddResponse, MarketBookGetResponse, MarketBookReleaseResponse,
    BookInfo
)
from mt5_grpc_proto.market_book_pb2_grpc import MarketBookServiceServicer
from mt5_grpc_proto.common_pb2 import Error


class MarketBookServiceImpl(MarketBookServiceServicer):
    def _convert_to_book_info(self, mt5_book_info):
        """Convert MT5 book info to protobuf BookInfo message"""
        return BookInfo(
            type=mt5_book_info.type,
            price=mt5_book_info.price,
            volume=mt5_book_info.volume
        )

    def AddMarketBook(self, request, context):
        """Subscribe to market depth updates"""
        success = mt5.market_book_add(request.symbol)
        
        if not success:
            error = mt5.last_error()
            return MarketBookAddResponse(
                success=False,
                error=Error(code=error[0], message=error[1])
            )

        return MarketBookAddResponse(
            success=True,
            error=Error(code=0, message="")
        )

    def GetMarketBook(self, request, context):
        """Get current market depth data"""
        book = mt5.market_book_get(request.symbol)
        
        if book is None:
            error = mt5.last_error()
            return MarketBookGetResponse(
                error=Error(code=error[0], message=error[1])
            )

        return MarketBookGetResponse(
            book=[self._convert_to_book_info(item) for item in book],
            error=Error(code=0, message="")
        )

    def ReleaseMarketBook(self, request, context):
        """Unsubscribe from market depth updates"""
        success = mt5.market_book_release(request.symbol)
        
        if not success:
            error = mt5.last_error()
            return MarketBookReleaseResponse(
                success=False,
                error=Error(code=error[0], message=error[1])
            )

        return MarketBookReleaseResponse(
            success=True,
            error=Error(code=0, message="")
        ) 