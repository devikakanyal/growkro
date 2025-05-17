from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import google.generativeai as genai
from django.conf import settings

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash")

@csrf_exempt  # ✅ Exempts CSRF for testing (remove in production)
def get_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # ✅ Parse JSON
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"error": "Empty message received"}, status=400)

            # Send to Gemini AI
            response = model.generate_content([user_message])
            bot_reply = response.text if response else "Sorry, I couldn't generate a response."

            return JsonResponse({"response": bot_reply})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data received"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def animation(request):
    return render(request, "animation.html")

def home(request):
    return render(request, "homepage.html")
