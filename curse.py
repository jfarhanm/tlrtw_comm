import curses
import spi_comm
import command_defs
import protocol_defs
import time 

# I feel like this is not at all consistent by any means
# It is wheel is some places and motor in others 
# Thank you insomnia and a general lack of intellect ?
class GuiCommSender:
    def __init__(self):
        self.state=command_defs.CommandDefinitions.NOTHING
        self.command = None
    def package_and_send_command():
        pass

class CursesGui:
    SERVO_MIN = 0
    SERVO_MAX = 180

    MOTOR_MIN = 0
    MOTOR_MAX = 180
    def __init__(self):        
        self.servo_r_position = 0
        self.servo_y_position = 0

        self.wheel_left_speed=0;
        self.wheel_right_speed=0

        self.left_wheel_speed =0
        self.right_wheel_speed = 0 


        # All the curses stuff 
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        

        self.x_start = 5
        self.x_end = curses.COLS-7
        self.y_start = 5
        self.y_end = curses.LINES-7
        


        #Heading
        current_start_x = self.x_start
        current_start_y = self.y_start
        self.main_window = self.stdscr #curses.newwin(5,5,self.y_end,self.x_end)
        
        # Part windows 
        current_start_x = self.x_start
        current_start_y = self.y_start 
        self.main_window.addstr(0,self.x_end//2-10,"[[TLRTW'S TUI]]")
        self.main_window.refresh()


        #servos 
        self.servo_win_height = 10
        self.servo_win_width = 30
        self.servo_win_begin_x = current_start_x
        self.servo_win_begin_y = current_start_y

        #current_start_x= current_start_x + self.servo_win_width
        current_start_y= current_start_y + self.servo_win_height
        #self.main_window = curses.newwin(self.servo_win_height,self.servo_win_width,self.servo_win_begin_y,self.servo_win_begin_x)
        self.main_window.addstr(self.servo_win_begin_y,self.servo_win_begin_x +  5,"[SERVO PARAMETERS]")

        #motors
        self.motor_win_height = 10
        self.motor_win_width = 30
        self.motor_win_begin_x = current_start_x
        self.motor_win_begin_y = current_start_y

        current_start_x= current_start_x + self.motor_win_width
        current_start_y= current_start_y
        #self.main_window = curses.newwin(self.motor_win_height,self.motor_win_width, self.motor_win_begin_y,self.motor_win_begin_x)
        self.main_window.addstr(self.motor_win_begin_y,self.motor_win_begin_x +  5,"[WHEEL PARAMETERS]")

        self.help_win_height = 10
        self.help_win_width = 30
        self.help_win_begin_x = current_start_x
        self.help_win_begin_y = current_start_y
        self.main_window.addstr(self.help_win_begin_y,self.help_win_begin_x +  5,"[HELP]")
        self.main_window.addstr(self.help_win_begin_y+1,self.help_win_begin_x + 1, "A, D        : Control Servo Yaw")
        self.main_window.addstr(self.help_win_begin_y+2,self.help_win_begin_x +  1,"Z, C        : Control Servo Pitch")
        self.main_window.addstr(self.help_win_begin_y+3,self.help_win_begin_x +  1,"left, right : Control Motion Direction")
        self.main_window.addstr(self.help_win_begin_y+4,self.help_win_begin_x +  1,"Space       : Stop Motion ")
        self.main_window.addstr(self.help_win_begin_y+4,self.help_win_begin_x +  1,"Q           : Quit ")

        self.status_win_height = 10
        self.status_win_width = 30
        self.status_win_begin_x = current_start_x
        self.status_win_begin_y = self.servo_win_begin_y
        self.main_window.addstr(self.status_win_begin_y,  self.status_win_begin_x +  5,"[STATUS]")
        self.main_window.addstr(self.status_win_begin_y+1,self.status_win_begin_x +  1,"[RESP] : [NOT READY]")
        self.main_window.addstr(self.status_win_begin_y+2,self.status_win_begin_x +  1,"[WORKING]")
        self.main_window.addstr(self.status_win_begin_y+3,self.status_win_begin_x +  1,"[CLEAR]")
        self.comm_sender = GuiCommSender()

    def update_main_window():
        pass
        
    def update_servo_window(self):
        load_data_start = "["
        load_data_end = "]"
        nums_r = (self.servo_r_position/self.SERVO_MAX)*10
        nums_y = (self.servo_y_position/self.SERVO_MAX)*10
        nums_r = int(nums_r)
        nums_y = int(nums_y)
        strdata_r = " S-R : [{0}]".format(self.servo_r_position) + load_data_start + '█'*nums_r + ' '*(10-nums_r) + load_data_end
        strdata_y = " S-Y : [{0}]".format(self.servo_y_position) + load_data_start + '█'*nums_y + ' '*(10-nums_y) + load_data_end 
        self.main_window.addstr(self.servo_win_begin_y + 3, self.servo_win_begin_x + 1,strdata_r)
        self.main_window.addstr(self.servo_win_begin_y + 6,self.servo_win_begin_x + 1,strdata_y)
        self.main_window.refresh()
    
    def update_wheel_window(self):
        load_data_start = "["
        load_data_end = "]"
        nums_r = (self.wheel_left_speed/self.MOTOR_MAX)*10
        nums_y = (self.wheel_right_speed/self.MOTOR_MAX)*10
        nums_r = int(nums_r)
        nums_y = int(nums_y)
        strdata_lft = " M-L : [{0}]".format(self.wheel_left_speed) + load_data_start + '█'*nums_r + ' '*(10-nums_r) + load_data_end
        strdata_rgt = " M-R : [{0}]".format(self.wheel_right_speed) + load_data_start + '█'*nums_y + ' '*(10-nums_y) + load_data_end 
        self.main_window.addstr(self.motor_win_begin_y + 3,self.motor_win_begin_x + 1,strdata_lft)
        self.main_window.addstr(self.motor_win_begin_y + 6,self.motor_win_begin_x + 1,strdata_rgt)
        self.main_window.refresh()

    def handle_r_servo(self):
        if self.servo_r_position >self.SERVO_MAX:
            self.servo_r_position = self.SERVO_MAX

        if self.servo_r_position < self.SERVO_MIN:
            self.servo_r_position = self.SERVO_MIN
        r_servo_data = command_defs.CommandDefinitions.servo_set_position('R',self.servo_r_position)
        self.protocol.package(r_servo_data)
        self.spi_command_cycle()
        self.update_servo_window()

    def handle_y_servo(self):
        if self.servo_y_position >self.SERVO_MAX:
            self.servo_y_position = self.SERVO_MAX
            
        if self.servo_y_position < self.SERVO_MIN:
            self.servo_y_position = self.SERVO_MIN
        y_servo_data = command_defs.CommandDefinitions.servo_set_position('Y',self.servo_y_position)
        self.protocol.package(y_servo_data)
        self.spi_command_cycle()
        self.update_servo_window()
    
    def handle_wheel(self):
        if self.wheel_left_speed>self.MOTOR_MAX:
            self.wheel_left_speed = self.MOTOR_MAX

        if self.wheel_left_speed<self.MOTOR_MIN:
            self.wheel_left_speed = self.MOTOR_MIN
        
        if self.wheel_right_speed>self.MOTOR_MAX:
            self.wheel_right_speed = self.MOTOR_MAX

        if self.wheel_right_speed<self.MOTOR_MIN:
            self.wheel_right_speed = self.MOTOR_MIN
        l_motor_data = command_defs.CommandDefinitions.motor_set_speed('L',self.wheel_left_speed)
        r_motor_data = command_defs.CommandDefinitions.motor_set_speed('R',self.wheel_right_speed)
        
        # Left Wheel 
        self.protocol.package(l_motor_data)
        self.spi_command_cycle()
        # Right Wheel
        self.protocol.package(r_motor_data)
        self.spi_command_cycle()
        self.update_wheel_window()

    def init_comms(self):
        self.comm = spi_comm.SPIComm()
        self.cmd_defs = command_defs.CommandDefinitions()
        self.protocol = protocol_defs.Command()
    
    def spi_command_cycle(self):
        ret = []
        out = protocol_defs.ErrorDefinitions.ERR_INV_MAGIC_NUMBER
        self.comm.clear_buffers()
        if self.comm.poll_rdy():
            self.comm.tx(self.protocol.get_send_data())
            self.comm.clear_buffers()
        if self.comm.poll_rdy():
            ret = self.comm.tx(self.protocol.random_read_data)
            out = self.protocol.parse(ret)
        return out


    def main_loop(self):
        self.init_comms()
        try:
            while 1:
                
                c = self.stdscr.getch()
                
                # All the wheel Stuff
                # A lot of this is redundant 
                if c==curses.KEY_UP:
                    start_speed = self.wheel_left_speed
                    if start_speed<=self.wheel_right_speed:
                        start_speed = self.wheel_right_speed
                    self.wheel_left_speed = start_speed + 10
                    self.wheel_right_speed = start_speed + 10
                    self.handle_wheel()
                if c==curses.KEY_DOWN:
                    start_speed = self.wheel_left_speed
                    if start_speed<=self.wheel_right_speed:
                        start_speed = self.wheel_right_speed
                    self.wheel_left_speed = start_speed - 10
                    self.wheel_right_speed = start_speed - 10
                    self.handle_wheel()
                if c==curses.KEY_LEFT:
                    self.wheel_left_speed+=10
                    self.wheel_right_speed-=10
                    self.handle_wheel()
                if c==curses.KEY_RIGHT:
                    self.wheel_right_speed+=10
                    self.wheel_left_speed-=10
                    self.handle_wheel()
                if c==ord(' '):
                    self.wheel_left_speed=0
                    self.wheel_right_speed=0
                    self.handle_wheel()

                if c==ord('s'): #print to screen
                    pass

                # All the servo stuff 
                if c==ord('a'): #yaw go right 
                    self.servo_y_position-=10
                    self.handle_y_servo()
                if c==ord('d'): #left
                    self.servo_y_position+=10
                    self.handle_y_servo()
                if c==ord('z'): #roll right 
                    self.servo_r_position-=10
                    self.handle_r_servo()
                if c==ord('c'):#left 
                    self.servo_r_position+=10
                    self.handle_r_servo()

                if c==ord('q'):
                    break
                #time.sleep(0.1) # a 1ms delay for safety 
        finally: 
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()    
            curses.endwin()


if __name__=='__main__':
    gui = CursesGui()
    gui.main_loop()

