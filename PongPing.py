import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

width = 640
height = 480
paddle_width = 30
paddle_height = 150
ball_radius = 20
ball_speed_x = 8
ball_speed_y = 6

left_paddle_y = height // 2 - paddle_height // 2
right_paddle_y = height // 2 - paddle_height // 2
ball_x = width // 2
ball_y = height // 2

left_score = 0
right_score = 0
winning_score = 5

cap = cv2.VideoCapture(0)

def draw_objects(frame):
    cv2.rectangle(frame, (0, left_paddle_y), (paddle_width, left_paddle_y + paddle_height), (255, 0, 0), -1)
    cv2.rectangle(frame, (width - paddle_width, right_paddle_y), (width, right_paddle_y + paddle_height), (255, 0, 0), -1)

    cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 0, 255), -1)

    cv2.putText(frame, f'{left_score}', (width // 4, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
    cv2.putText(frame, f'{right_score}', (3 * width // 4, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

def move_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, left_score, right_score,ball_radius,paddle_height,paddle_width
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_y <= ball_radius or ball_y >= height - ball_radius:
        ball_speed_y = -ball_speed_y

    if (ball_x - ball_radius <= paddle_width and
        left_paddle_y < ball_y < left_paddle_y + paddle_height):
        ball_speed_x = -ball_speed_x
        if ball_speed_x > -20 or ball_speed_x < 20:
            if ball_speed_x < 0:
                ball_speed_x -= 1
            else:
                ball_speed_x += 1
        if ball_radius > 8:
            ball_radius -= 2
        if paddle_width > 20 :
            paddle_width -= 2
        if paddle_height > 80:
            paddle_height -= 10

    if (ball_x + ball_radius >= width - paddle_width and
        right_paddle_y < ball_y < right_paddle_y + paddle_height):
        ball_speed_x = -ball_speed_x
        if ball_speed_x > -20 or ball_speed_x < 20:
            if ball_speed_x < 0:
                ball_speed_x -= 1
            else:
                ball_speed_x += 1
        if ball_radius > 8:
            ball_radius -= 2
        if paddle_width > 20 :
            paddle_width -= 2
        if paddle_height > 80:
            paddle_height -= 10

    if ball_x < 0:
        right_score += 1
        reset_ball()
    elif ball_x > width:
        left_score += 1
        reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y,ball_radius,paddle_height,paddle_width
    ball_x = width // 2
    ball_y = height // 2
    ball_radius = 20
    if ball_speed_x < 0:
        ball_speed_x = 5
    else:
        ball_speed_x = -5
    paddle_width = 30
    paddle_height = 150

def ai_move_paddle():
    global left_paddle_y
    if ball_y < left_paddle_y + paddle_height // 2:
        left_paddle_y -= 5 
    elif ball_y > left_paddle_y + paddle_height // 2:
        left_paddle_y += 5

def check_winner():
    global left_score, right_score
    if game_mode == "human_vs_human":
        if left_score >= winning_score:
            return "Left Player Wins!"
        elif right_score >= winning_score:
            return "Right Player Wins!"
    else:
        if left_score >= winning_score:
            return "AI Wins!"
        elif right_score >= winning_score:
            return "Human Wins!"
    return None

def display_menu(frame):
    options = ["Ping Pong Game", "1. Human vs Human", "2. Human vs AI", "Hover hand to choose"]

    y_start = height // 2 - 80 
    y_step = 50 

    for i, option in enumerate(options):
        text_size = cv2.getTextSize(option, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        x = (width - text_size[0]) // 2  
        y = y_start + i * y_step
        box_coords = ((x - 10, y - text_size[1] - 10), (x + text_size[0] + 10, y + 10)) 
        cv2.rectangle(frame, box_coords[0], box_coords[1], (0, 255, 0), 2)
        cv2.putText(frame, option, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

def detect_selection(hand_pos):
    x, y = hand_pos
    if width // 4 < x < 3 * width // 4:
        if height // 2 - 40 < y < height // 2: 
            return "human_vs_human"
        elif height // 2 + 10 < y < height // 2 + 60:
            return "human_vs_ai"
    return None

def display_winner(frame, winner_text):
    text_size = cv2.getTextSize(winner_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    x = (width - text_size[0]) // 2
    y = height // 2
    box_coords = ((x - 20, y - text_size[1] - 20), (x + text_size[0] + 20, y + 20))
    cv2.rectangle(frame, box_coords[0], box_coords[1], (0, 255, 0), 2)
    cv2.putText(frame, winner_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

game_mode = None
selection_start_time = None
selection_duration = 2  

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if game_mode is None:

        display_menu(frame)


        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)


                selected_option = detect_selection((x, y))
                if selected_option:
                    if selection_start_time is None:
                        selection_start_time = time.time()
                    elif time.time() - selection_start_time >= selection_duration:
                        game_mode = selected_option
                        break
                else:
                    selection_start_time = None

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Ping Pong', frame)

    else:

        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

                if x > width // 2:
                    right_paddle_y = y - paddle_height // 2

                if game_mode == "human_vs_human":
                    if x < width // 2:
                        left_paddle_y = y - paddle_height // 2

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if game_mode == 'human_vs_ai':
            ai_move_paddle()

        move_ball()
        draw_objects(frame)

        winner = check_winner()
        if winner:
            display_winner(frame, winner)
            cv2.imshow('Ping Pong', frame)
            cv2.waitKey(3000)
            
            left_score = 0
            right_score = 0


        cv2.imshow('Ping Pong', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()