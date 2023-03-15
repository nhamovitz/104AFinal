import cv2
from pathlib import Path

# print(dir(cv2))

demo_path = Path('.') / 'media' / 'vid1_WIN_20230310_14_20_03_Pro.mp4'

cap = cv2.VideoCapture(str(demo_path))

length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(length)

frame_number = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    # print(frame_number)
    if frame_number in (103, 104, 105):
        print(frame_number)
        print(frame)

    # print(type(frame))
    # print(frame.shape)
    cv2.imshow('Frame', frame)

    frame_number +=1
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()
