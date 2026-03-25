import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import numpy as np
import pandas as pd
import pickle
from code_combine import load_scd_ndefs_and_templates, code_combiner
from ressources import landmark_names
import time
from pythonosc import udp_client
import math
import sys # for user input on console

def get_keypoints_with_names(landmarks):
    keypoints_with_names = []
    for i, landmark in enumerate(landmarks):
        keypoints_with_names.append({
            'name': landmark_names[i],
            'x': landmark.x,
            'y': landmark.y,
            'z': landmark.z,
            'visibility': landmark.visibility
        })
    return keypoints_with_names

# Helper Func to calculate center between two point coordinates
def calc_center_between(val_a, val_b):
    center = val_a + ((val_b - val_a) / 2)
    return center

def calc_distance(a_x, a_y, b_x, b_y):
    distance = math.sqrt(pow(a_x - b_x, 2) + pow(a_y - b_y, 2))
    return distance

# Function for making the first letter of a string upper case
def capitalize_first_letter(s):
    if not s:  # Check if the string is empty
        return s
    return s[0].upper() + s[1:]

def normalize(pose):
    norm_poses = []
    if pose[12].visibility < 0.2 and pose[11].visibility < 0.2:
        return [0, 0] * 12
    elif pose[12].visibility > 0.2 and pose[11].visibility < 0.2:
        x_center = pose[12].x + 0.15
        y_center = pose[12].y
    elif pose[12].visibility < 0.2 and pose[11].visibility > 0.2:
        x_center = pose[11].x - 0.15
        y_center = pose[11].y
    elif pose[12].visibility > 0.2 and pose[11].visibility > 0.2:
        x_center = pose[12].x + ((pose[11].x - pose[12].x) / 2)
        y_center = min(pose[11].y, pose[12].y) + (abs(pose[12].y - pose[11].y) / 2)

    # take keypoints only from left shoulder to right hip
    for i in range(11, 25):
        norm_x = pose[i].x - x_center
        norm_y = pose[i].y - y_center
        norm_poses.append([norm_x, norm_y, pose[i].visibility])
        #print(i)
        #print([norm_x, norm_y, pose[i].visibility])
    return norm_poses

def scale_color(color):
    return tuple(int(min(c * 1.5, 255)) for c in color)


# filled symbols
def paintRect(im, x, y, width, color):
    cv2.rectangle(im, (x ,y), (x + width ,y + width), color, -1)

def paintRect_l(im, x, y, width, color):
    cv2.rectangle(im, (x ,y), (x + int(width / 2.0)  ,y + width ), color, -1)

def paintRect_r(im, x, y, width, color):
    cv2.rectangle(im, (x + int(width / 2.0), y), (x + width , y + width), color, -1)

def paintCircle(im, x, y, width, color):
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 0, 360, color, -1)

def paintCircle_l(im, x, y, width, color):
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 90, 270, color, -1)

def paintCircle_r(im, x, y, width, color):
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 0, 90, color, -1)
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 270, 360, color, -1)

def paintCircle(im, x, y, width, color):
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 0, 360, color, -1)

def paintTriangle(im, x, y, width, color):
    pts = np.array([[x , y + int(width/2)], [x + width, y + int(width/2)], [x + int(width/2), y]])
    cv2.fillPoly(im, [pts], color)

def paintTriangle_l(im, x, y, width, color):
    pts = np.array([[x , y + int(width/2)], [x + int(width/2), y + int(width/2)], [x + int(width/2), y]])
    cv2.fillPoly(im, [pts], color)

def paintTriangle_r(im, x, y, width, color):
    pts = np.array([[x + int(width/2), y + int(width/2)], [x + width, y + int(width/2)], [x + int(width/2), y]])
    cv2.fillPoly(im, [pts], color)

def paintCross(im, x, y, width, color):
    cv2.line(im, (x, y + width), (x + width, y), color, int(width * 0.15))
    cv2.line(im, (x, y), (x + width, y + width), color, int(width * 0.15))

