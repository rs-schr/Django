from django.shortcuts import render, redirect
from django.contrib import messages
import openai
import os
from dotenv import load_dotenv
load_dotenv()

from . models import Past
# Create your views here.
def home(request):
    # check for home submission

    if request.method == "POST":
        #os.environ['REQUESTS_CA_BUNDLE'] = 'C:\\prg\\sni.cloudflaressl.com.crt'
        question = request.POST["question"]
        past_response = request.POST["past_response"]

        # API ChatGBT
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.Model.list()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        # Parse the response
        print(response["choices"])
        response =response["choices"][0]["text"]
        response = response.replace("\n", "<br/>")
        # Logig for past response
        if "null" in past_response:
            past_response = response
        else:
            past_response = f"{past_response}<br/><br/>{response}"

        # save to database
        record = Past(question=question, response=response)
        record.save()
        return render(request, 'chatbot/home.html', {"question":question, "response":response, "past_response":past_response})

    return render(request, 'chatbot/home.html', {})

def past(request):
    past = Past.objects.all()
    return render(request, 'chatbot/past.html', {"past":past})

def delete_past(request, Past_id):
    past = Past.objects.get(id=Past_id)
    past.delete()
    messages.success(request, ('Past has been deleted!'))
    return redirect('past')
