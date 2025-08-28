from django.http import JsonResponse
from .logic import chatbot

def chat(request):
    user_message = request.GET.get("message", "")
    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)
    
    bot_reply = chatbot.get_response(user_message)
    return JsonResponse({"reply": bot_reply})
