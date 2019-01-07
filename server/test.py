import socket
import select
from datetime import datetime
import sys
import os

def endsession(f, filename, sock, log):
    f.close()
    sessionEnd_time = datetime.now()
    output(log,str(sessionEnd_time), 'Closed a file: ' ,filename)
    sock.send(b'Closed a file: ' + filename.encode()+ b"\n")

    output(log, str(sessionEnd_time),'End the Session at ', str(sessionEnd_time))
    sock.send(b'End the Session at ' + str(sessionEnd_time).encode()+ b"\n\n")
    output(log, '--------------------------------------------------------------\n--------------------------------------------------------------', '')

def output(f,time,attribute,data):
    print(time + attribute + data + '\n')
    f.write(time + attribute + data + '\n')

def main():

    #定数
    START = '#s\r\n'
    QUIT = '#q\r\n'
    SIGNAL = '#signal'

    host = "192.168.24.10"
    port = 50000
    elements_number = 10
    bufsize = 4096
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

    output(log, str(servstart_time), 'Use IPaddress: ', host)
    output(log, str(servstart_time), 'Use Port: ', str(port))
    output(log, str(servstart_time), 'Starting the server at: ', str(servstart_time))

    #例外処理
    try:
        #listenserver_socket.bind((socket.gethostname(), port))
        listenserver_socket.bind((str(host), port))
    except OSError as e:
        errortime =  datetime.now()
        output(log, str(errortime), str(e),'')

    else:
        waittotime = datetime.now()
        listenserver_socket.listen(elements_number)
        output(log, str(waittotime),'Waiting for a client to call...','');
    try:
        while True:
            rready_socket, wready_socket, xready_socket = select.select(readfds, [], [])

            #読み可能な記述子を1つずつみていく
            for sock in rready_socket:
                #その記述子が新規接続であれば
                if listenserver_socket is sock:
                    connfd, address = listenserver_socket.accept()
                    readfds.add(connfd)
                    startconnectiontime = datetime.now()                    
                    output(log, str(startconnectiontime), 'NewDiscriptor', str(connfd))
                    output(log, str(startconnectiontime), 'startconnectiontime at: ', str(startconnectiontime))
                    saved_data[connfd.fileno()]=[]
                    #nclients=nclients+1

                #新規でなければ
                else:
                    try:
                        #データ受信
                        msg = sock.recv(bufsize)
                    except ConnectionResetError as e:
                        errortime =  datetime.now()
                        output(log, str(errortime),str(e),'')
                    else:
                        cfd = sock.fileno()
                        #print("cfd:")
                        #print(cfd)
                        receiveddata_time = datetime.now()

                        #受け取ったデータ長が0だったら
                        if len(msg) == 0:
                            del saved_data[sock.fileno()]
                            readfds.remove(sock)
                            disconnectiontime = datetime.now()
                            output(log, str(disconnecitontime), 'Disconnection: ',str(sock))
                            output(log, str(disconnecitontime), 'Disconnectiontime at: ', str(disconnectiontime))
                            sock.close()
                        else:
                            try:
                                received_data = msg.decode('ascii')
                            except UnicodeDecodeError as e:
                                errortime =  datetime.now()
                                output(log, str(errortime),str(e), '')
                            else:
                                if (flag):
                                   # debugname = (new_dir_path+'/debug.csv')
                                   # debugf = open(debugname, 'a')
                                    #flag=False
                                #debugf.write(str(received_data))
#                                debugf.write(received_data)

                                #output(log, str(receiveddata_time)+ ': ', received_data)
                                #print("****************")
                                #print(msg)
                                    print("utf-data: "+ received_data)
                                #print("****************")

                                if received_data == START:
                                    if writeenable:
                                        message_time =  datetime.now()
                                        output(log, str(message_time),'The file is already open','')
                                        sock.send(b'The file is already open'+ b"\n")
                                        endsession(f, filename, sock, log)
                                    sessionStart_time = datetime.now()
                                    filename = (new_dir_path+'/{0:%Y%m%d_%H%M%S}'.format(sessionStart_time) + '.csv')
                                    #sessionlogname = (new_dir_path+'/{0:%Y%m%d_%H%M%S}'.format(sessionStart_time) + '.log')
                                    #sessionlog = open (sessionlogname, 'a')
                                    output(log, str(sessionStart_time),'Starting the Session at ', str(sessionStart_time))
                                    #output(sessionlog, 'Starting the Session at ', str(sessionStart_time))
                                    sock.send(b'Starting the Session at ' + str(sessionStart_time).encode()+b'\n')

                                    f = open (filename, 'a')
                                    message_time = datetime.now()
                                    output(log, str(message_time), 'Opened a new file: ', filename)
                                    #output(sessionlog, 'Opened a new file: ', filename)
                                    sock.send(b'Opened a new file: ' + filename.encode()+b'\n\n')

                                    writeenable = True #書き込み可能に

                                elif received_data == QUIT:
                                    if writeenable:
                                        endsession(f, filename, sock, log)
                                        writeenable = False

                                elif received_data == SIGNAL:
                                    #to be conntinued...
                                    Calc()

                                elif writeenable:
                                    #received_data:str saved_data:配列
                                    #print("saved_data{0}".format(cfd))
                                    #print(saved_data[cfd])
                                    tail_data = ''.join(saved_data[cfd])
                                    received_data = tail_data + received_data

                                    if(received_data[-1]=='\n'):
                                        print(received_data)
                                        f.write(received_data)
                                        log.write(received_data)
                                        #sessionlog.write(spritdata[i]+'\n')

                                        #saved_dataを初期化
                                        saved_data[cfd] = []
                                    else:

                                        splitdata = received_data.split('\n')

                                        i=0
                                        while(i < len(splitdata)-1):

                                            print(splitdata[i])
                                            log.write(splitdata[i]+'\n')
                                            #sessionlog.write(spritdata[i]+'\n')
                                            f.write(splitdata[i]+'\n')
                                            i=i+1

                                        string=splitdata[i]
                                        saved_data[cfd]=[]

                                        for c in string:
                                            saved_data[cfd].append(c)

        f.close()
    #    sessionlog.close()
        debugf.close()


    finally:
        for sock in readfds:
            sock.close()
        log.close()
        print("終了しました")
    return

    #未実装
def calc():
    print('to be continue...')

main()
