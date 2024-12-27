from django.http import HttpResponse
from django.template import loader

from .models import note


def index(request):
    latest_question_list = note.objects.order_by("-pub_date")[:5]
    template = loader.get_template("note/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, note_id):
    return HttpResponse("You're looking at notes %s." % note_id)