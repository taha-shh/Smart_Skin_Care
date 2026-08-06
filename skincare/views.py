import json
from PIL import Image
import google.generativeai as genai
import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatSession, ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
import markdown

CHATBOT_API_KEY = os.getenv('GOOGLE_API_KEY') or os.getenv('CHATBOT_API_KEY')
genai.configure(api_key=CHATBOT_API_KEY)

def skin_chat_bot(request, session_id=None):
    if session_id:
        chat_session = get_object_or_404(ChatSession, id=session_id)
    elif request.user.is_authenticated:
        chat_session = ChatSession.objects.filter(user=request.user).order_by('-created_at').first()
        if not chat_session:
            chat_session = ChatSession.objects.create(user=request.user)
    else:
        guest_session_id = request.session.get('guest_session_id')
        if guest_session_id:
            try:
                chat_session = ChatSession.objects.filter(id=session_id).first()
                if not chat_session:
                 return redirect('skin_chat_new')
            except ChatSession.DoesNotExist:
                chat_session = ChatSession.objects.create(user=None)
                request.session['guest_session_id'] = chat_session.id
        else:
            chat_session = ChatSession.objects.create(user=None)
            request.session['guest_session_id'] = chat_session.id

    if request.method == 'POST':
        user_text = request.POST.get('message_text', '').strip()
        user_image = request.FILES.get('message_image')

        if user_text or user_image:
            user_msg = ChatMessage.objects.create(
                session=chat_session,
                sender='user',
                text_content=user_text,
                image=user_image
            )

            try:
                system_instruction = (
                    "أنت 'طبيب البشرة الذكي'، مستشار خبير في العناية بالبشرة والجلدية. "
                    "أجب بلغة عربية طبية سهلة وبأسلوب ودود ومختصر."
                )

                model = genai.GenerativeModel(
                    model_name='gemini-2.5-flash',
                    system_instruction=system_instruction
                )

                contents = []
                if user_text:
                    contents.append(user_text)

                if user_msg.image:
                    img = Image.open(user_msg.image.path)
                    img.thumbnail((1024, 1024))
                    contents.append(img)

                response = model.generate_content(contents)
                ai_response_text = response.text
                formatted_response = markdown.markdown(ai_response_text)

                ChatMessage.objects.create(
                    session=chat_session,
                    sender='ai',
                    text_content=  formatted_response
                )

            except Exception as e:
                ChatMessage.objects.create(
                    session=chat_session,
                    sender='ai',
                    text_content=f"تعذر الاتصال بالخادم الطبي حالياً. يرجى التأكد من جودة الاتصال بالشبكة وإعادة المحاولة. التفاصيل: {str(e)}"
                )

            return redirect('skin_chat_session', session_id=chat_session.id)

    all_messages = chat_session.messages.all().order_by('timestamp')
    return render(request, 'skin_chat.html', {
        'chat_session': chat_session,
        'all_messages': all_messages
    })

def register_page(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password_input != confirm_password:
            messages.error(request, "كلمات المرور غير متطابقة.")
            return render(request, 'register.html')
        if not User.objects.filter(username=username_input).exists():
            user = User.objects.create_user(username=username_input, email=email_input, password=password_input)
            messages.success(request, "تم انشاء الحساب بنجاح")
            return redirect('login') 
        else:
            messages.error(request, "اسم المستخدم موجود مسبقاً.")
    return render(request, 'register.html')

def login_page(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        user = authenticate(request, username=username_input, password=password_input)
        if user is not None:
            login(request, user) 
            return redirect('home')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور خاطئة.")
    return render(request, 'login.html')

def home_page(request):
    latest_session_id = None
    if request.user.is_authenticated:
        latest_session = ChatSession.objects.filter(user=request.user).order_by('-created_at').first()
        if latest_session:
            latest_session_id = latest_session.id
    return render(request, 'index.html', {'latest_session_id': latest_session_id})

def about_page(request):
    return render(request, 'Aboutus.html')

def products_page(request):
    return render(request, 'LocalProducts.html')

def upload_skin_image(request):
    return render(request, 'upload_image.html')