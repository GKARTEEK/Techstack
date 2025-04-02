from django.http import JsonResponse
from languages.models import Topic

def get_topics(request):
    language_id = request.GET.get('language')
    if not language_id:
        return JsonResponse([], safe=False)
    
    topics = Topic.objects.filter(language_id=language_id).values('id', 'name')
    return JsonResponse(list(topics), safe=False)