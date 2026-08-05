from django.contrib import admin
from .models import UserProfile , SkinAnalysis
admin.site.register(UserProfile)

@admin.register(SkinAnalysis)
class SkinAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user' , 'ai_prediction' , 'ai_confidence' , 'created_at')

    fields = ('user' , 'image' ,  'ai_prediction' , 'ai_confidence' , 'skin_routine' , 'recommended_products' , 'recommendations')