import cv2 
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

recording = False
flip_mode = False
record_start_time = None

alpha = 1.0
beta = 0

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    if flip_mode:
        frame = cv2.flip(frame, 1)

    current_time = time.time()
    fps = 1 / (current_time - prev_time) if current_time != prev_time else 0
    prev_time = current_time

    cv2.putText(frame, f"FPS: {int(fps)}", (10, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    mode_text = "RECORD" if recording else "PREVIEW"
    mode_color = (0, 0, 255) if recording else (255, 255, 255)
    cv2.putText(frame, f"MODE: {mode_text}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, mode_color, 2)

    if recording:
        elapsed_time = int(time.time() - record_start_time)

        hours = elapsed_time // 3600
        mins = (elapsed_time % 3600) // 60
        secs = elapsed_time % 60

        time_text = f"{hours:02}:{mins:02}:{secs:02}"

        # 깜빡이는 빨간 점
        if int(time.time() * 2) % 2 == 0:
            cv2.circle(frame, (width // 2 - 110, 35), 10, (0, 0, 255), -1)

        # REC 표시 (상단 중앙)
        cv2.putText(frame, f"REC {time_text}", (width // 2 - 90, 42),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        out.write(frame)

    cv2.putText(frame, "SPACE: Record ON/OFF | ESC: Exit", (10, height - 50),
              cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    cv2.putText(frame, "F: Flip | U/D: Brightness | C/X: Contrast", (10, height - 80),
              cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1) 

    cv2.imshow("Video Recorder", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break
    elif key == 32:
        recording = not recording
        if recording:
            record_start_time = time.time()
    elif key == ord('f'):
        flip_mode = not flip_mode
    elif key == ord('u'):
        beta += 10
    elif key == ord('d'):
        beta -= 10
    elif key == ord('c'):
        alpha += 0.1
    elif key == ord('x'):
        alpha = max(0.1, alpha - 0.1)

cap.release()
out.release()
cv2.destroyAllWindows()