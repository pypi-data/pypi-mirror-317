import MetaTrader5 as mt5
import grpc
import os

from mt5_grpc_proto import common_pb2
from mt5_grpc_proto.common_pb2 import Error, GetLastErrorResponse
from mt5_grpc_proto.common_pb2_grpc import MetaTraderServiceServicer


class MetaTraderServiceImpl(MetaTraderServiceServicer):
    def GetLastError(self, request, context):
        """Implementation of GetLastError RPC method"""
        response = GetLastErrorResponse()
        try:
            # Get last error from MT5
            error_code, error_message = mt5.last_error()

            # Create error object
            error = Error(
                code=error_code,
                message=error_message
            )

            # Set error in response
            response.error.CopyFrom(error)
            return response

        except Exception as e:
            response.error.code = -1  # Generic error code for exceptions
            response.error.message = str(e)
            return response

    def Connect(self, request, context):
        """Implementation of Connect RPC method"""
        response = common_pb2.Empty()
        try:
            # If path is provided, set the MetaTrader5 path
            if request.path:
                # Validate the directory exists
                if not os.path.isdir(request.path):
                    error_code, error_message = mt5.last_error()
                    context.abort(grpc.StatusCode.INVALID_ARGUMENT, f'Invalid directory path: {request.path}')
                    return None
                
                # Set the path for MetaTrader5 initialization
                if not mt5.initialize(path=request.path):
                    error_code, error_message = mt5.last_error()
                    context.abort(grpc.StatusCode.INTERNAL, error_message)
                    return None
            else:
                # Initialize with default path
                if not mt5.initialize():
                    error_code, error_message = mt5.last_error()
                    context.abort(grpc.StatusCode.INTERNAL, error_message)
                    return None

            return response

        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            return None