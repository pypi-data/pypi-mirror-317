import socket
import time
import struct
from hashlib import sha256

import HvH_Maid_API

import HvH_Maid_API.byte_convertor as byte_bee
from HvH_Maid_API.messagebuf import MessageBuf
from HvH_Maid_API.authclient import AuthClient


host = 'game.havenandhearth.com'
port = 1870
Server = {'msg_type':{0:'SESS',1:'REL',2:'ACK',3:'BEAT',6:'OBJDATA',7:'OBJACK',8:'CLOSE'}}


class MessageType(object):
    MSG_SESS = 0
    MSG_REL = 1
    MSG_ACK = 2
    MSG_BEAT = 3
    MSG_OBJDATA = 6
    MSG_OBJACK = 7
    MSG_CLOSE = 8

class RelMessageType(object):
    RMSG_NEWWDG = 0
    RMSG_WDGMSG = 1
    RMSG_DSTWDG = 2
    RMSG_GLOBLOB = 4
    RMSG_RESID = 6
    RMSG_PARTY = 7
    RMSG_CATTR = 9

def Combo_connect(login, passw, shizo_connect_number):
    acc_1 = AuthClient()
    my_hash = sha256(passw.encode('utf-8')).digest()
    passw_hash = sha256(passw.encode('utf-8')).hexdigest()
    passw_hash = my_hash

    acc_1.connect('game.havenandhearth.com', 1871, 'authsrv.crt')
    cookie = acc_1.login(login, passw_hash)
    cookie_2 = cookie[5:]

    Game_connect()
    print('game connected')
    Game_start_session(login, cookie_2, shizo_connect_number)
    print('session started')
    

def Game_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, port))
    Server['sock'] = sock

def Game_start_session(username, cookie, shizo_connect_number):
        msg = MessageBuf()
        msg.add_uint8(MessageType.MSG_SESS)
        msg.add_uint16(2)
        msg.add_string('Hafen')
        msg.add_uint16(shizo_connect_number)
        msg.add_string(username)
        msg.add_uint16(len(cookie))
        msg.add_bytes(cookie)
        #print('Len:',len(cookie))
        #print('Len cookie:',len(cookie))
        #print('cookie:',cookie)
        Game_send_msg(msg)
        
        #data = Server['sock'].recv(200)
        #dec = data.decode("utf-8")
        #print(data,' > ',dec),
        #print('AUTORIZATION MSG:', msg.buf)

        data, addr = Server['sock'].recvfrom(65535)
        print('data',data)

def Receive_from_server():
    msg = {}
    msg['data'], msg['addr'] = Server['sock'].recvfrom(65535)
    msg['pos'] = 0
    msg['type'] = Server['msg_type'][byte_bee.get_uint8(msg)]
    msg['size'] = len(msg['data'])
    return msg

def Handle_server_data():
    print(msg['data'][0], msg['type'], msg['size'])
    #byte_bee.get_remaining(msg)
    if msg['size'] > 1 and msg['type'] == 'OBJDATA':
        print(msg['data'][1], msg['data'][2])
        fl = byte_bee.get_uint8(msg)
        #fl=0
        idd = byte_bee.get_uint32(msg)
        frame = byte_bee.get_int32(msg)
        print('fl',fl,'idd',idd[0],idd[1],'frame',frame[0],frame[1])
        print('pos',msg['pos'])

        #while msg['size'] > msg['pos']:
        data_type = byte_bee.get_uint8(msg)
        print('data_type',data_type)
        for i in range(0,15):
            byte = msg['data'][i].to_bytes(1, byteorder='big')
            byte2 = msg['data'][i].to_bytes(1, byteorder='little')
            print('i',i,' : ',msg['data'][i],byte)

        if data_type == 75:
            print("get_coords")
            coord = byte_bee.get_coords(msg)
            print(coord)
            
    fumo = struct.pack("<I", 984613049) #969716090 973002760 975591811
    #type_fumo = (1).to_bytes(1, byteorder='little')
    type_fumo = 14
    found_fumo = 0
    print('fumo',fumo[0],fumo[1],fumo[2],fumo[3],fumo)
    if msg['size'] > 1 and msg['type'] == 'OBJDATA' and 1==1:
        for i in range(0,msg['size']):
            if i + 4 < msg['size']:
                byte_0 = msg['data'][i]
                byte_1 = msg['data'][i+1]
                byte_2 = msg['data'][i+2]
                byte_3 = msg['data'][i+3]
                if byte_0 == fumo[0] and byte_1 == fumo[1] and byte_2 == fumo[2] and byte_3 == fumo[3]:
                    print('FUUUUUUUUMOOOOO!!!!!!!! UWU UWU UWU',i)
                    print('next B',msg['data'][i+4])
                    found_fumo = 1
                if type_fumo == byte_0:
                    print('FUM type',i)

def Text_to_bytes(text):
    text_b = []
    for el in text:
        b = bytes(el, 'utf-8')[0]
        text_b.append(b)
    return text_b
    

def Chat_msg(text, shizo_number):
    b = Text_to_bytes(text)
    msg = [1] + [shizo_number] + [0, 1, 24, 0, 0, 0, 109, 115, 103, 0, 2] + b + [0]
    Send_msg_0(msg)

def Char_select(name, shizo_number):
    b = Text_to_bytes(name)
    msg = [1] + [shizo_number] + [0, 1, 3, 0, 0, 0, 112, 108, 97, 121, 0, 2] + b + [0]
    Send_msg_0(msg)

def Wow_im_so_so_smart_java_programmer():
    Send_msg_0([1, 0, 0, 1, 0, 0, 0, 0, 102, 111, 99, 117, 115, 0, 1, 1, 0, 0, 0])

def Hf_tp(shizo_number):
    msg = [1] + [shizo_number] + [0, 1, 30, 0, 0, 0, 97, 99, 116, 0, 2, 116, 114, 97, 118, 101, 108, 0, 2, 104, 101, 97, 114, 116, 104, 0, 4, 0, 3, 8, 154, 241, 255, 130, 207, 240, 255]
    Send_msg_0(msg)
        
def Send_msg(java_bytes):
    msg = Bytes_convertor(java_bytes)
    #print('msg', msg)
    Send_to_server(msg)
    time.sleep(0.25)
    
def Send_to_server(msg):
    print('MSG:',msg)
    Server['sock'].sendto(msg, (host, port))

def Send_msg_0(java_bytes):
    #for i in range(len(java_bytes)):
    msg = bytearray(java_bytes)
    #print('msg', msg)
    #print('MSG:',msg)
    Send_to_server(msg)
    time.sleep(0.25)

def Bytes_convertor(java_bytes):
    python_bytes = new_list = [ x % 256 for x in java_bytes]
    bytes_arr = bytearray(python_bytes)
    return bytes_arr
    
def Game_send_msg(msg):
    #print('MSG:',msg.buf)
    Server['sock'].sendto(msg.buf, (host, port))
