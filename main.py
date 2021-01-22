# Step 1:   User detection process.
# Step 2:   User login operation.
# Step 3:   Object detection.
# Step 4:   Photo capturing process and acknowledgment.
# Step 5:   Process continuation or termination instruction.
# Step 6:   Session End.

import serial
import time

ser = serial.Serial('COM10', 9600)


# Step:1 (User presence is monitored and once detected (User:Null:end:) is (tx to UI from MC))
def User_detection_loop():
    User_detection_string = ser.readline()
    while(User_detection_string != b"User:Null:end:"):
        User_detection_string = ser.readline()
        User_detection_string.strip()
        User_detection_string = User_detection_string[:-2]
        print("User is not detected yet")
        print(User_detection_string)
        if (User_detection_string == b"User:Null:end:"):
            print("User is detected")
            User_login_opeartion()

# Step:2 (Login process is performed and once successful (Monitor:Null:end:) is (tx to MC from UI))
def User_login_opeartion():
    user_login_details = input(" \n type name")
    if (user_login_details == "Anirudh" or user_login_details == "Shanker"):
        print("Login successful")
        ser.write("Monitor:Null:end:".encode())
        object_detection_loop()

# Step:3 (Object presence is monitored inside the chute and once detected  (Object:chute_number:end:) is (tx to UI from MC))
def object_detection_loop():
    object_detection_string = ser.readline()
    while(object_detection_string != b"Object:1:end:" or object_detection_string != b"Object:2:end:" or object_detection_string != b"Object:3:end:"):
        object_detection_string = ser.readline()
        object_detection_string.strip()
        object_detection_string = object_detection_string[:-2]
        print("In object detection loop")
        print("object_detection_string")
        print(object_detection_string)
        if (object_detection_string == b"Object:1:end:" or object_detection_string == b"Object:2:end:" or object_detection_string == b"Object:3:end:"):
            Object_photo_Ack_loop()
# Step:4 Once photo is captured (Object_Ack:Null:end:) is (tx to MC from UI))
def Object_photo_Ack_loop():
    Object_photo_operation = input(" \n Is photo taken yes or no")
    if (Object_photo_operation == "yes"):
        time.sleep(2)
        ser.write("Object_Ack:Null:end:".encode())
        time.sleep(2)
        Process_cont_or_ter()

# Step:5 Once a session is done provide yes or no to control the process.
def Process_cont_or_ter():
    Process = input(" \n Do you want to continue yes or no ")
    if (Process == "yes"):
        object_detection_loop()
    elif (Process == "no"):
        Operation_end_loop()

# Step:6 Once a process is finished (End:Null:end:) is (tx to MC from UI)
def Operation_end_loop():
    ser.write("End:Null:end".encode())
    end_string = ser.readline
    print("After end string")
    print(end_string)
    User_detection_loop()


time.sleep(2)
while(True):
        User_detection_loop()
