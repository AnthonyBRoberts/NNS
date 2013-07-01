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
from story.forms import *
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
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm(request.POST, request.FILES or None)
            form.author = request.user
            form.publish_date = datetime.datetime.now()
        elif request.user.get_profile().user_type == 'Editor':
            form = Article_EForm(request.POST, request.FILES or None)
        else:
            form = Article_RForm(request.POST, request.FILES or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.publish_date = datetime.datetime.now()
            article.save()
            article.author.add(request.user)
            msg = "Article saved successfully"
            messages.success(request, msg, fail_silently=True)
            if article.is_published and article.publish_date <= datetime.datetime.today():
                subject = article.title
                email_text = article.email_text
                story_text = article.text
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
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm()
        elif request.user.get_profile().user_type == 'Editor':
            form = Article_EForm()
        else:
            form = Article_RForm()
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
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm(request.POST, request.FILES, instance=article)
            form.publish_date = datetime.datetime.now()
        elif request.user.get_profile().user_type == 'Editor':
            form = Article_EForm(request.POST, request.FILES, instance=article)
        else:
            form = Article_RForm(request.POST, request.FILES, instance=article)
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
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm(instance=article)
        elif request.user.get_profile().user_type == 'Editor':
            form = Article_EForm(instance=article)
        else:
            form = Article_RForm(instance=article)
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
