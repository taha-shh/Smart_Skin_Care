from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    
    SKIN_TYPES = [
        ('dry', 'جافة'),
        ('oily', 'دهنية'),
        ('mixed', 'مختلطة'),
        ('sensitive', 'حساسة'),
    ]
    
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPES, blank=True, null=True, verbose_name="نوع البشرة")
    medical_history = models.TextField(blank=True, null=True, verbose_name="السجل الطبي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "ملف المستخدم"
        verbose_name_plural = "ملفات المستخدمين"
        ordering = ['-created_at']

    def str(self):
        return f"ملف المستخدم: {self.user.username}"


class SkinAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="المستخدم")
    image = models.ImageField(upload_to='skin_images/', verbose_name="صورة البشرة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التحليل")
    ai_prediction = models.CharField(max_length=255, null=True, blank=True, verbose_name="التشخيص")
    ai_confidence = models.FloatField(null=True, blank=True, verbose_name="نسبة الثقة")
    skin_routine = models.TextField(null=True, blank=True, verbose_name="الروتين الموصى به")
    recommended_products = models.TextField(null=True, blank=True, verbose_name="المنتجات المقترحة")
    recommendations = models.TextField(null=True, blank=True, verbose_name="توصيات إضافية")

    class Meta:
        verbose_name = "تحليل البشرة"
        verbose_name_plural = "تحليلات البشرة"
        ordering = ['-created_at']

    def str(self):
        return f"تحليل رقم {self.id} - {self.user.username if self.user else 'زائر'}"


class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="المستخدم")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ بدء المحادثة") 

    class Meta:
        verbose_name = "جلسة محادثة"
        verbose_name_plural = "جلسات المحادثة"
        ordering = ['-created_at']

    def str(self):
        return f"محادثة رقم {self.id} - {self.user.username if self.user else 'زائر'}"


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', verbose_name="جلسة المحادثة")
    
    SENDER_CHOICES = [
        ('user', 'المريض'),
        ('ai', 'الذكاء الاصطناعي'),
    ]
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="المرسل")
    text_content = models.TextField(null=True, blank=True, verbose_name="نص الرسالة")
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True, verbose_name="الصورة المرفقة")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="توقيت الرسالة")

    class Meta:
        verbose_name = "رسالة"
        verbose_name_plural = "رسائل المحادثات"
        ordering = ['timestamp']

    def str(self):
        return f"رسالة من {self.get_sender_display()} في المحادثة {self.session.id}"