import MetaTrader5 as mt5
from mt5_grpc_proto.account_pb2 import AccountInfo, AccountInfoResponse
from mt5_grpc_proto.account_pb2_grpc import AccountInfoServiceServicer


class AccountInfoServiceImpl(AccountInfoServiceServicer):
    def GetAccountInfo(self, request, context):
        """
        Implements the GetAccountInfo RPC method.
        Returns account information from MetaTrader 5.
        """
        # Initialize the response
        response = AccountInfoResponse()

        try:
            # Get account info from MT5
            account_info = mt5.account_info()
            
            if account_info is None:
                error_code, error_message = mt5.last_error()
                response.error.code = error_code
                response.error.message = error_message
                return response

            # Create AccountInfo message and populate it with MT5 data
            info = AccountInfo()
            
            # Integer properties
            info.login = account_info.login
            info.trade_mode = account_info.trade_mode
            info.leverage = account_info.leverage
            info.limit_orders = account_info.limit_orders
            info.margin_so_mode = account_info.margin_so_mode
            info.margin_mode = account_info.margin_mode
            info.currency_digits = account_info.currency_digits

            # Boolean properties
            info.trade_allowed = account_info.trade_allowed
            info.trade_expert = account_info.trade_expert
            info.fifo_close = account_info.fifo_close

            # Double properties
            info.balance = account_info.balance
            info.credit = account_info.credit
            info.profit = account_info.profit
            info.equity = account_info.equity
            info.margin = account_info.margin
            info.margin_free = account_info.margin_free
            info.margin_level = account_info.margin_level
            info.margin_so_call = account_info.margin_so_call
            info.margin_so_so = account_info.margin_so_so
            info.margin_initial = account_info.margin_initial
            info.margin_maintenance = account_info.margin_maintenance
            info.assets = account_info.assets
            info.liabilities = account_info.liabilities
            info.commission_blocked = account_info.commission_blocked

            # String properties
            info.name = account_info.name
            info.server = account_info.server
            info.currency = account_info.currency
            info.company = account_info.company

            # Set the account_info field in the response
            response.account_info.CopyFrom(info)
            
            return response

        except Exception as e:
            response.error.code = -1  # Generic error code for exceptions
            response.error.message = str(e)
            return response
