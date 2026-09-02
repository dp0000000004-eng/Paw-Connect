
from django.shortcuts import render, redirect
from .models import Chat
from dotenv import load_dotenv
import os
import random
from openai import OpenAI
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def chat(request):

    # One of these lines is shown at the top of the chat UI
    greetings = [

    f"Nice to see you, {request.user.username}. What’s new?",
    f"Hey {request.user.username}, glad you’re here!",
    f"Good to catch up with you, {request.user.username}",
    f"Hello {request.user.username}, how’s your day going?",
    f"Great to have you around, {request.user.username}!",
    f"Hi {request.user.username}, always a pleasure!",
    f"{request.user.username}, it’s wonderful to see you again!",
    f"Hey there, {request.user.username} — what’s happening?",
    f"Welcome back, {request.user.username}!",
    f"{request.user.username}, you always brighten the chat!"
    
    ]


    # Form submitted (user typed a prompt). AI reply is currently disabled.
    if request.method == "POST":

        # Would load NVIDIA_AI_API_KEY when the API block is turned on

        chat = Chat()
    
        prompt = request.POST.get('prompt')
    
        client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = os.environ.get('NVIDIA_AI_API_KEY'),
            timeout=60.0
        )
    
        completion = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
    
        messages = [
            {
                "role":"assistant",
                "content":"don't give ans using .md format give in normal paragraph use white space tag insted " + prompt
            }
        ],
    
        temperature=1,
        top_p=0.95,
        max_tokens=1384,
        extra_body={"chat_template_kwargs":{"enable_thinking":True}},
        stream=True
        )
    
        response = ""
    
        for chunk in completion:
            if not chunk.choices:
                continue
            reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if reasoning:
                print(reasoning, end="")
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content + " "
    
    
        user = User.objects.get(username=request.user.username)
    
        chat.prompt = prompt
        chat.user = user
        chat.response = response
        chat.save()

    chats = Chat.objects.all()

    # Random greeting from the list above
    greets = random.choice(greetings)


    return render(
        request,
        'ai.html',
        {
            "chats":chats,  # Past Q&A — uncomment when Chat.save() is enabled
            "greets": greets
        }
    )
