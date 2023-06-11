import random
class ProtocolDefs:
    BEGIN = 0x24
    END = 0x3B

class ErrorDefinitions:
    OK = 0x4F
    ERR_INV_HEAD = 0x48
    ERR_INV_FOOT = 0x46
    ERR_INV_CMD = 0x49
    ERR_INV_MAGIC_NUMBER = 0x50 


class Command:
    def __init__(self):
        self.buf=[]
        self.BUF_LEN = 64
        self.MAX_MESSAGE_LEN =32
        self.current_magic_number = 0x42
        self.current_data =[]
        self.current_in_buf=[0]*64
        self.current_out_buf=[0]*64
        self.random_read_data = [0xFF]*64
    
    def init_buffers(self):
        #print(self.current_out_buf)
        self.current_in_buf=[0]*50
        self.current_out_buf=[0]*50


    # buf is gonna be a list
    def parse(self,buf,result=[]):
        start_index=0
        end_index=0
        for i in range(0,self.BUF_LEN):
            if buf[i]==ProtocolDefs.BEGIN:
                start_index = i
            if buf[i]==ProtocolDefs.END:
                end_index = i
                break;
            end_index = end_index+1

        if start_index > self.BUF_LEN/4:
            return ErrorDefinitions.ERR_INV_HEAD
        
        if end_index > 7*self.BUF_LEN/8:
            return ErrorDefinitions.ERR_INV_FOOT
        
        if buf[start_index+1]!=self.current_magic_number:
            return ErrorDefinitions.ERR_INV_MAGIC_NUMBER
        
        if buf[start_index+2]!=ErrorDefinitions.OK:
            return ErrorDefinitions.ERR_INV_CMD
        
        #[data_start,data_end)
        data_start = start_index+3
        data_end = end_index
        self.current_data = buf[data_start:data_end]
        return ErrorDefinitions.OK
    

    def package(self,data):
        self.init_buffers()
        if len(data)>=32:
            print("Data longer than 32 bytes")
            return 
        self.current_magic_number = random.randint(7,127)
        send_buffer = [ProtocolDefs.BEGIN, self.current_magic_number]
        send_buffer.extend(data)
        send_buffer.append(ProtocolDefs.END)
        buf_len = len(send_buffer)
        self.current_out_buf[0:buf_len] = send_buffer[0:buf_len]
       #print(self.current_out_buf)


    def get_send_data(self):
        return bytes(self.current_out_buf)
    
    def get_data(self):
        return self.current_data
    

if __name__=='__main__':
    commands = Command()
    data =[i for i in range (0,32)]
    in_buffer = [0]*64
    commands.package(data)
    out = commands.get_send_data()
    beg = [ProtocolDefs.BEGIN, commands.current_magic_number,ErrorDefinitions.ERR_INV_CMD]
    
    in_buffer[0:3] = beg[0:3]
    in_buffer[3:32] = data[0:32]
    in_buffer[13] = ProtocolDefs.END

    rdata = commands.parse(in_buffer)
    print("| out is {0} |".format(out))
    print(">%x"%rdata)
    print("data is {0}".format(commands.current_data))
