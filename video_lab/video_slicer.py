import cv2
import os

src = "mavideo.mp4"
video_path = rf'C:\Users\vivie\Documents\My_py\toolbox\video_lab\video_input\{src}'
output_folder = r'.\Documents\My_py\toolbox\video_lab\frames_output'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f'Error: Cannot open video file {video_path}')
else:
    currentFrame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  
        
        name = os.path.join(output_folder, f'frame_{currentFrame}.jpg')
        if frame is not None:
            cv2.imwrite(name, frame)
            print(f'Creating... {name}')
        else:
            print(f'Skipping empty frame {currentFrame}')

        currentFrame += 1

    print("------ fin du traitement -------")

    cap.release()
    cv2.destroyAllWindows()
