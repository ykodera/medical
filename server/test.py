import socket
import select
from datetime import datetime
import sys
import os

def endsession(f, filename, sessionlog, sock, log):
    f.close()
    sessionlog.close()
    output(log, 'Closed a file: ' ,filename)
    sock.send(b'Closed a file: ' + filename.encode()+ b"\n")

    sessionEnd_time = datetime.now()
    output(log, 'End the Session at ', str(sessionEnd_time))
    sock.send(b'End the Session at ' + str(sessionEnd_time).encode()+ b"\n\n")

def output(f,attribute,data):
    print(attribute + data + '\n')
    f.write(attribute + data + '\n')

def main():

    #定数
    START = '#s\r\n'
    QUIT = '#q\r\n'
    SIGNAL = '#signal'

    host = "192.168.24.10"
    port = 50000
    elements_number = 10
    bufsize = 1024
    writeenable = False
    listenserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = set([listenserver_socket])
    msg = b''
    saved_data = {}
    #nclients = 0

    #debug用
    flag=True

    servstart_time = datetime.now()

    new_dir_path='data/{0:%Y%m%d_%H%M%S}'.format(servstart_time)
    os.mkdir(new_dir_path)

    log = open(new_dir_path +'/all_{0:%Y%m%d_%H%M%S}'.format(servstart_time)+'.log', 'a')

    output(log, 'Use IPaddress: ', host)
    output(log, 'Use Port: ', str(port))
    output(log, 'Starting the server at: ', str(servstart_time))

    #例外処理
    try:
        listenserver_socket.bind((socket.gethostname(), port))
        listenserver_socket.listen(elements_number)

        output(log, 'Waiting for a client to call...','');

        while True:
            rready_socket, wready_socket, xready_socket = select.select(readfds, [], [])

            #読み可能な記述子を1つずつみていく
            for sock in rready_socket:
                #その記述子が新規接続であれば
                if listenserver_socket is sock:
                    connfd, address = listenserver_socket.accept()
                    readfds.add(connfd)
                    output(log, 'NewDiscriptor', str(connfd))
                    startconnectiontime = datetime.now()
                    output(log, 'startconnectiontime at: ', str(startconnectiontime))
                    saved_data[connfd.fileno()]=[]
                    #nclients=nclients+1
                    print("create buffer")

                #新規でなければ
                else:
                    #データ受信
                    msg = sock.recv(bufsize)
                    cfd = sock.fileno()
                    print("cfd:")
                    print(cfd)
                    receiveddata_time = datetime.now()

                    #受け取ったデータ長が0だったら
                    if len(msg) == 0:
                        sock.close()
                        readfds.remove(sock)
                        output(log, 'Disconnection: ',str(connfd))
                        disconnectiontime = datetime.now()
                        output(log, 'Disconnectiontime at: ', str(disconnectiontime))
                    else:
                        received_data = msg.decode('utf-8')
                        if (flag):
                            debugname = (new_dir_path+'/debug.csv')
                            debugf = open(debugname, 'a')
                            flag=False
                        debugf.write(received_data)

                        #output(log, str(receiveddata_time)+ ': ', received_data)
                        #print("****************")

                        #print(msg)
                        #print("utf-data: "+ received_data)
                        #print("****************")

                        if received_data == START:
                            if writeenable:
                                output(log, 'The file is already open','')
                                sock.send(b'The file is already open'+ b"\n")
                                endsession(f, filename, sessionlog, sock, log)
                            sessionStart_time = datetime.now()
                            filename = (new_dir_path+'/{0:%Y%m%d_%H%M%S}'.format(sessionStart_time) + '.csv')
                            sessionlogname = (new_dir_path+'/{0:%Y%m%d_%H%M%S}'.format(sessionStart_time) + '.log')
                            output(log, 'Starting the Session at ', str(sessionStart_time))

                            sock.send(b'Starting the Session at ' + str(sessionStart_time).encode()+b'\n')

                            f = open (filename, 'a')
                            sessionlog = open (sessionlogname, 'a')
                            output(log, 'Opened a new file: ', filename)
                            sock.send(b'Opened a new file: ' + filename.encode()+b'\n\n')

                            writeenable = True #書き込み可能に

                        elif received_data == QUIT:
                            if writeenable:
                                endsession(f, filename, sessionlog,sock, log)
                                writeenable = False

                        elif received_data == SIGNAL:
                            #to be conntinued...
                            calc()

                        elif writeenable:
                            #received_data:str saved_data:配列
                            print("saved_data{0}".format(cfd))
                            print(saved_data[cfd])
                            tail_data = ''.join(saved_data[cfd])
                            received_data = tail_data + received_data

                            if(received_data[-1]=='\n'):
                                print(received_data)
                                f.write(received_data)
                                #saved_dataを初期化
                                saved_data[cfd] = []
                            else:
                                print('aaaa')
                                spritdata = received_data.split('\n')

                                i=0
                                while(i < len(spritdata)-1):

                                    print(spritdata[i])
                                    log.write(spritdata[i]+'\n')
                                    f.write(spritdata[i]+'\n')
                                    i=i+1

                                string=spritdata[i]
                                saved_data[cfd]=[]

                                #分解
                                for c in string:
                                    saved_data[cfd].append(c)


                                #print(saved_data)#saved_data;str

                            #sessionlog.write((str(receiveddata_time) + ','+ received_data.rstrip('\r\n')+','+'\n'))
                            #f.write((str(receiveddata_time) + ',' + received_data.rstrip('\r\n')+','+'\n'))

        f.close()
        debugf.close()


    finally:
        for sock in readfds:
            sock.close()
        log.close()
    return


    #計算箇所(予定),計算の前の加工もどうするか考えないと...
def calc():
    print('Calc!')

main()
