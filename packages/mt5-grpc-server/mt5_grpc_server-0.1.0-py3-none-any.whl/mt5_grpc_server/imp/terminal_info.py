import MetaTrader5 as mt5
from mt5_grpc_proto.terminal_pb2 import TerminalInfoResponse
from mt5_grpc_proto.terminal_pb2_grpc import TerminalInfoServiceServicer
from mt5_grpc_proto.common_pb2 import Error


class TerminalInfoServiceImpl(TerminalInfoServiceServicer):
    def GetTerminalInfo(self, request, context):
        """Get MetaTrader 5 terminal information"""
        terminal_info = mt5.terminal_info()
        
        if terminal_info is None:
            error = mt5.last_error()
            return TerminalInfoResponse(
                error=Error(code=error[0], message=error[1])
            )

        return TerminalInfoResponse(
            community_account=terminal_info.community_account,
            community_connection=terminal_info.community_connection,
            connected=terminal_info.connected,
            dlls_allowed=terminal_info.dlls_allowed,
            trade_allowed=terminal_info.trade_allowed,
            tradeapi_disabled=terminal_info.tradeapi_disabled,
            email_enabled=terminal_info.email_enabled,
            ftp_enabled=terminal_info.ftp_enabled,
            notifications_enabled=terminal_info.notifications_enabled,
            mqid=terminal_info.mqid,
            build=terminal_info.build,
            maxbars=terminal_info.maxbars,
            codepage=terminal_info.codepage,
            ping_last=terminal_info.ping_last,
            community_balance=terminal_info.community_balance,
            retransmission=terminal_info.retransmission,
            company=terminal_info.company,
            name=terminal_info.name,
            language=terminal_info.language,
            path=terminal_info.path,
            data_path=terminal_info.data_path,
            commondata_path=terminal_info.commondata_path,
            error=Error(code=0, message="")
        )