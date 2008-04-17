# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/Core/DISET/private/InnerRPCClient.py,v 1.5 2008/04/17 13:51:09 acasajus Exp $
__RCSID__ = "$Id: InnerRPCClient.py,v 1.5 2008/04/17 13:51:09 acasajus Exp $"

import types
from DIRAC.Core.Utilities import Subprocess
from DIRAC.Core.DISET.private.BaseClient import BaseClient
from DIRAC.Core.Utilities.ReturnValues import S_OK


class InnerRPCClient( BaseClient ):

  def executeRPC( self, functionName, args ):
    if self.timeout:
      retVal = Subprocess.pythonCall( self.timeout, self.__serverRPC, functionName, args )
      if retVal[ 'OK' ]:
        return retVal[ 'Value' ]
      return retVal
    else:
      return self.__serverRPC( functionName, args )

  def __serverRPC( self, functionName, args ):
    rpcStub = ( self.serviceName, self.kwargs, functionName, args )
    retVal = self._connect()
    if not retVal[ 'OK' ]:
      retVal[ 'rpcStub' ] = rpcStub
      return retVal
    retVal = self._proposeAction( ( "RPC", functionName ) )
    if not retVal[ 'OK' ]:
      retVal[ 'rpcStub' ] = rpcStub
      return retVal
    self.transport.sendData( S_OK( args ) )
    receivedData = self.transport.receiveData()
    self.transport.close()
    if type( receivedData ) == types.DictType:
      receivedData[ 'rpcStub' ] = rpcStub
    return receivedData

