from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    SKIN_TYPES = [
        ('dry', 'جافة'),
        ('oily', 'دهنية'),
        ('mixed', 'مختلطة'),
        ('sensitive', 'حساسة'),
    ]
    
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPES, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"ملف المستخدم: {self.user.username}"


class SkinAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='skin_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    ai_prediction = models.CharField(max_length=255, null=True, blank=True)
    ai_confidence = models.FloatField(null=True, blank=True)
    skin_routine = models.TextField(null=True, blank=True)
    recommended_products = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    def str(self):
        return f"Analysis {self.id} - {self.user.username if self.user else 'Guest'}"


class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def str(self):
        return f"محادثة رقم {self.id} - {self.user.username if self.user else 'Guest'}"


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    
    SENDER_CHOICES = [
        ('user', 'المريض'),
        ('ai', 'الذكاء الاصطناعي'),
    ]
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    text_content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"رسالة من {self.get_sender_display()} في المحادثة {self.session.id}"