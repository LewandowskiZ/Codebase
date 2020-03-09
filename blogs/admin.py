from django.contrib import admin

from .models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['article_title']
    fieldsets = [
        (None, {'fields': ['article_title']}),
        (None, {'fields': ['article_content']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [CommentInline]


admin.site.register(Article, ArticleAdmin)

