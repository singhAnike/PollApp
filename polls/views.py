from django.shortcuts import get_object_or_404, render, HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question, Choice


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# Writing more views

# command way to deal with page not find 404 issue 
# ...
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})


class DetailView(generic.DetailView):
    model = Question
    template_name = "templates/polls/detail.html" 
# here we need to give a path manually becouse
# here i am give diffrent name of the project but in case of django documnets project name and inside template directory same name as a polls


class ResultsView(generic.DetailView):
    model = Question
    template_name = "templates/polls/results.html"


# this is the dumy of the vote method
# def vote(request, question_id):
#     return HttpResponse("you're voting on question %s." % question_id)


# Real vote method
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) # here i am alter a server
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "templates/polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# Here is new index page
class IndexView(generic.ListView):
    template_name = "templates/polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5] 