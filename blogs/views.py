from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Article, Comment


class IndexView(generic.ListView):
    template_name = 'blogs/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        return Article.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DeleteView):
    model = Article
    template_name = 'blogs/detail.html'

    def get_queryset(self):
        return Article.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DeleteView):
    model = Article
    template_name = 'blogs/results.html'


def add(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    try:
        comment_id = request.POST.get('comment_id')
        comment_content = request.POST.get('comment_content')
        time = timezone.now()
    except(KeyError):
        return render(request, 'blogs/detail.html', {
            'article': article,
            'error_message': "用户名或评论内容为空！",
        })
    else:
        comment = Comment(article=article, comment_id=comment_id, comment_content=comment_content, pub_date=time)
        comment.save()
        return HttpResponseRedirect(reverse('blogs:results', args=(article.id,)))

