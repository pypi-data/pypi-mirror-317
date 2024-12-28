import MetaTrader5 as mt5
from mt5_grpc_proto.initialize_pb2 import (
    LoginResponse, ShutdownResponse, VersionResponse
)
from mt5_grpc_proto.initialize_pb2_grpc import InitializeServiceServicer
from mt5_grpc_proto.common_pb2 import Error


class InitializeServiceImpl(InitializeServiceServicer):
    def Login(self, request, context):
        """Connect to the specified trading account"""
        success = mt5.login(
            request.login,
            request.password,
            request.server
        )
        
        if not success:
            error = mt5.last_error()
            return LoginResponse(
                success=False,
                error=Error(code=error[0], message=error[1])
            )

        return LoginResponse(
            success=True,
            error=Error(code=0, message="")
        )

    def Shutdown(self, request, context):
        """Shut down connection to the MetaTrader 5 terminal"""
        success = mt5.shutdown()
        
        if not success:
            error = mt5.last_error()
            return ShutdownResponse(
                success=False,
                error=Error(code=error[0], message=error[1])
            )

        return ShutdownResponse(
            success=True,
            error=Error(code=0, message="")
        )

    def GetVersion(self, request, context):
        """Get the MetaTrader 5 terminal version"""
        version = mt5.version()
        
        if version is None:
            error = mt5.last_error()
            return VersionResponse(
                error=Error(code=error[0], message=error[1])
            )

        return VersionResponse(
            version=f"{version[0]}.{version[1]}.{version[2]}",
            error=Error(code=0, message="")
        ) 