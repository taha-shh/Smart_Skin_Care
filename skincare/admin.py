from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, SkinAnalysis, ChatSession, ChatMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'skin_type', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('skin_type', 'created_at')


@admin.register(SkinAnalysis)
class SkinAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'display_image', 'ai_prediction', 'display_confidence', 'created_at')
    search_fields = ('user__username', 'ai_prediction')
    list_filter = ('ai_prediction', 'created_at')
    readonly_fields = ('display_image_large',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px; border-radius: 6px; object-fit: cover;" />', obj.image.url)
        return "بدون صورة"
    display_image.short_description = "الصورة"

    def display_image_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; border-radius: 8px;" />', obj.image.url)
        return "بدون صورة"
    display_image_large.short_description = "معاينة الصورة"

    def display_confidence(self, obj):
        return f"{obj.ai_confidence}%" if obj.ai_confidence else "-"
    display_confidence.short_description = "نسبة الثقة"


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('timestamp', 'display_chat_image')
    fields = ('sender', 'text_content', 'image', 'display_chat_image', 'timestamp')

    def display_chat_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 4px; object-fit: cover;" />', obj.image.url)
        return "-"
    display_chat_image.short_description = "صورة مرفقة"


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'short_text', 'timestamp')
    search_fields = ('text_content', 'session__user__username')
    list_filter = ('sender', 'timestamp')

    def short_text(self, obj):
        return obj.text_content[:40] + '...' if obj.text_content else 'صورة فقط'
    short_text.short_description = "محتوى الرسالة"


admin.site.site_header = "لوحة إدارة العناية الذكية بالبشرة"
admin.site.site_title = "العناية الذكية بالبشرة"
admin.site.index_title = "مرحباً بك في لوحة التحكم الإدارية"