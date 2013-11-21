import os
import redis
import time
import datetime
from tools.killgremlins import killgremlins, replace_all
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import smart_str, smart_unicode, force_unicode
from notification import models as notification
from story.models import Article
from story.forms import *
from story.tasks import send_published_article
from apps.account.models import UserProfile



@login_required 
def inprogress_index(request):
    """
    Stories in progress view, a list of all stories in progress
    """
    inprogress_list = Article.objects.filter(is_published=False).order_by('-publish_date')
    paginator = Paginator(inprogress_list, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('story/article_inprogress_list.html', RequestContext(request, {
        'lines': show_lines, 'inprogress_list': inprogress_list,
    }))


@login_required 
def story_index(request):
    """
    Story index view, a list of all published stories
    """
    story_list = Article.objects.filter(is_published=True).order_by('-publish_date')
    paginator = Paginator(story_list, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('story/article_list.html', RequestContext(request, {
        'lines': show_lines, 
    }))

 
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
            article.author = request.user
            article.publish_date = datetime.datetime.now()
            cleaned_text = replace_all(article.text)
            article.text = cleaned_text
            article.save()
            form.save_m2m()
            msg = "Article saved successfully"
            messages.success(request, msg, fail_silently=True)
            if article.is_published and article.send_now and article.publish_date <= datetime.datetime.today():
                subject = article.title
                byline = article.byline
                email_text = article.email_text
                story_text = article.text 
                bc_only = form.cleaned_data['broadcast_only']
                recipients = []
                date_string = time.strftime("%Y-%m-%d-%H-%M")
                logFile = open('static/email_logs/sent_emails-' + date_string + '.txt', 'w')
                logFile.write("Recipients for " + date_string + ":\n")
                logFile.close()
                for profile in UserProfile.objects.filter(user_type = 'Editor'):
                    recipients.append(profile.user.email)
                for profile in UserProfile.objects.filter(user_type = 'Reporter'):        
                    recipients.append(profile.user.email)
                if bc_only:
                    for profile in UserProfile.objects.filter(Q(user_type = 'Client') & (Q(pub_type = 'Radio') | Q(pub_type = 'Television'))):
                        recipients.append(profile.user.email)
                else:
                    for profile in UserProfile.objects.filter(user_type = 'Client'):        
                        recipients.append(profile.user.email)
                for r in recipients:
                    if article.docfile is not None:
                        attachment = article.docfile
                        send_published_article.delay(date_string, request.user.email, r, subject,
                                                        byline, email_text, story_text, attachment)
                    else:
                        send_published_article.delay(date_string, request.user.email, r, subject,
                                                        byline, email_text, story_text)
                msg = "Article published successfully"
                messages.success(request, msg, fail_silently=True)
            return redirect(article)
    else:
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm(initial={'byline': request.user.get_profile().byline})
        elif request.user.get_profile().user_type == 'Editor':
            form = Article_EForm(initial={'byline': request.user.get_profile().byline,
                         'email_text': '<p>Editors/News Directors:</p><p></p><p>Thank you,</p><p>Nebraska News Service</p>'})
            form.fields['author'].queryset = UserProfile.objects.filter(Q(user_type = 'Reporter') | Q(user_type = 'Editor'))
        else:
            form = Article_RForm(initial={'byline': request.user.get_profile().byline})
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
            cleaned_text = replace_all(article.text)
            article.text = cleaned_text
            article = form.save()
            msg = "Article updated successfully"
            messages.success(request, msg, fail_silently=True)
            if article.is_published and article.send_now and article.publish_date <= datetime.datetime.today():
                subject = article.title
                byline = article.byline
                email_text = article.email_text
                story_text = article.text 
                bc_only = form.cleaned_data['broadcast_only']
                recipients = []
                date_string = time.strftime("%Y-%m-%d-%H-%M")
                logFile = open('static/email_logs/sent_emails-' + date_string + '.txt', 'w')
                logFile.write("Recipients for " + date_string + ":\n")
                logFile.close()
                for profile in UserProfile.objects.filter(user_type = 'Editor'):
                    recipients.append(profile.user.email)
                for profile in UserProfile.objects.filter(user_type = 'Reporter'):        
                    recipients.append(profile.user.email)
                if bc_only:
                    for profile in UserProfile.objects.filter(Q(user_type = 'Client') & (Q(pub_type = 'Radio') | Q(pub_type = 'Television'))):
                        recipients.append(profile.user.email)
                else:
                    for profile in UserProfile.objects.filter(user_type = 'Client'):        
                        recipients.append(profile.user.email)
                for r in recipients:
                    if article.docfile is not None:
                        attachment = article.docfile
                        send_published_article.delay(date_string, request.user.email, r, subject,
                                                        byline, email_text, story_text, attachment)
                    else:
                        send_published_article.delay(date_string, request.user.email, r, subject,
                                                        byline, email_text, story_text)
                msg = "Article published successfully"
                messages.success(request, msg, fail_silently=True)
            return redirect(article)
    else:
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm(instance=article, initial={'byline': article.author.get_profile().byline})
        elif request.user.get_profile().user_type == 'Editor':
            if article.email_text:
                form = Article_EForm(instance=article, initial={'email_text': article.email_text})
                form.fields['author'].queryset = UserProfile.objects.filter(Q(user_type = 'Reporter') | Q(user_type = 'Editor'))
            else:
                form = Article_EForm(instance=article,
                    initial={'byline': article.author.get_profile().byline,
                             'email_text': '<p>Editors/News Directors:</p><p></p><p>Thank you,</p><p>Nebraska News Service</p>'})
                form.fields['author'].queryset = UserProfile.objects.filter(Q(user_type = 'Reporter') | Q(user_type = 'Editor'))
        else:
            form = Article_RForm(instance=article, initial={'byline': article.author.get_profile().byline})
    return render_to_response('story/article_form.html', 
                              { 
                                  'form': form,
                                  'article': article,
                              },
                              context_instance=RequestContext(request))