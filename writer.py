import pyperclip
import pyautogui
import time
from ressources import codeDict
import math
import numpy as n
from read_scd_files import parse_ndef_file, parse_combinator_file
from pythonosc import udp_client
#import threading

#lock = threading.Lock()
#settings.busy = False

typingIsRunning = False

action_dict = {
    0 : "None",
    1 : "Saw",
    2 : "Sine",
    3 : "Square",
    4 : "Tri",
    5 : "Startup",
}

ndef_index_dict = {
    1 : 0,
    2 : 1,
    3 : 2,
    4 : 3,
    5 : 4,
    6 : 5,
    10 : 6,
    11 : 7,
    12 : 8,
}

# ndef_index_dict = {
#     1 : "SinOsc",
#     2 : "Saw",
#     3 : "LFTri",
#     4 : "LFPulse",
#     5 : "LFNoise2",
#     6 : "Dust",
#     10 : "LFNoise0",
#     11 : "LFNoise1",
#     12 : "LFNoise2",
# }

def spawn_text(msg):
    pyperclip.copy(msg) # copy msg in the clipboard
    pyautogui.hotkey('command', 'v') # paste msg

def delete_text(msg):
    num_lines = len(msg.splitlines())
    pyautogui.keyDown('shift')  # hold down the shift key
    pyautogui.keyUp('fn')    # work-around for a bug in pyautogui concerning arrow keys
    pyautogui.press('up', num_lines+1)     # press the up arrow key
    pyautogui.keyUp('shift')    # release the shift key
    pyautogui.press('del', num_lines)     # press the up arrow key
    pyautogui.keyUp('fn')    # work-around for a bug in pyautogui concerning arrow keys

def run_listed_code(key):
    pyautogui.typewrite(key)
    #print("code_writer: key written")
    pyautogui.press('enter')
    #print("code_writer: enter pressed")
    spawn_text(codeDict[key])
    #print("code_writer: text spawned")
    pyautogui.hotkey('command', 'enter') # paste msg
    #print("code_writer: command+enter pressed")

def print_letter_test():
    pyautogui.press('enter')
    pyautogui.typewrite("&&TEST 1a 2b 3d 4e")
    pyautogui.press('enter')

def equality_check(arr1, arr2, size1, size2):
   if (size1 != size2):
      return False
   arr1.sort()
   arr2.sort()
   for i in range(0, size2):
      if (arr1[i] != arr2[i]):
         return False
   return True

def print_startup_dur(startTime):
    pyautogui.press('enter', 2)
    startUpDur = time.time() - startTime

    pyautogui.typewrite("Now& {}".format(time.time()) )
    pyautogui.press('enter')
    pyautogui.typewrite("Function Call& {}".format(startTime) )
    pyautogui.press('enter')
    pyautogui.typewrite("Startup Time for writer& {}".format(startUpDur) )
    pyautogui.press('enter')
    pyautogui.press('enter')
    pyautogui.press('enter')

def run_synth_code_by_class(synth_class):
    try:
            pyautogui.hotkey('command', 'a')
            pyautogui.press('enter')
            pyautogui.keyUp('fn')    #

            keyToBeRun = "&&" + synth_class
            #print(f"Attempting to run_listed_code with key: {keyToBeRun}")
            #print_startup_dur()
            run_listed_code(keyToBeRun)
            #time.sleep(5)
            #delete_text(codeDict[keyToBeRun])
            #print(f"Successfully ran and deleted code for: {keyToBeRun}")
            #settings.busy = False
    except Exception as e:
            print(f"Error occurred: {e}")
            #settings.busy = False
