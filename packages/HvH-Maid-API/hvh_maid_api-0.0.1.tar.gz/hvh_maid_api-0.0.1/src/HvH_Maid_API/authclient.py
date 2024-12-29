import socket
import ssl
import time

from messagebuf import MessageBuf
#from simplelogger import SimpleLogger

G_server = {'1':1}

class AuthException(Exception):
    pass


#class AuthClient(SimpleLogger):
class AuthClient():
    def __init__(self, verbose=False):
        #SimpleLogger.__init__(self)
        self.verbose = verbose

    def connect(self, host, port, cert_path):
        #try:
        if 1==1:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.ws = ssl.wrap_socket(s, ca_certs=cert_path)
            #self.ws.connect((host, port))
            sock = ssl.wrap_socket(s, ca_certs=cert_path)
            G_server['sock'] = sock
            #print(G_server)
            #print(sock)
            #print(host)
            #print(port)
            print('connected')
            G_server['sock'].connect((host, port))
        #except Exception as e:
            #raise AuthException(e)

    def login(self, username, password):
        #self.__recv_bytes(2)
        msg = MessageBuf()
        msg.add_string('pw')
        msg.add_string(username)
        #msg.add_bytes(password.decode('hex'))
        msg.add_bytes(password)
        #msg.add_string(password)
        #print('MSG:',msg,'type',type(msg))
        self.__send_msg(msg)

        self.__recv_bytes(1,200)

        #print('LOOKING FOR COOKIE')

        msg = MessageBuf()
        msg.add_string('cookie')
        self.__send_msg(msg)
        #time.sleep(5)
        res = self.__recv_bytes(1,200)
        print('RES:',res)
        G_server['cookie'] = res
        
        #time.sleep(5)
        #self.__recv_bytes(2)
        #rpl = self.__recv_msg()
        #print('rpl',rpl)
        #status = rpl.get_string()
        #if status == 'ok':
            #acc = rpl.get_string()  # This is normally the same thing as `username`
            #print(acc)
        #    return
        #elif status == 'no':
            #print('NO')
        #    err = rpl.get_string()
        #    raise AuthException(err)
        #else:
        #    raise AuthException('Unexpected reply: "' + status + '"')
        return G_server['cookie']

    def get_cookie(self):
        #print('- trying to get cookie')
        msg = MessageBuf()
        msg.add_string('cookie')
        self.__send_msg(msg)
        time.sleep(5)
        self.__recv_bytes(2)
        time.sleep(5)
        self.__recv_bytes(2)

        #rpl = self.__recv_msg()
        #status = rpl.get_string()
        #if status == 'ok':
        #    cookie = rpl.get_bytes(32)
        #    return cookie
        #else:
        #    raise AuthException('Unexpected reply: "' + status + '"')

    def __prepend_header(self, msg):
        tmp = MessageBuf()
        tmp.add_uint16(len(msg.buf), be=True)
        tmp.add_bytes(msg.buf)
        return tmp

    def __send_msg(self, msg):
        msg = self.__prepend_header(msg)
        if self.verbose:
            self.info('> ' + str(msg))
        #self.ws.sendall(msg.buf)
        #print('MSG:',msg.buf,'type',type(msg.buf))
        G_server['sock'].sendall(msg.buf)

    def __recv_msg(self):
        #print('trying to get header')        
        header = MessageBuf(self.__recv_bytes(2))
        #print('set header >', header)
        #data_len = header.get_uint16(be=True)
        #print('get data')
        #msg = MessageBuf(self.__recv_bytes(data_len))
        #if self.verbose:
        #    self.info('< ' + str(msg))
        #return msg

    def __recv_bytes(self, max_count, bytes_size):
        #res = []
        count= 0
        
        while True:
            #print('count',count)
            count = count + 1
            #bytes_to_read = l - len(res)
            #if bytes_to_read < 1:
                #break
            if count > max_count:
                break

            #data = self.ws.recv(bytes_to_read)
            #print('+')
            data = G_server['sock'].recv(bytes_size)
            #print('-')
            if not data:
                print('there is no data')
                break

            #res += data
            #data = int.from_bytes(data, 'little')
            #res.append(data)
            #v = data.decode("utf-8")
            #v = data.decode("latin-1")
            #res.extend(data)
            #print('-',data,'>',v)
        #res = bytearray(res)
        print('type',type(data))
        print(data)
        return data
