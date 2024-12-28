import MetaTrader5 as mt5
from google.protobuf.timestamp_pb2 import Timestamp
from mt5_grpc_proto.symbol_info_pb2 import SymbolInfo, SymbolInfoResponse
from mt5_grpc_proto.symbol_info_pb2_grpc import SymbolInfoServiceServicer


class SymbolInfoServiceImpl(SymbolInfoServiceServicer):
    def GetSymbolInfo(self, request, context):
        """
        Implements the GetSymbolInfo RPC method.
        Returns detailed information about a specified symbol from MetaTrader 5.
        """
        # Initialize the response
        response = SymbolInfoResponse()
        
        try:
            # Get symbol info from MT5
            symbol_info = mt5.symbol_info(request.symbol)
            
            if symbol_info is None:
                error_code, error_message = mt5.last_error()
                response.error.code = error_code
                response.error.message = error_message
                return response

            # Create SymbolInfo message and populate it with MT5 data
            info = SymbolInfo()
            
            # Boolean properties
            info.custom = symbol_info.custom
            info.select = symbol_info.select
            info.visible = symbol_info.visible
            info.spread_float = symbol_info.spread_float
            info.margin_hedged_use_leg = symbol_info.margin_hedged_use_leg

            # Integer properties
            info.chart_mode = symbol_info.chart_mode
            info.session_deals = symbol_info.session_deals
            info.session_buy_orders = symbol_info.session_buy_orders
            info.session_sell_orders = symbol_info.session_sell_orders
            info.volume = symbol_info.volume
            info.volumehigh = symbol_info.volumehigh
            info.volumelow = symbol_info.volumelow
            info.digits = symbol_info.digits
            info.spread = symbol_info.spread
            info.ticks_bookdepth = symbol_info.ticks_bookdepth
            info.trade_calc_mode = symbol_info.trade_calc_mode
            info.trade_mode = symbol_info.trade_mode
            info.trade_stops_level = symbol_info.trade_stops_level
            info.trade_freeze_level = symbol_info.trade_freeze_level
            info.trade_exemode = symbol_info.trade_exemode
            info.swap_mode = symbol_info.swap_mode
            info.swap_rollover3days = symbol_info.swap_rollover3days
            info.expiration_mode = symbol_info.expiration_mode
            info.filling_mode = symbol_info.filling_mode
            info.order_mode = symbol_info.order_mode
            info.order_gtc_mode = symbol_info.order_gtc_mode
            info.option_mode = symbol_info.option_mode
            info.option_right = symbol_info.option_right

            # Timestamp properties
            if hasattr(symbol_info, 'time'):
                timestamp = Timestamp()
                timestamp.FromSeconds(int(symbol_info.time))
                info.time.CopyFrom(timestamp)
            
            if hasattr(symbol_info, 'start_time'):
                start_time = Timestamp()
                start_time.FromSeconds(int(symbol_info.start_time))
                info.start_time.CopyFrom(start_time)
            
            if hasattr(symbol_info, 'expiration_time'):
                expiration_time = Timestamp()
                expiration_time.FromSeconds(int(symbol_info.expiration_time))
                info.expiration_time.CopyFrom(expiration_time)

            # Double properties
            info.bid = symbol_info.bid
            info.bidhigh = symbol_info.bidhigh
            info.bidlow = symbol_info.bidlow
            info.ask = symbol_info.ask
            info.askhigh = symbol_info.askhigh
            info.asklow = symbol_info.asklow
            info.last = symbol_info.last
            info.lasthigh = symbol_info.lasthigh
            info.lastlow = symbol_info.lastlow
            info.volume_real = symbol_info.volume_real
            info.volumehigh_real = symbol_info.volumehigh_real
            info.volumelow_real = symbol_info.volumelow_real
            info.option_strike = symbol_info.option_strike
            info.point = symbol_info.point
            info.trade_tick_value = symbol_info.trade_tick_value
            info.trade_tick_value_profit = symbol_info.trade_tick_value_profit
            info.trade_tick_value_loss = symbol_info.trade_tick_value_loss
            info.trade_tick_size = symbol_info.trade_tick_size
            info.trade_contract_size = symbol_info.trade_contract_size
            info.trade_accrued_interest = symbol_info.trade_accrued_interest
            info.trade_face_value = symbol_info.trade_face_value
            info.trade_liquidity_rate = symbol_info.trade_liquidity_rate
            info.volume_min = symbol_info.volume_min
            info.volume_max = symbol_info.volume_max
            info.volume_step = symbol_info.volume_step
            info.volume_limit = symbol_info.volume_limit
            info.swap_long = symbol_info.swap_long
            info.swap_short = symbol_info.swap_short
            info.margin_initial = symbol_info.margin_initial
            info.margin_maintenance = symbol_info.margin_maintenance
            info.session_volume = symbol_info.session_volume
            info.session_turnover = symbol_info.session_turnover
            info.session_interest = symbol_info.session_interest
            info.session_buy_orders_volume = symbol_info.session_buy_orders_volume
            info.session_sell_orders_volume = symbol_info.session_sell_orders_volume
            info.session_open = symbol_info.session_open
            info.session_close = symbol_info.session_close
            info.session_aw = symbol_info.session_aw
            info.session_price_settlement = symbol_info.session_price_settlement
            info.session_price_limit_min = symbol_info.session_price_limit_min
            info.session_price_limit_max = symbol_info.session_price_limit_max
            info.margin_hedged = symbol_info.margin_hedged
            info.price_change = symbol_info.price_change
            info.price_volatility = symbol_info.price_volatility
            info.price_theoretical = symbol_info.price_theoretical
            info.price_greeks_delta = symbol_info.price_greeks_delta
            info.price_greeks_theta = symbol_info.price_greeks_theta
            info.price_greeks_gamma = symbol_info.price_greeks_gamma
            info.price_greeks_vega = symbol_info.price_greeks_vega
            info.price_greeks_rho = symbol_info.price_greeks_rho
            info.price_greeks_omega = symbol_info.price_greeks_omega
            info.price_sensitivity = symbol_info.price_sensitivity

            # String properties
            info.basis = symbol_info.basis
            info.category = symbol_info.category
            info.currency_base = symbol_info.currency_base
            info.currency_profit = symbol_info.currency_profit
            info.currency_margin = symbol_info.currency_margin
            info.bank = symbol_info.bank
            info.description = symbol_info.description
            info.exchange = symbol_info.exchange
            info.formula = symbol_info.formula
            info.isin = symbol_info.isin
            info.name = symbol_info.name
            info.page = symbol_info.page
            info.path = symbol_info.path

            # Set the symbol_info field in the response
            response.symbol_info.CopyFrom(info)
            
            return response

        except Exception as e:
            response.error.code = -1  # Generic error code for exceptions
            response.error.message = str(e)
            return response
