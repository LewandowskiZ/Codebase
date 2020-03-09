import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Article


class ArticleModelTests(TestCase):

    def test_was_published_recently_with_future_article(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_article = Article(pub_date=time)
        self.assertIs(future_article.was_published_recently(), False)

    def test_was_published_recently_with_old_article(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_article = Article(pub_date=time)
        self.assertIs(old_article.was_published_recently(), False)

    def test_was_published_recently_with_recent_article(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_article = Article(pub_date=time)
        self.assertIs(recent_article.was_published_recently(), True)


def create_article(article_title, article_content, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Article.objects.create(article_title=article_title, article_content=article_content, pub_date=time)


class ArticleIndexViewTests(TestCase):
    def test_no_article(self):
        response = self.client.get(reverse('blogs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No blogs are available.")
        self.assertQuerysetEqual(response.context['latest_article_list'], [])

    def test_past_article(self):
        create_article(article_title="Past article.", article_content=" ", days=-30)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: Past article.>']
        )

    def test_future_article(self):
        create_article(article_title="Future article.", article_content=" ", days=30)
        response = self.client.get(reverse('blogs:index'))
        self.assertContains(response, "No blogs are available.")
        self.assertQuerysetEqual(response.context['latest_article_list'], [])

    def test_future_article_and_past_article(self):
        create_article(article_title="Past article.", article_content=" ", days=-30)
        create_article(article_title="Future article.", article_content=" ", days=30)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: Past article.>']
        )

    def test_two_past_questions(self):
        create_article(article_title="Past article 1.", article_content=" ", days=-30)
        create_article(article_title="Past article 2.", article_content=" ", days=-5)
        response = self.client.get(reverse('blogs:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: Past article 2.>', '<Article: Past article 1.>']
        )


class ArticleDetailViewTests(TestCase):
    def test_future_article(self):
        future_article = create_article(article_title="Future article.", article_content=" ", days=30)
        url = reverse('blogs:detail', args=(future_article.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_article(self):
        past_article = create_article(article_title="Past article.", article_content=" ", days=-30)
        url = reverse('blogs:detail', args=(past_article.id,))
        response = self.client.get(url)
        self.assertContains(response, past_article.article_title)