import protocol_defs
import command_defs
import spidev 
import pigpio
import time


class SPIComm:
    def __init__(self):
        self.BUF_LEN = 64
        self.tx_buf = bytearray(self.BUF_LEN)
        self.rx_buf = bytearray(self.BUF_LEN)
        
        self.SPI_CHANNEL =0 
        self.spi = spidev.SpiDev(0,self.SPI_CHANNEL)
        self.spi.max_speed_hz = 40000
        self.spi.mode = 3
        self.spi.loop = False
        self.spi.bits_per_word = 8

        self.RDY_PIN = 27 
        self.pi = pigpio.pi() 
        self.pi.set_mode(self.RDY_PIN,pigpio.INPUT)
        self.pi.set_pull_up_down(self.RDY_PIN,pigpio.PUD_UP) # Ok gotta figure this out 


    def clear_buffers(self):
        for i in range (0,self.BUF_LEN):
            self.tx_buf[i] = 0xFF
            self.rx_buf[i] = 0xFF

    def recv(self):
        self.clear_buffers()
        return self.spi.readbytes(self.BUF_LEN)
    
    def tx(self,data):
        self.clear_buffers()
        d_len = len(data)
        if d_len>self.BUF_LEN-2:
            d_len = self.BUF_LEN - 2
        for i in range(0,d_len):
            self.tx_buf[i] = data[i]        
        #print("\n\n>TX BUFFER IS : \n\n",self.tx_buf) #print
        reply = self.spi.xfer(list(self.tx_buf))
        return reply

    def poll_rdy(self):
        while True:
            rdy = self.pi.read(self.RDY_PIN)
            time.sleep(0.0001)
            if rdy:
                return True


class RComm:
    def __init__(self):
        self.comm = SPIComm()
        self.cmd_defs = command_defs.CommandDefinitions()
        self.protocol = protocol_defs.Command()
    
    def run(self):
        motor_data = command_defs.CommandDefinitions.motor_set_speed('L',128)
        servo_data = command_defs.CommandDefinitions.servo_set_position('R',120)
        display_data = command_defs.CommandDefinitions.display_print("HELLO TLRTW")
        
        self.protocol.package(motor_data)
        
        if self.comm.poll_rdy():
            self.comm.tx(self.protocol.get_send_data())
            self.comm.clear_buffers()
            ret = []
        if self.comm.poll_rdy():
            ret = self.comm.tx(self.protocol.random_read_data)
            print("RET IS : ",ret)
            out = self.protocol.parse(ret)
            print("PARSE RESULT IS : ",out)

         



if __name__=='__main__':
    comm = RComm()
    print(">INITIALISED SPI COMM")
    comm.run()
    
