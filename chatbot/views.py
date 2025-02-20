from django.http import JsonResponse
from openai import OpenAI
from .models import Chat
from django.views.decorators.csrf import csrf_exempt
import PyPDF3
import json

client = OpenAI(api_key="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", base_url="https://openrouter.ai/api/v1")

# Create your views here.
def ask_openai(message):
    pdf_file = open("nomina.pdf", "rb")
    pdf_reader = PyPDF3.PdfFileReader(pdf_file)

    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text = page.extractText()

        response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {
                "role": "user",
                "content": message + text
            }
            ]
        )

        answer = response.choices[0].message.content.strip()
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
