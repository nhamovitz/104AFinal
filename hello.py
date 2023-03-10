import cv2

# print(dir(cv2))

cap = cv2.VideoCapture('.\\media\\vid1_WIN_20230310_14_20_03_Pro.mp4')

while (cap.isOpened()):
    ret, frame = cap.read()
    print(frame)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()
