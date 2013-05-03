import os
import redis
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic.list_detail import object_list
from models import Article, Edit
from forms import ArticleForm, EditForm
from story.tasks import send_published_article

@login_required 
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            msg = "Article saved successfully"
            messages.success(request, msg, fail_silently=True)
            if article.is_published:
                subject = article.title
                body = article.text
                attachment = article.docfile.url
                send_published_article.delay(request.user.email,
                                             subject,
                                             body,
                                             attachment)
                msg = "Article saved and published successfully"
                messages.success(request, msg, fail_silently=True)
            return redirect(article)
    else:
        form = ArticleForm()
    return render_to_response('story/article_form.html', 
                              { 'form': form },
                              context_instance=RequestContext(request))

@login_required 
def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None, instance=article)
    edit_form = EditForm(request.POST or None)
    if form.is_valid():
        article = form.save()
        if article.is_published:
                subject = article.title
                body = article.text
                attachment = article.docfile.url
                send_published_article.delay(request.user.email, subject, body, attachment)
                msg = "Article saved and published successfully"
                messages.success(request, msg, fail_silently=True)
        if edit_form.is_valid():
            edit = edit_form.save(commit=False)
            edit.article = article
            edit.editor = request.user
            edit.save()
            msg = "Article updated successfully"
            messages.success(request, msg, fail_silently=True)
            return redirect(article)
    return render_to_response('story/article_form.html', 
                              { 
                                  'form': form,
                                  'edit_form': edit_form,
                                  'article': article,
                              },
                              context_instance=RequestContext(request))
@login_required 
def article_history(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return  object_list(request, 
                        queryset=Edit.objects.filter(article__slug=slug),
                        extra_context={'article': article})
