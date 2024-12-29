import struct

# NOTE: Auth server uses BE, game server uses LE
def JorbBee(be):
    return '>' if be else '<'

def get_uint8(msg, be=False):
    res = msg['data'][msg['pos']]
    msg['pos'] += 1
    return res

def get_uint32(msg, be=False):
    b = msg['data'][msg['pos']:msg['pos'] + 4]
    res = struct.unpack(JorbBee(be) + 'I', b)[0]
    msg['pos'] += 4
    return [res, b]

def get_int32(msg, be=False):
    b = msg['data'][msg['pos']:msg['pos'] + 4]
    res = struct.unpack(JorbBee(be) + 'i', b)[0]
    msg['pos'] += 4
    return [res, b]

def get_remaining(msg):
    res = msg['data'][msg['pos']:]
    res_pos = len(msg['data'])
    
    print('res_pos',res_pos,'len_res',len(res),' : ',res[0])
    return res

def get_coords(msg):
        x = get_int32(msg)[0]
        y = get_int32(msg)[0]
        return {'x':x,'y':y}
