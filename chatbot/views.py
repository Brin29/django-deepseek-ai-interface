from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from .models import Chat
from django.views.decorators.csrf import csrf_exempt
import json

client = OpenAI(api_key="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", base_url="https://openrouter.ai/api/v1")

# Create your views here.
def ask_openai(message):
    response = client.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages=[
        {
            "role": "user",
            "content": message
        }
        ]
    )

    answer = response.choices[0].message.content
    return answer
    

@csrf_exempt  # Esto es necesario si no estás utilizando CSRF tokens en tu API
def chatbot(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        message = data.get('message')

        if message:
            response = ask_openai(message)
            chat = Chat(message=message, response=response)
            chat.save()
            return JsonResponse({'message': message, 'response': response})
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)
