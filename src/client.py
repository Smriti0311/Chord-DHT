#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import sys
import glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/cs557-inst/thrift-0.13.0/lib/py/build/lib*')[0])

# from tutorial import Calculator
# from tutorial.ttypes import InvalidOperation, Operation, Work

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from chord import FileStore
import hashlib
from chord.ttypes import RFile
from chord.ttypes import RFileMetadata

def main():
    # Make socket
    transport = TSocket.TSocket(sys.argv[1], int(sys.argv[2]))

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = FileStore.Client(protocol)

    # Connect!
    transport.open()



    # client.setFingerTable(ft)
    
    fname = 'sampleWrite.txt'
    my_file = RFile()
    my_file.content = 'This is a sample'
    my_file.meta = RFileMetadata()
    my_file.meta.filename = fname
    my_file.meta.version = 1
    
    # print('In writefile: ')
    # client.writeFile(my_file)
    # print('Out of writefile: ')


    print('In readfile: ')
    client.readFile(fname)
    print('Out of readfile: ')


    # print('checking if control is going to getNodeSucc fn')
    # client.getNodeSucc()

    # print('Checking if control is going to findpred fn')
    # fname = '128.226.114.200:9088'
    # client.findPred(fname)

    
    


    # Close!
    transport.close()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
