import os
import redis
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.list_detail import object_list
from story.models import Article
from story.forms import ArticleForm
from story.tasks import send_published_article

@login_required 
def inprogress_index(request):
    """
    Stories in progress view, a list of all stories in progress
    """
    inprogress_list = Article.objects.filter(is_published=False)
    return render_to_response('story/article_inprogress_list.html',
                              {'inprogress_list': inprogress_list})

@login_required 
def add_article(request):
    """
    Create new article
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            msg = "Article saved successfully"
            messages.success(request, msg, fail_silently=True)
            if article.is_published and article.publish_date <= datetime.datetime.today():
                subject = article.title
                email_text = article.email_text
                story_text = article.title + '\n' + 'By ' + article.author.get_full_name() + '\n' + article.text#This is a bad idea, move to template, make more variables
                
                docfile = article.docfile
                try:
                    attachment = docfile
                    send_published_article.delay(request.user.email,
                                                 subject,
                                                 email_text,
                                                 story_text,
                                                 attachment)
                except:
                    send_published_article.delay(request.user.email,
                                                 subject,
                                                 email_text,
                                                 story_text)
                msg = "Article published successfully"
                messages.success(request, msg, fail_silently=True)
            return redirect(article)
    else:
        form = ArticleForm()
    return render_to_response('story/article_form.html', 
                              { 'form': form },
                              context_instance=RequestContext(request))

@login_required 
def edit_article(request, slug):
    """
    Update existing article
    """
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            msg = "Article updated successfully"
            messages.success(request, msg, fail_silently=True)
            if article.is_published and article.publish_date <= datetime.datetime.today():
                subject = article.title
                email_text = article.email_text
                story_text = article.text
                if article.docfile is not None:
                    attachment = article.docfile
                    send_published_article.delay(request.user.email,
                                                 subject,
                                                 email_text,
                                                 story_text,
                                                 attachment)
                else:
                    send_published_article.delay(request.user.email,
                                                 subject,
                                                 email_text,
                                                 story_text)
                                                 
                msg = "Article published successfully"
                messages.success(request, msg, fail_silently=True)   
            return redirect(article)
    else:
        form = ArticleForm(instance=article)
    return render_to_response('story/article_form.html', 
                              { 
                                  'form': form,
                                  'article': article,
                              },
                              context_instance=RequestContext(request))

@login_required 
def article_history(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return  object_list(request, 
                        queryset=Edit.objects.filter(article__slug=slug),
                        extra_context={'article': article})
