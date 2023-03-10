import cv2

# print(dir(cv2))

cap = cv2.VideoCapture('.\\media\\vid1_WIN_20230310_14_20_03_Pro.mp4')

length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(length)



while (cap.isOpened()):
    ret, frame = cap.read()
    # print(frame)
    print(type(frame))
    print(frame.shape)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()
