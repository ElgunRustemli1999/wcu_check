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

logger = logging.getLogger(__name__)
baku_tz = pytz.timezone("Asia/Baku")

def recognize_face(request):
    if request.method != "POST":
        return JsonResponse({"message": "Yalnız POST metodu dəstəklənir."}, status=405)

    try:
        body = json.loads(request.body)
        image_data = body.get('image')
        if not image_data:
            return JsonResponse({"status": "error", "message": "Şəkil göndərilməyib."})

        decoded_image = b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(decoded_image)).convert("RGB")
        image_np = np.array(image)

        encodings = face_recognition.face_encodings(image_np)
        if not encodings:
            return JsonResponse({"status": "error", "message": "Üz tanınmadı."})

        unknown_encoding = encodings[0]
        now = timezone.now().astimezone(baku_tz)

        for worker in Worker.objects.filter(is_active=True):
            if not worker.face_encoding:
                continue

            try:
                stored_encoding = np.frombuffer(
                    base64.b64decode(worker.face_encoding), dtype=np.float64
                )
                distance = face_recognition.face_distance([stored_encoding], unknown_encoding)[0]

                if distance < 0.5:
                    # Mövcud qeydiyyatı tap
                    attendance = Attendance.objects.filter(
                        worker=worker,
                        check_in_time__date=now.date()
                    ).order_by('-check_in_time').first()

                    if attendance and attendance.is_checked_in and not attendance.check_out_time:
                        attendance.mark_check_out()
                        action = "check_out"
                        message = f"{worker.worker_name} {worker.worker_surname} çıxış etdi."
                    elif attendance and not attendance.is_checked_in:
                        attendance.mark_check_in()
                        action = "check_in"
                        message = f"{worker.worker_name} {worker.worker_surname} ikinci dəfə giriş etdi."
                    else:
                        # Heç bir qeydiyyat yoxdursa
                        attendance = Attendance.objects.create(
                            worker=worker,
                            check_in_time=now,
                            is_checked_in=True
                        )
                        attendance.check_if_holiday()
                        action = "check_in"
                        message = f"{worker.worker_name} {worker.worker_surname} işə gəldi."

                    return JsonResponse({
                        "status": "success",
                        "message": message,
                        "worker_id": worker.id,
                        "type": action,
                        "time": now.strftime("%H:%M:%S"),
                        "date": now.strftime("%d %B %Y"),
                        "department": worker.department.department_name if worker.department else "Yoxdur",
                        "position": worker.position.position_name if worker.position else "Yoxdur",
                        "full_name": f"{worker.worker_name} {worker.worker_surname}"
                    })

            except Exception as e:
                logger.warning(f"Worker encoding parsing xətası: {worker.email} - {str(e)}")
                continue

        return JsonResponse({"status": "error", "message": "Tanınan işçi tapılmadı."})

    except Exception as e:
        logger.error(f"Ümumi xəta: {str(e)}")
        return JsonResponse({"status": "error", "message": f"Xəta baş verdi: {str(e)}"})