def paintCross_l(im, x, y, width, color):
    cv2.line(im, (x, y + width), (x + width, y), color, int(width * 0.15))

def paintCross_r(im, x, y, width, color):
    cv2.line(im, (x, y), (x + width, y + width), color, int(width * 0.15))



# empty symbols
def drawRect(im, x, y, width, color):
    cv2.rectangle(im, (x ,y), (x + width ,y + width), color, 3)

def drawRect_l(im, x, y, width, color):
    cv2.rectangle(im, (x ,y), (x + int(width / 2.0)  ,y + width ), color, 3)

def drawRect_r(im, x, y, width, color):
    cv2.rectangle(im, (x + int(width / 2.0), y), (x + width , y + width), color, 3)

def drawCircle(im, x, y, width, color):
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 0, 360, color, 3)

def drawCircle_l(im, x, y, width, color):
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 90, 270, color, 3)
    cv2.line(im, (x + int(width/2), y), (x + int(width/2), y + width), color, int(width * 0.05))

def drawCircle_r(im, x, y, width, color):
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 0, 90, color, 3)
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 270, 360, color, 3)
    cv2.line(im, (x + int(width/2), y), (x + int(width/2), y + width), color, int(width * 0.05))

def drawCircle(im, x, y, width, color):
    cv2.ellipse(im, (x + int(width/2)  ,y + int(width/2) ), (int(width/2), int(width/2)), 0, 0, 360, color, 3)

def drawTriangle(im, x, y, width, color):
    pts = np.array([[x , y + int(width/2)], [x + width, y + int(width/2)], [x + int(width/2), y]])
    cv2.polylines(im, [pts], isClosed=True, color=color, thickness=3)

def drawTriangle_l(im, x, y, width, color):
    pts = np.array([[x , y + int(width/2)], [x + int(width/2), y + int(width/2)], [x + int(width/2), y]])
    cv2.polylines(im, [pts], isClosed=True, color=color, thickness=3)

def drawTriangle_r(im, x, y, width, color):
    pts = np.array([[x + int(width/2), y + int(width/2)], [x + width, y + int(width/2)], [x + int(width/2), y]])
    cv2.polylines(im, [pts], isClosed=True, color=color, thickness=3)

def drawCross(im, x, y, width, color):
    cv2.line(im, (x, y + width), (x + width, y), color, int(width * 0.05))
    cv2.line(im, (x, y), (x + width, y + width), color, int(width * 0.05))

def drawCross_l(im, x, y, width, color):
    cv2.line(im, (x, y + width), (x + width, y), color, int(width * 0.05))

def drawCross_r(im, x, y, width, color):
    cv2.line(im, (x, y), (x + width, y + width), color, int(width * 0.05))

symbol_functions = [
    paintTriangle_l,
    paintTriangle_r,
    paintTriangle,
    paintCircle_l,
    paintCircle_r,
    paintCircle,
    paintCross_l,
    paintCross_r,
    paintCross,
    paintRect_l,
    paintRect_r,
    paintRect
]

symbol_functions_empty = [
    drawTriangle_l,
    drawTriangle_r,
    drawTriangle,
    drawCircle_l,
    drawCircle_r,
    drawCircle,
    drawCross_l,
    drawCross_r,
    drawCross,
    drawRect_l,
    drawRect_r,
    drawRect
]

action_dict = {
    "none": 0 ,
    "head_l": 1,
    "head_r": 2,
    "head_b": 3,
    "belly_l" : 4,
    "belly_r" : 5,
    "belly_b" : 6,
    "shoulders_l" : 7,
    "shoulders_r" : 8,
    "shoulders_b" : 9,
    "hip_l" : 10,
    "hip_r" : 11,
    "hip_b" : 12,
    "startup" : 5,
}

