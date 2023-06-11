class CommandDefinitions:
    MOTOR = 0x4D
    SERVO = 0x53
    DISPLAY= 0x44
    LEFT = 0
    RIGHT =1
    NOTHING = 0xFF
    def __init__(self) -> None:
        pass

    def motor_set_speed(direction, value):
        dt = [CommandDefinitions.MOTOR]
        if direction=='L':
            dt.append(0)
        elif direction=='R':
            dt.append(1)
        if value>255 or value < 0:
            print("Motor value must be less than 255")
            return
        dt.append(value)
        return dt
    
    def servo_set_position(direction,value):
        dt = [CommandDefinitions.SERVO]
        if direction=='R':
            dt.append(0)
        elif direction=='Y':
            dt.append(1)
        if value>255 or value < 0:
            print("Servo value must be less than 255")
            return
        dt.append(value)
        return dt
    
    def display_print(value):
        dt = [CommandDefinitions.DISPLAY]
        dt.append(value)
        return dt
    
if __name__=='__main__':
    print("Hello")


    
        
