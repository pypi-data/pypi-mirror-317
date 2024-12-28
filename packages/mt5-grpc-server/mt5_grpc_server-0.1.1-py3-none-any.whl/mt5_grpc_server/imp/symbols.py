import MetaTrader5 as mt5
from mt5_grpc_proto.symbols_pb2 import (
    SymbolsTotalResponse, SymbolsGetResponse, SymbolSelectResponse
)
from mt5_grpc_proto.symbols_pb2_grpc import SymbolsServiceServicer
from mt5_grpc_proto.common_pb2 import Error


class SymbolsServiceImpl(SymbolsServiceServicer):
    def GetSymbolsTotal(self, request, context):
        """Get the number of all financial instruments"""
        total = mt5.symbols_total()
        
        if total is None:
            error = mt5.last_error()
            return SymbolsTotalResponse(
                error=Error(code=error[0], message=error[1])
            )

        return SymbolsTotalResponse(
            total=total,
            error=Error(code=0, message="")
        )

    def GetSymbols(self, request, context):
        """Get all financial instruments"""
        symbols = mt5.symbols_get(group=request.group if request.group else "*")
        
        if symbols is None:
            error = mt5.last_error()
            return SymbolsGetResponse(
                error=Error(code=error[0], message=error[1])
            )

        return SymbolsGetResponse(
            symbols=[symbol.name for symbol in symbols],
            error=Error(code=0, message="")
        )

    def SelectSymbol(self, request, context):
        """Select a symbol in the Market Watch window"""
        success = mt5.symbol_select(
            request.symbol,
            request.enable
        )
        
        if not success:
            error = mt5.last_error()
            return SymbolSelectResponse(
                success=False,
                error=Error(code=error[0], message=error[1])
            )

        return SymbolSelectResponse(
            success=True,
            error=Error(code=0, message="")
        ) 