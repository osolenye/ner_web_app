from django.shortcuts import render
from django.http import JsonResponse
import json
import spacy
from .models import QueryHistory  # Импортируем модель

# Загрузка модели spaCy
nlp = spacy.load("en_core_web_sm")  # Для русского языка: "ru_core_news_sm"


def index(request):
    # Получаем историю запросов
    history = QueryHistory.objects.only("text", "entities", "created_at").order_by('-created_at')[:10]
    return render(request, 'index.html', {'history': history})


def extract_entities(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()

        if not text:
            return JsonResponse({"error": "No text provided"}, status=400)

        doc = nlp(text)

        # Извлечение именованных сущностей
        entities = [{"label": ent.label_, "text": ent.text} for ent in doc.ents]

        # Сохранение запроса в базу данных
        QueryHistory.objects.create(text=text, entities=json.dumps(entities))

        # Получаем историю запросов
        history = QueryHistory.objects.only("text", "entities", "created_at").order_by('-created_at')[:10]

        return render(request, 'index.html', {'entities': entities, 'history': history})

    return index(request)
