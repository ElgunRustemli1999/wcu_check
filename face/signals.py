import face_recognition
import numpy as np
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Worker

@receiver(post_save, sender=Worker)
def generate_face_encoding(sender, instance, **kwargs):
    if instance.face_image and not instance.face_encoding:
        try:
            # Şəkil faylını yükləyirik
            image_path = instance.face_image.path
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                encoding = encodings[0]
                # Numpy array-i list şəklində string formatında saxlayırıq
                instance.face_encoding = str(list(encoding))
                instance.save()
        except Exception as e:
            print(f"Üz encoding yaratmaqda xəta: {e}")
