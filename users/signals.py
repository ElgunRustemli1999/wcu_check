from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import CustomUser, Worker
import face_recognition
import numpy as np
import base64
import os
import logging

logger = logging.getLogger(__name__)

# ========================= 1. CustomUser yarandıqda Worker yaradılır =========================
@receiver(post_save, sender=CustomUser)
def create_worker_if_not_exists(sender, instance, created, **kwargs):
    if created:
        Worker.objects.create(
            worker_name=instance.first_name or "",
            worker_surname=instance.last_name or "",
            email=instance.email,
            phone_number=instance.phone_number,
            is_hr=instance.is_hr,
            is_manager=instance.is_manager,
            is_employee=instance.is_employee,
            contract_start_date=instance.contract_start_date,
            contract_end_date=instance.contract_end_date,
        )

# ========================= 2. CustomUser yenilənəndə Worker sync olunur =========================
@receiver(post_save, sender=CustomUser)
def sync_worker_from_user(sender, instance, **kwargs):
    try:
        worker = Worker.objects.get(email=instance.email)
        worker.worker_name = instance.first_name or ""
        worker.worker_surname = instance.last_name or ""
        worker.phone_number = instance.phone_number
        worker.is_hr = instance.is_hr
        worker.is_manager = instance.is_manager
        worker.is_employee = instance.is_employee
        worker.contract_start_date = instance.contract_start_date
        worker.contract_end_date = instance.contract_end_date
        worker.save()
    except Worker.DoesNotExist:
        pass

# ========================= 3. Worker yaradıldıqda encoding alınır =========================
@receiver(post_save, sender=Worker)
def generate_face_encoding(sender, instance, created, **kwargs):
    def process_encoding():
        try:
            if instance.face_image and os.path.exists(instance.face_image.path):
                image = face_recognition.load_image_file(instance.face_image.path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    instance.face_encoding = base64.b64encode(encodings[0].tobytes()).decode('utf-8')
                    instance.save()
        except Exception as e:
            logger.error(f"Üz encoding alınarkən xəta baş verdi: {e}")

    # Fayl tam olaraq yazıldıqdan sonra encoding prosesi başlasın
    if created:
        transaction.on_commit(process_encoding)
