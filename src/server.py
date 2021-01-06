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

import glob
import sys
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/cs557-inst/thrift-0.13.0/lib/py/build/lib*')[0])

# from tutorial import Calculator
# from tutorial.ttypes import InvalidOperation, Operation

# from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from pathlib import Path
import hashlib
from chord import FileStore
import socket
from collections import defaultdict
from chord.ttypes import NodeID

# storeOfNodeFT = {}
#currentNode = 0


class FileHandler:
    # fingerTable = []
    def __init__(self):
        self.storeOfNodeFT = defaultdict(list)
        self.portNumber = sys.argv[1]
        self.ipAddress = socket.gethostbyname(socket.gethostname())
        self.key = self.ipAddress + ':' + self.portNumber
        n = NodeID()
        n.ip = self.ipAddress
        n.port = self.portNumber
        n.id = hashlib.sha256(self.key.encode('utf-8')).hexdigest()
        self.currentNode = n
        self.storeOfMetadata = {}
        self.retOfFindPred = 0



    

    def makeSocket(self, ip, port):
        transport = TSocket.TSocket(ip, int(port))
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = FileStore.Client(protocol)
        transport.open()
        return client 


    

    def writeFile(self, rFile):
        try:
            if rFile.meta not in self.storeOfMetadata:
                metadata = {}
                # metadata['Owner'] = rFile.meta.owner
                metadata['Version'] = 0
                metadata['Filename'] = rFile.meta.filename
                key = metadata['Filename']
                print('filename = ',key)
                content_hash = hashlib.sha256(key.encode('utf-8')).hexdigest()
                metadata['content_hash'] = content_hash
                self.storeOfMetadata[rFile.meta.filename] = metadata
            else:
                fname = self.storeOfMetadata[rFile.meta.filename]
                # file_version = fname['Version'] + 1
                fname['Version'] = rFile.meta.version + 1 

        except Exception as err:
            print("SystemException: ",err)

    def readFile(self, rFile):
        try:
            if rFile in self.storeOfMetadata:
                return rFile
        except Exception as err:
            print("SystemException: ",err)

        


    
    def setFingertable(self, ft):
        # print('Port number is: ',sys.argv[1])
        # portNumber = sys.argv[1]
        # print(ft[0])
        # print('NEW LINE')
        # print(socket.gethostbyname(socket.gethostname()))
        # ipAddress = socket.gethostbyname(socket.gethostname())
        # key = ipAddress + ':' + portNumber
        # nodeId = hashlib.sha256(key.encode('utf-8'))
        # self.currentNode = nodeId
        print(self.currentNode)
        self.storeOfNodeFT[self.currentNode.id] = ft
        # print('/-/-/-/-/-/-/-/-/-\n')
        print('In setFingerTable',self.storeOfNodeFT[self.currentNode.id][0])
        # print("Each node and it\'s fingertable ")
        # print(storeOfNodeFT)



    def findPred(self, filename):
        # currNodeIP = socket.gethostbyname(socket.gethostname())
        # currNodePort = sys.argv[1]
        # key = currNodeIP + ':' + currNodePort
        # currNodeHash = hashlib.sha256(key.encode('utf-8'))
        # print("In findPred: ", self.storeOfNodeFT[self.currentNode][0])
        # print("Printing filenameHash",filenameHash)
        # print('Type of ft entry: ',type(self.storeOfNodeFT[self.currentNode][0]))
        # print('Getting node id', self.storeOfNodeFT[self.currentNode][0].id)
        # print('Getting node IP', self.storeOfNodeFT[self.currentNode][0].ip)
        # print('Getting node port', self.storeOfNodeFT[self.currentNode][0].port)
        # print('Filename is ',filename)
        
        # print('filenamehash is ',str(filenameHash))
        # count = 0
        # for i in range(0, len(self.storeOfNodeFT[self.currentNode])):
        #     # print('Node id ',i,' = ',self.storeOfNodeFT[self.currentNode][i].id)
        #     if filename == self.storeOfNodeFT[self.currentNode][i].id:
        #         print('on this server')
        #     else:
        #         count += 1
        #         continue
        # print('not on this server')
        # print('Count = ',count)


        filenameHash = hashlib.sha256(filename.encode('utf-8')).hexdigest()
        wanted = filenameHash
        print('\nwanted: ',wanted)
        succOfCurr = self.getNodeSucc()
        curr = self.currentNode
        print('\nSuccessor of current node = ',succOfCurr)
        if succOfCurr.id == wanted:
            print('successor of current node = wanted, so pred is current')
            n = NodeID()
            n.ip = self.currentNode.ip
            n.port = self.currentNode.port
            n.id = self.currentNode.id
            print(n)
            dummy = NodeID()
            dummy.ip = 'dummy'
            dummy.port = 0
            dummy.id = 'dummy'
            self.retOfFindPred = n
            return dummy
        

        elif wanted > curr.id and wanted < succOfCurr.id:
            print('\ngoing here .....\n')
            print('id = ',self.currentNode.id)
            print('ip = ',self.currentNode.ip)
            print('port = ',self.currentNode.port)
            n = NodeID()
            n.ip = self.currentNode.ip
            n.port = self.currentNode.port
            n.id = self.currentNode.id
            print(n)
            dummy = NodeID()
            dummy.ip = 'dummy'
            dummy.port = 0
            dummy.id = 'dummy'
            return dummy
            
        else:
            print('going in else')
            temp = self.storeOfNodeFT[self.currentNode.id]
            for i in range(len(temp)-1, 1, -1): 
                #print('going in for')
                if curr.id < temp[i].id < wanted:
                    print('going in for-if')
                    print(temp[i].ip, temp[i].port)
                    print('going in for-if before socket call')
                    client = self.makeSocket(temp[i].ip, temp[i].port)
                    print('going in for-if after socket call')
                    tmp = client.findPred(filename)
                    return self.makeSocket(temp[i].ip, temp[i].port).findPred(filename)
                # else:
                #     dummy = NodeID()
                #     dummy.ip = 'dummy'
                #     dummy.port = 0
                #     dummy.id = 'dummy'
                #     # self.retOfFindPred = n
                #     return dummy




    def getNodeSucc(self):
        try:
            print("In getNodeSucc ",self.storeOfNodeFT[self.currentNode.id][0])
            print('Exiting getNodeSucc')
            return self.storeOfNodeFT[self.currentNode.id][0]
        except Exception as err:
            print('SystemException: ',err)




    

if __name__ == '__main__':
    handler = FileHandler()
    processor = FileStore.Processor(handler)
    transport = TSocket.TServerSocket(port=int(sys.argv[1]))
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