# def move(desired_line, current_line, num_lines, desired_pos, current_pos, num_chars_per_line):
#     if desired_line == 0:
#         pyautogui.hotkey('command', 'up') # paste msg
#         current_pos = 0
#     elif desired_line >= num_lines:
#         pyautogui.hotkey('command', 'down') # paste msg
#     else:
#         while desired_line != current_line:
#             if desired_line < current_line:
#                 pyautogui.press('down')
#                 desired_line+=1
#             else:
#                 pyautogui.press('up')
#                 desired_line-=1
#
#     if desired_pos == 0:
#         pyautogui.hotkey('command', 'left') # paste msg
#     elif desired_pos >= num_chars_per_line:
#         pyautogui.hotkey('command', 'right') # paste msg
#     else:
#         while desired_pos != current_pos:
#             if current_pos < desired_pos:
#                 pyautogui.press('right')
#                 current_pos+=1
#             else:
#                 pyautogui.press('left')
#                 current_pos-=1

def move(desired_line, current_line, num_lines, desired_pos, current_pos, num_chars_per_line):
    if desired_line == 0:
        pyautogui.hotkey('command', 'up') # paste msg
        current_pos = 0
        current_line = 0
    elif desired_line >= num_lines:
        pyautogui.hotkey('command', 'down') # paste msg
        current_pos = num_chars_per_line
        current_line = num_lines
    else:
        num_line_presses = int(abs(desired_line - current_line))
        if desired_line < current_line:
            pyautogui.press('up', presses=num_line_presses)
            desired_line+=num_line_presses
        else:
            pyautogui.press('down', presses=num_line_presses)
            desired_line-=num_line_presses

    if desired_pos == 0:
        pyautogui.hotkey('command', 'left') # paste msg
        current_pos = 0
    elif desired_pos >= num_chars_per_line-1:
        pyautogui.hotkey('command', 'right') # paste msg
        current_pos = num_chars_per_line
    else:
        num_char_presses = int(abs(desired_pos - current_pos))
        if current_pos < desired_pos:
            pyautogui.press('right', presses=num_char_presses)
            current_pos+=num_char_presses
        else:
            pyautogui.press('left', presses=num_char_presses)
            current_pos-=num_char_presses

def load_scd_ndefs_and_templates():
    template_file_path = "Ndefs/combination_templates.scd"
    combinators = parse_combinator_file(template_file_path)

    n_definitions = []
    ndef_path_mask = "Ndefs/{}.scd"
    for i in range(0, 10):
        fp = ndef_path_mask.format(i)
        try:
            result = parse_ndef_file(fp)
            n_definitions.append(result)
        except:
            result = ["//file_not_found", "//file_not_found", "//file_not_found"]
            n_definitions.append(result)
            continue
    return combinators, n_definitions

def code_composer(input_array, combis, n_defs):
    definition_index_a = input_array[0]
    definition_index_b = input_array[2]
    combinator_index = 0
    mode_index_a = 1
    if input_array[1] == 9: # ADD
        combinator_index = 2
        mode_index_a = 0
    elif input_array[1] == 8: # MULTIPLY
        combinator_index = 1
        mode_index_a = 0
    elif input_array[1] == 7: # MODULATE
        combinator_index = 0
        mode_index_a = 1
    string = combis[combinator_index]
    string = remove_curly_brackets(string)
    string = string.format(n_defs[ndef_index_dict[definition_index_a]][mode_index_a], n_defs[ndef_index_dict[definition_index_b]][2])
    string = return_curly_brackets(string)
    return string

def remove_curly_brackets(string):
    string = string.replace("{}", "§§")
    string = string.replace("{", "°")
    string = string.replace("}", "$")
    string = string.replace("§§", "{}")
    return string

def return_curly_brackets(string):
    string = string.replace("°", "{")
    string = string.replace("$", "}")
    return string

