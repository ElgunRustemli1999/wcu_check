from django.http import JsonResponse
from django.utils import timezone
from attendance.models import Attendance
from users.models import Worker
import face_recognition
import numpy as np
import base64
from base64 import b64decode
from PIL import Image
from io import BytesIO
import json
import logging
import pytz
import requests
from django.http import HttpResponse
from requests.auth import HTTPDigestAuth
logger = logging.getLogger(__name__)
baku_tz = pytz.timezone("Asia/Baku")


import cv2
from django.http import StreamingHttpResponse

def gen():
    cap = cv2.VideoCapture('rtsp://admin:7963686wcu@10.0.0.145/Streaming/Channels/101')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("⚠️ Kamera bağlantısı qurula bilmədi.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Kamera görüntüsü oxuna bilmədi.")
            break

        # MJPEG formatına çevir
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    

def video_feed(request):
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')


def recognize_face(request):
    if request.method != "POST":
        return JsonResponse({"message": "Yalnız POST metodu dəstəklənir."}, status=405)

    try:
        body = json.loads(request.body)
        image_data = body.get('image')

        if not image_data:
            return JsonResponse({"status": "error", "message": "Şəkil göndərilməyib."})

        # Base64 formatından şəkil çevrilir
        image_data = b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image_np = np.array(image)
        face_locations = face_recognition.face_locations(image_np)
        print("Face locations:", face_locations)
        print(image_np.shape)
        print(image_np.shape)
        # Üz encoding-ləri al
        encodings = face_recognition.face_encodings(image_np,face_locations)
        print(encodings)
        if not encodings:
            return JsonResponse({"status": "error", "message": "Üz tanınmadı."})

        unknown_encoding = encodings[0]

        for worker in Worker.objects.filter(is_active=True):
            if not worker.face_encoding:
                continue

            try:
                stored_encoding = np.frombuffer(
                    base64.b64decode(worker.face_encoding), dtype=np.float64
                )

                # Uzaqlıq ölçülür
                distance = face_recognition.face_distance([stored_encoding], unknown_encoding)[0]
                print(f"Test | {worker.worker_name}: Distance = {distance:.4f}")
                print(distance)

                if distance < 0.5:  # adaptiv eşik
                    now = timezone.now()

                    attendance, created = Attendance.objects.get_or_create(
                        worker=worker,
                        check_in_time__date=now.date(),
                        defaults={'check_in_time': now, 'is_checked_in': True}
                    )

                    if not created and attendance.is_checked_in and not attendance.check_out_time:
                        attendance.mark_check_out()
                        return JsonResponse({
                            "status": "success",
                        "message": f"{worker.worker_name} çıxış etdi.",
                        "worker_id": worker.id,
                        "full_name": f"{worker.worker_name} {worker.worker_surname}",
                        "type": "check_out",
                        "time": now.strftime("%H:%M:%S"),
                        "position": worker.position.position_name if worker.position else "-",
                        "department": worker.department.department_name if worker.department else "-"
                        })

                    elif not created and not attendance.is_checked_in:
                        attendance.mark_check_in()
                        return JsonResponse({
                            "status": "success",
                            "message": f"{worker.worker_name} ikinci dəfə giriş etdi.",
                            "worker_id": worker.id,
                            "type": "check_in",
                            "time": now.strftime("%H:%M:%S")
                        })

                    return JsonResponse({
                        "status": "success",
                        "message": f"{worker.worker_name} işə gəldi.",
                        "worker_id": worker.id,
                        "type": "check_in",
                        "time": now.strftime("%H:%M:%S")
                    })

            except Exception as e:
                logger.warning(f"Worker encoding parsing xətası: {worker.email} - {str(e)}")
                continue

        return JsonResponse({"status": "error", "message": "Tanınan işçi tapılmadı."})

    except Exception as e:
        logger.error(f"Ümumi xəta: {str(e)}")
        return JsonResponse({"status": "error", "message": f"Xəta baş verdi: {str(e)}"})
