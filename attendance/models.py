from django.db import models
from users.models import Worker
from django.utils import timezone
from core.models import Holiday

class Attendance(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True)
    check_out_time = models.DateTimeField(null=True,blank=True)
    is_checked_in = models.BooleanField(default=False)


    extra_hours = models.FloatField(default=0)
    late_minutes = models.IntegerField(default=0)
    is_holiday = models.BooleanField(default=False)
    early_leave = models.CharField(max_length=100,null=True, blank=True)

    is_approved_leave = models.BooleanField(default=False) # Icaze Tesdiqlenibmi?
    is_absent = models.BooleanField(default=False) #Ishe gelmeyibmi?
    #default_check_out_time = models.DateTimeField(default=timezone.now().replace(hour=14, minute=0,second=0, microsecond=0))
    status = models.CharField(max_length=20, choices=[
        ('ontime', 'Vaxtında gəlib'),
        ('late', 'Gec gəlib'),
        ('absent', 'Gəlməyib'),
        ('early_leave', 'Tez çıxıb'),
        ], null=True, blank=True)


    def __str__(self):
        return f"{self.worker.worker_name} - {self.check_in_time.date() if self.check_in_time else 'No check-in'}"
    
    def mark_check_in(self):
        """Check-in zamani"""
        if not self.is_checked_in:
            self.check_in_time = timezone.now()
            self.is_checked_in = True
            self.check_if_holiday()
            self.save()
    
    def mark_check_out(self):
        """Check-out zamanı"""
        if self.is_checked_in:
            self.check_out_time = timezone.now()
            self.is_checked_in = False
            self.calculate_hours()
            self.save()
    

    def calculate_hours(self):
        """Gecikmə, əlavə saat və tez çıxma hesablaması"""
        if self.check_in_time and self.check_out_time:
            # Gözlənilən giriş saatı
            if self.worker.working_type == 'full_time':

                standart_check_in = self.check_in_time.replace(hour=9, minute=0, second=0, microsecond=0)
                expected_hours = 9
            elif self.worker.working_type == 'part_time_moring':
                standart_check_in = self.check_in_time.replace(hour=9,minute=0, second=0, microsecond=0)
                expected_hours = 4
            elif self.worker.working_type == 'part_time_afternoon':
                standart_check_in = self.check_in_time.replace(hour=14, minute=0, second=0, microsecond=0)
                expected_hours = 4
            


            #gecikme
            if self.check_in_time > standart_check_in:
                delta = self.check_in_time - standart_check_in
                self.late_minutes = int(delta.total_seconds() / 60)

            # İş saatları və əlavə saat

            work_duration = self.check_out_time - self.check_in_time
            total_hours = work_duration.total_seconds() / 3600

            if total_hours> expected_hours:
                self.extra_hours = round(total_hours - expected_hours, 2)
            
            # Tez çıxma

            if self.check_out_time < self.get_expected_check_out_time():
                self.early_leave = (
                    "Tez Çıxma - İcazəli" if getattr(self.worker, "has_permission_to_leave_early", False)
                    else 'Tez Çıxma - İcazəsiz'
                )
    def auto_check_out(self):
        """Əgər işçi çıxış etməyibsə, avtomatik saat 18:00-a kimi çıxış əlavə et"""
        if self.is_checked_in and not self.check_out_time:
            self.check_out_time = self.get_expected_check_out_time()
            self.is_checked_in = False
            self.calculate_hours()
            self.save()


            
    def get_expected_check_out_time(self):
        today = timezone.now()
        if getattr(self.worker, "has_permission_to_leave_early", False):
            return today.replace(hour=14, minute=0, second=0, microsecond=0)
        return today.replace(hour=18, minute=0, second=0, microsecond=0)

    def check_if_holiday(self):
        """Bayram günü olub olmadığını yoxla (verilənlər bazasından)"""
        today = timezone.now().date()
        self.is_holiday = Holiday.objects.filter(date=today).exists()
        return self.is_holiday
    


    def is_work_day(self):
        """İş günü olub-olmamasını yoxla"""
        return timezone.now().weekday() < 5
    
    def is_absent_or_not_working(self):
        """İşçi gəlibmi? İş günü və ya bayramdı?"""
        return not self.is_work_day( ) or self.is_holiday or not self.is_checked_in