if __name__ == "__main__":
    sc_port_from_user = input("Please enter SC language port")
    if sc_port_from_user == "":
        sc_port_from_user = 57120

    time.sleep(5)

    mp_drawing = mp.solutions.drawing_utils # Drawing helpers
    mp_holistic = mp.solutions.holistic # Mediapipe Solutions
    formerClass = ''
    same_class_counter = 0
    same_class_detection_threshold = 20

    # Symbol Display
    symbol_width = 80
    symbol_display_list = [] # in cycles
    former_symbol_display_list = [] # in cycles
    class_detection_bar_width = 10

    # general Display
    pad_top_and_bottom = 0

    #code Composition
    code_string = ""
    combinators, n_definitions = load_scd_ndefs_and_templates()


    #print("--CP2")
    # Open Saved Model
    with open('thirteen-signs-14kp-rf.pkl', 'rb') as f:
        model = pickle.load(f)

    # Do Inference-Loop
    cap = cv2.VideoCapture(0)


    window_name = "Raw Webcam Feed"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)        # Create a named window

    # OSC Client einrichten
    ip = "127.0.0.1"

    port = int(sc_port_from_user)
    print("PORT: {}".format(port))
    client = udp_client.SimpleUDPClient(ip, port)

    # Initiate holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        i = 0

        while cap.isOpened():
            # print("--While-Loop-START")
            ret, frame = cap.read()

            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make Detections
            results = holistic.process(image)

            # Recolor image back to BGR for rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 3. Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                     mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                     mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                     )
            image = cv2.flip(image, 1)
            # Export coordinates
            try:
                # Extract Pose landmarks
                pose = results.pose_landmarks.landmark
                pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
                norm_poses = normalize(pose)

                keypoints_with_names = get_keypoints_with_names(pose)

                left_shoulder_x = -1
                right_shoulder_x = -1
                left_wrist_x = -1
                right_wrist_x = -1
                left_shoulder_y = -1
                right_shoulder_y = -1
                left_wrist_y = -1
                right_wrist_y = -1
                left_wrist_z = -1
                right_wrist_z = -1
                left_hip_x = -1
                right_hip_x = -1
                left_hip_y = -1
                right_hip_y = -1
                left_ankle_x = -1
                left_ankle_y = -1
                right_ankle_x = -1
                right_ankle_y = -1
                # Sende die Keypoints per OSC

                for kp in keypoints_with_names:
                    # client.send_message(f"/pose/{kp['name']}", [kp['x'], kp['y'], kp['z'], kp['visibility']])
                    if kp['name'] == "LEFT_SHOULDER":
                        left_shoulder_x =  kp['x']
                        left_shoulder_y =  kp['y']
                    elif kp['name'] == "RIGHT_SHOULDER":
                        right_shoulder_x =  kp['x']
                        right_shoulder_y =  kp['y']
                    elif kp['name'] == "LEFT_WRIST":
                        left_wrist_x =  kp['x']
                        left_wrist_y =  kp['y']
                        left_wrist_z = kp['z']
                    elif kp['name'] == "RIGHT_WRIST":
                        right_wrist_x =  kp['x']
                        right_wrist_y =  kp['y']
                        right_wrist_z = kp['z']
                    elif kp['name'] == "LEFT_HIP":
                        left_hip_x = kp['x']
                        left_hip_y = kp['y']
                    elif kp['name'] == "RIGHT_HIP":
                        right_hip_x = kp['x']
                        right_hip_y = kp['y']
                    elif kp['name'] == "LEFT_ANKLE":
                        left_ankle_x = kp['x']
                        left_ankle_y = kp['y']
                    elif kp['name'] == "RIGHT_ANKLE":
                        right_ankle_x = kp['x']
                        right_ankle_y = kp['y']

                if left_shoulder_x != -1 and right_shoulder_x != -1 and left_wrist_x != -1 and right_wrist_x != -1 and left_shoulder_y != -1 and right_shoulder_y != -1 and left_wrist_y != -1 and right_wrist_y != -1:
                    wrist_center_x = calc_center_between(left_wrist_x, right_wrist_x)
                    shoulder_center_x = calc_center_between(left_shoulder_x, right_shoulder_x)
                    both_wrists_x =  (shoulder_center_x - wrist_center_x) /  calc_distance(left_shoulder_x, left_shoulder_y, right_shoulder_x, right_shoulder_y)
                    wrist_center_y = calc_center_between(left_wrist_y, right_wrist_y)
                    shoulder_center_y = calc_center_between(left_shoulder_y, right_shoulder_y)
                    both_wrists_y =  (shoulder_center_y - wrist_center_y) /  calc_distance(left_shoulder_x, left_shoulder_y, right_shoulder_x, right_shoulder_y)
                    wrist_deviation_z =  calc_center_between(left_wrist_z, right_wrist_z)
                    openness = math.sqrt(pow(left_wrist_x - right_wrist_x, 2)+pow(left_wrist_y - right_wrist_y, 2)) / calc_distance(left_shoulder_x, left_shoulder_y, right_shoulder_x, right_shoulder_y)
                    left_wrist_y_norm = (shoulder_center_y - left_wrist_y) / calc_distance(left_shoulder_x, left_shoulder_y, right_shoulder_x, right_shoulder_y)
                    right_wrist_y_norm = (shoulder_center_y - right_wrist_y) / calc_distance(left_shoulder_x, left_shoulder_y, right_shoulder_x, right_shoulder_y)
                    client.send_message("/abstractions/upper_body", [both_wrists_x, both_wrists_y, wrist_deviation_z, openness, left_wrist_y_norm, right_wrist_y_norm])

                if left_hip_x != -1 and right_hip_x != -1 and left_hip_y != -1 and right_hip_y != -1 and left_ankle_x != -1 and left_ankle_y != -1 and right_ankle_x != -1 and right_ankle_y != -1:
                    hip_center_y = calc_center_between(left_hip_y, right_hip_y)
                    ankle_center_y = calc_center_between(left_ankle_y, right_ankle_y)
                    feet_hip_dist_norm = (ankle_center_y - hip_center_y) / (calc_distance(left_hip_x, left_hip_y, right_hip_x, right_hip_y)*4)
                    client.send_message("/abstractions/lower_body", [feet_hip_dist_norm])

                # Transform row
                row = list(np.array(norm_poses).flatten())

                # Make Detections
                X = pd.DataFrame([row])
                body_language_class = model.predict(X)[0]
                current_body_language_class_string = body_language_class.split(' ')[0]
                body_language_prob = model.predict_proba(X)[0]
                classes = model.classes_

                if current_body_language_class_string == 'head_l' and body_language_prob[4] < 0.8:
                    current_body_language_class_string = 'none'
                    body_language_prob[4] = 0.0


                if current_body_language_class_string == formerClass:
                    same_class_counter += 1

                    if (same_class_counter >= same_class_detection_threshold):
                        formerIndex = action_dict[formerClass]
                        #try:
                        if len(symbol_display_list) > 0:
                            if ((symbol_display_list[-1] != formerIndex) and (formerIndex >= 1) and (formerIndex <= 12)):
                                if len(symbol_display_list) >= 3:
                                    symbol_display_list.clear()

                                # only accept connecting signs in the middle (at position 2/3)
                                if len(symbol_display_list) == 1:
                                    if formerIndex >= 7 and formerIndex <= 9:
                                        symbol_display_list.append(formerIndex)
                                # on other positions (1/3 or 3/3), all signs are allowed
                                elif len(symbol_display_list) <= 2:
                                    if formerIndex < 7 or formerIndex > 9:
                                        symbol_display_list.append(formerIndex)
                                        if len(symbol_display_list) == 3:
                                            former_symbol_display_list.clear()
                                            code_string = code_combiner(symbol_display_list, combinators, n_definitions)
                                            client.send_message("/code/execute", [code_string])
                                            for i in range(0, 3):
                                                 former_symbol_display_list.append(symbol_display_list[i])
                        # in case that symbol list is still empty
                        elif (formerIndex >= 1) and (formerIndex <= 12):
                            # only accept sound symbols (smaller 7 or greater 9) – no combination symbols
                            if formerIndex < 7 or formerIndex > 9:
                                symbol_display_list.append(formerIndex)

                    # break with press q
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

                # Reset Counter when class has changed
                else:
                    formerClass = current_body_language_class_string
                    same_class_counter = 0

                # Colors
                colors = [
                    (245, 117, 16),   # Bright orange
                    (117, 245, 16),   # Lime green
                    (16, 117, 245),   # Bright blue
                    (255, 15, 255),   # Vibrant magenta
                    (255, 195, 0),    # Golden yellow
                    (0, 255, 127),    # Spring green
                    (255, 69, 0),     # Red-orange
                    (75, 0, 130),     # Indigo
                    (0, 191, 255),    # Deep sky blue
                    (255, 105, 180),  # Hot pink
                    (60, 179, 113),   # Medium sea green
                    (255, 20, 147),   # Deep pink
                    (138, 43, 226),   # Blue-violet
                    (255, 165, 0)     # Orange
                ]

                # list classes and probabilities
                class_index = 0
                start_y = 550
                for cl in classes:
                    cv2.rectangle(image, (10, start_y+(class_index*30)), (10 + int(round(body_language_prob[class_index],2)*100), start_y+30+(class_index*30)), colors[class_index], -1)
                    cv2.putText(image, str(cl), (10,start_y+30 + (class_index*30)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    if(cl == formerClass):
                        cv2.rectangle(image, (9, start_y-1+(class_index*30)), (9 + 200, start_y+31+(class_index*30)), (255, 255, 255), 2)
                    class_index +=1

                # former symbol list - paint symbols with filled geometries
                symbol_index = 0
                start_x = 100
                start_y = 100
                for former_symbol in former_symbol_display_list:
                    symbol_functions[former_symbol-1](image, start_x + (symbol_index*int(symbol_width * 1.5)), start_y, symbol_width, scale_color(colors[former_symbol]))
                    symbol_index +=1

                # current symbol list - paint symbols with empty geometries
                symbol_index = 0
                start_y = 195
                for symbol in symbol_display_list:
                    cv2.putText(image, str(symbol), (start_x + (symbol_index*int(symbol_width * 1.5)), start_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, scale_color(colors[symbol]), 2, cv2.LINE_AA)
                    symbol_functions_empty[symbol-1](image, start_x + (symbol_index*int(symbol_width * 1.5)), start_y + 15, symbol_width, colors[symbol])
                    symbol_index +=1

                #Display same class detection bar
                #same_class_counter
                if formerClass != 'none':
                    symbol_functions_empty[action_dict[formerClass]-1](image, 300, 320, int(symbol_width * 2.2), scale_color(colors[action_dict[formerClass]]))
                    cv2.rectangle(image, (300, 520), (300 + int(min(round(same_class_counter,2)*(symbol_width * 2.2/same_class_detection_threshold), symbol_width * 2.2)), 520 + class_detection_bar_width), colors[action_dict[formerClass]], -1)

                # Display code
                lines = code_string.splitlines()
                #line_index = 0
                for line_index in range(1, len(lines)-1):
                    cv2.putText(image, str(lines[line_index]), (780,25 + (line_index * 33)), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
                    line_index +=1

            except:
                pass

            # Padding, when screen format does not fit well
            image = cv2.copyMakeBorder(image,pad_top_and_bottom,pad_top_and_bottom,0,0,cv2.BORDER_CONSTANT)
            cv2.imshow(window_name, image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                print("--BREAK with q ")
                process.join()
                break

    process.join()
    cap.release()
    cv2.destroyAllWindows()
