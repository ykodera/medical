import socket
import select
from datetime import datetime
import sys

def main():
    if len(sys.argv)!=3:
        print("aaaa")

    args = sys.argv
    print("ok")
    host = args[1]#ipaddress
    port = int(args[2])#port
    elements_number = 10
    bufsize = 1024
    writeenable = False
    listenserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = set([listenserver_socket])
    msg = b''
    servstart_time = datetime.now()
    log = open('all_'+'{0:%Y%m%d}'.format(servstart_time)+'.log', 'a')
    #定数
    START = '#start\r\n'
    QUIT = '#quit\r\n'
    SIGNAL = '#signal'

    print('Use IPaddress:', host)
    print('Use Port:', port)
    print('Starting the server at', servstart_time)
    log.write('Starting the server at' + str(servstart_time)+'\n')

    #例外処理
    try:
        listenserver_socket.bind((host, port))
        listenserver_socket.listen(elements_number)

        print('Waiting for a client to call...')
        log.write('Waiting for a client to call...'+'\n')

        while True:
            rready_socket, wready_socket, xready_socket = select.select(readfds, [], [])

            #読み可能な記述子を1つずつみていく
            for sock in rready_socket:
                #その記述子が新規接続であれば
                if listenserver_socket is sock:
                    connfd, address = listenserver_socket.accept()
                    readfds.add(connfd)
                    log.write('NewDiscriptor' + str(connfd)+'\n')
                    print('NewDiscriptor', connfd)
                    startconnectiontime = datetime.now()
                    print('startconnectiontime at:', startconnectiontime)

                #新規でなければ
                else:
                    #データ受信
                    msg = sock.recv(bufsize)
                    msg.strip()

                    receiveddata_time = datetime.now()

                    #受け取ったデータ長が0だったら
                    if len(msg) == 0:
                        sock.close()
                        readfds.remove(sock)
                        log.write('Disconnection' + str(connfd)+'\n')
                        print('Disconnection ', connfd)
                        disconnectiontime = datetime.now()
                        print('disconnectiontime at:', disconnectiontime)
                    else:
                        received_data = msg.decode('utf-8')
                        log.write(str(receiveddata_time)+ ': ' + received_data+'\n')
                        print("****************")
                        print(receiveddata_time, ': ',received_data)#どのクライアントからの表示かも表示するのを追加予定
                        print("****************")

                        if received_data == START:
                            if writeenable:
                                log.write('The file is already open'+'\n')
                                print('The file is already open')
                                sock.send(b'The file is already open'+ b"\n")
                                endsession(f, filename, sessionlog, sock, log)
                            sessionStart_time = datetime.now()
                            filename = ('{0:%Y%m%d_%H%M%S}'.format(sessionStart_time) + '.csv')
                            sessionlogname = ('{0:%Y%m%d_%H%M%S}'.format(sessionStart_time) + '.log')
                            log.write('Starting the Session at ' + str(sessionStart_time))
                            print('Starting the Session at ', sessionStart_time)
                            sock.send(b'Starting the Session at ' + str(sessionStart_time).encode()+b'\n')

                            f = open (filename, 'a')
                            sessionlog = open (sessionlogname, 'a')
                            log.write('Opened a new file: ' + filename+'\n')
                            print('Opened a new file: ' + filename)
                            sock.send(b'Opened a new file: ' + filename.encode()+b'\n\n')

                            writeenable = True #書き込み可能に

                        elif received_data == QUIT:
                            if writeenable:
                                endsession(f, filename, sessionlog,sock, log)
                                writeenable = False

                        elif received_data == SIGNAL:
                            calc()

                        elif writeenable:
                            #ここが怪しい
                            #データを走査して、改行に当たったらそこまでをwriteするように
                            f.write((str(receiveddata_time) + ','+ received_data.rstrip('\r\n')+','+'\n'))
                            sessionlog.write((str(receiveddata_time) + ','+ received_data.rstrip('\r\n')+','+'\n'))
        f.close()

    finally:
        for sock in readfds:
            sock.close()
        log.close()
    return

def endsession(f, filename, sessionlog, sock, log):
    f.close()
    sessionlog.close()
    log.write('Closed a file: ' + filename+ '\n')
    print('Closed a file: ', filename)
    sock.send(b'Closed a file: ' + filename.encode()+ b"\n")

    sessionEnd_time = datetime.now()
    log.write('End the Session at ' + str(sessionEnd_time))
    print('End the Session at: ', sessionEnd_time, '\n')
    sock.send(b'End the Session at ' + str(sessionEnd_time).encode()+ b"\n\n")

    #計算箇所(予定),計算の前の加工もどうするか考えないと...
def calc():
    print('Calc!')

main()