def run_test_loop(shared_class_index, shared_wrist_dev_x, shared_wrist_dev_y, shared_sign_array):
    passedTime = 0
    lastTime = time.time()
    last_class = 100  # Initial value

    #positionTracker
    num_lines = 20
    num_chars_per_line = 56
    current_line = num_lines
    current_char_in_line = num_chars_per_line
    line_0_reference = 0.5

    # movement speed
    last_relative_pos_x = 0
    last_relative_pos_y = 0
    last_sign_array = [-1, -1, -1]

    # code composirion
    combinators, n_definitions = load_scd_ndefs_and_templates()

    # osc
    # OSC Client einrichten
    ip = "127.0.0.1"
    port = 57120
    client = udp_client.SimpleUDPClient(ip, port)

    #go to SC and do fresh startTime
    pyautogui.hotkey('command', 'space') # paste msg
    time.sleep(0.5)
    spawn_text("SuperCollider")
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('command', 'up') # paste msg
    time.sleep(0.5)
    spawn_text("//Length of combinators: {}; Length of n_definitions: {}; ".format(len(combinators), len(n_definitions)))
    #spawn_text("--CP1")
    while passedTime <= 20:
    #while True:
        #print("run_test_loop() passedTime: {}".format(passedTime))
        currentTime = time.time()
        passedTime = passedTime + (lastTime - currentTime)
        lastTime = currentTime
        current_class = shared_class_index.value
        current_sign_array = shared_sign_array[:]
        #spawn_text("--CP2")
        #try:
            #spawn_text("--CP3")
        #if( ( n.array([last_sign_array]) != n.array([current_sign_array]) ).all() ):
        if( last_sign_array[0] != current_sign_array[0] or last_sign_array[1] != current_sign_array[1] or last_sign_array[2] != current_sign_array[2]):
            #if(equality_check(last_sign_array, current_sign_array, len(last_sign_array), len(current_sign_array))):
                #spawn_text(" Yes!! The given arrays are DIFFERENR : last: {}; current: {} ".format(len(last_sign_array), len(current_sign_array)))
            #pyautogui.press('enter')
            #spawn_text(" ---Yes!! The given arrays are DIFFERENT----c:-{}--l:-{}----".format(current_sign_array[:], last_sign_array[:]))
            pyautogui.press('enter')
            last_sign_array = current_sign_array[:]
            try:
                # string_arr = code_composer(current_sign_array)
                # for string in string_arr:
                #      spawn_text(string)
                #      pyautogui.hotkey('command', 'enter')
                #      pyautogui.press('enter')

                string = code_composer(current_sign_array, combinators, n_definitions)
                #string = string.replace("\\", "$")
                client.send_message("/code/execute", [string])

                # strings = string.splitlines()
                # for line in strings:
                #     line = line.replace("\\", "$")
                #     client.send_message("/code/execute", ["().play;"])
                #spawn_text(string)
                #pyautogui.hotkey('command', 'enter')
                #pyautogui.press('enter')

            except Exception as e:
                 spawn_text("Problem with string_arr - {} ".format(e))


        #spawn_text("--CP5")
        relative_pos_y = shared_wrist_dev_y.value + line_0_reference
        if relative_pos_y < 0:
            line_0_reference += abs(relative_pos_y)
        destination_line = num_lines - round(max(min(relative_pos_y * num_lines, num_lines),0), 0)
        #move_up_down(destination_line, current_line, num_lines)
        relative_pos_x = shared_wrist_dev_x.value + 0.5
        destination_char_pos = round(max(min(relative_pos_x * num_chars_per_line, num_chars_per_line),0), 0)
        if round(passedTime, 1)%5 == 0:
            #pyautogui.hotkey('command', 'up') # paste msg
            current_pos = 0
            current_line = 0
        #move(destination_line, current_line, num_lines, destination_char_pos, current_char_in_line, num_chars_per_line)
        current_line = destination_line
        current_char_in_line = destination_char_pos

        speed = math.sqrt(pow(last_relative_pos_x - relative_pos_x, 2) + pow(last_relative_pos_y - relative_pos_y, 2))
        last_relative_pos_x = relative_pos_x
        last_relative_pos_y = relative_pos_y



        time.sleep(0.01)
    print("run_test_loop() WhileLoop ended")
