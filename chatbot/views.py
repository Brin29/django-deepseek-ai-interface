from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI

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
    


def chatbot(request):
    # response_data = {'message': 'Hello World'}
    # return JsonResponse(response_data)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')