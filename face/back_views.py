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

baku_tz = pytz.timezone("Asia/Baku")
baku_now = timezone.now().astimezone(baku_tz)

logger = logging.getLogger(__name__)

def recognize_face(request):
    if request.method != "POST":
        return JsonResponse({"message": "Yalnız POST metodu dəstəklənir."}, status=405)

    try:
        body = json.loads(request.body)
        image_data = body.get('image')

        if not image_data:
            return JsonResponse({"status": "error", "message": "Şəkil göndərilməyib."})

        image_data = b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image_np = np.array(image)

        encodings = face_recognition.face_encodings(image_np)
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

                distance = face_recognition.face_distance([stored_encoding], unknown_encoding)[0]

                if distance < 0.5:
                    print(distance)
                    now = baku_now

                    attendance, created = Attendance.objects.get_or_create(
                        worker=worker,
                        check_in_time__date=now.date(),
                        defaults={'check_in_time': now, 'is_checked_in': True}
                    )

                    action = "check_in"
                    message = f"{worker.worker_name} {worker.worker_surname} işə gəldi."
                    if not created and attendance.is_checked_in and not attendance.check_out_time:
                        attendance.mark_check_out()
                        action = "check_out"
                        message = f"{worker.worker_name} {worker.worker_surname} çıxış etdi."
                    elif not created and not attendance.is_checked_in:
                        attendance.mark_check_in()
                        action = "check_in"
                        message = f"{worker.worker_name} {worker.worker_surname} ikinci dəfə giriş etdi."

                    return JsonResponse({
                        "status": "success",
                        "message": message,
                        "worker_id": worker.id,
                        "type": action,
                        "time": now.strftime("%H:%M:%S"),
                        "department": worker.department.department_name if worker.department else "Yoxdur",
                        "position": worker.position.position_name if worker.position else "Yoxdur",
                    })

            except Exception as e:
                logger.warning(f"Worker encoding parsing xətası: {worker.email} - {str(e)}")
                continue

        return JsonResponse({"status": "error", "message": "Tanınan işçi tapılmadı."})

    except Exception as e:
        logger.error(f"Ümumi xəta: {str(e)}")
        return JsonResponse({"status": "error", "message": f"Xəta baş verdi: {str(e)}"})
