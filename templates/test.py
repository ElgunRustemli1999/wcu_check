import cv2

# RTSP linkini bura yaz
rtsp_url = 'rtsp://admin:7963686wcu@10.0.0.145/Streaming/Channels/101'
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("RTSP bağlantısı alınmadı")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Görüntü alınmadı")
        break

    cv2.imshow("RTSP Kamera", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC ilə çıx
        break

cap.release()
cv2.destroyAllWindows()
