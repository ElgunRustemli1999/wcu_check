import cv2
import face_recognition
import numpy as np
from django.core.exceptions import ObjectDoesNotExist
from users.models import Worker
import base64

# Kamera başlatmaq
def start_camera():
    video_capture = cv2.VideoCapture(0)  # 0 - Yerləşdiyi kamera

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Kamera açılmadı.")
            break

        # Kameradan alınan şəkli üz tanıma üçün hazırlamaq
        rgb_frame = frame[:, :, ::-1]  # BGR-dan RGB-yə çeviririk

        # Kameradakı bütün üzləri tanımaq
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Verilən encoding ilə tanıma
            match = False
            workers = Worker.objects.all()  # Bütün işçiləri alırıq

            for worker in workers:
                known_encoding = base64.b64decode(worker.face_encoding)
                known_encoding = np.frombuffer(known_encoding, dtype=np.float64)
                results = face_recognition.compare_faces([known_encoding], face_encoding)

                if True in results:
                    match = True
                    # İşçinin adını və soyadını ekranda göstərmək
                    name = f"{worker.worker_name} {worker.worker_surname}"
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Giriş-çıxış saatını qeyd et (Check-in/Check-out)
                    handle_check_in_check_out(worker)

            if not match:
                cv2.putText(frame, "Taninmadi", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Kamera görüntüsünü ekranda göstəririk
        cv2.imshow('Video', frame)

        # `q` düyməsini basaraq kameranı dayandırmaq
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def handle_check_in_check_out(worker):
    """İşçinin giriş-çıxış saatlarını idarə et"""
    from datetime import datetime
    now = datetime.now()

    if worker.check_in is None:
        worker.check_in = now
        worker.save()
        print(f"Check-in: {now}")
    else:
        worker.check_out = now
        worker.save()
        print(f"Check-out: {now}")

