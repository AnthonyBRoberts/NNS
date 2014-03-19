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
from django.views.generic import DetailView, ListView
from notification import models as notification
from story.models import Article, MediaItem
from story.forms import *
from story.management import send_article, notify_editor
from apps.account.models import UserProfile


class FrontpageView(DetailView):
    template_name = "welcome_content.html"
    def get_object(self):
        return get_object_or_404(Article, slug="front-page")
    def get_context_data(self, **kwargs):
        context = super(FrontpageView, self).get_context_data(**kwargs)
        context['slug'] = "front-page"
        queryset = UserProfile.objects.filter(user_type="Reporter")
        context['reporter_list'] = queryset
        return context

class AboutView(DetailView):
    template_name="about.html"
    def get_object(self):
        return get_object_or_404(Article, slug="about-us")
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['slug'] = "about-us"
        return context

class ReporterDocsView(DetailView):
    template_name="reporterdocs.html"
    def get_object(self):
        return get_object_or_404(Article, slug="reporter-documentation")
    def get_context_data(self, **kwargs):
        context = super(ReporterDocsView, self).get_context_data(**kwargs)
        context['slug'] = "reporter-documentation"
        return context

class EditorDocsView(DetailView):
    template_name="reporterdocs.html"
    def get_object(self):
        return get_object_or_404(Article, slug="editor-documentation")
    def get_context_data(self, **kwargs):
        context = super(EditorDocsView, self).get_context_data(**kwargs)
        context['slug'] = "editor-documentation"
        return context


@login_required 
def story_index(request):
    """
    Story index view, a list of all published stories
    """
    story_list = Article.objects.filter(is_published=True).order_by('-publish_date')
    paginator = Paginator(story_list, 20)
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
def inprogress_index(request):
    """
    Stories in progress view, a list of all stories in progress
    """
    inprogress_list = Article.objects.filter(is_published=False).order_by('-publish_date')
    paginator = Paginator(inprogress_list, 20)
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
def media_index(request):
    """
    Stories in progress view, a list of all stories in progress
    """
    media_list = MediaItem.objects.filter(is_published=True).order_by('-publish_date')
    paginator = Paginator(media_list, 20)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('story/media_list.html', RequestContext(request, {
        'lines': show_lines, 'media_list': media_list,
    }))

@login_required 
def media_inprogress_index(request):
    """
    Stories in progress view, a list of all stories in progress
    """
    media_list = MediaItem.objects.filter(is_published=False).order_by('-publish_date')
    paginator = Paginator(media_list, 20)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('story/media_inprogress_list.html', RequestContext(request, {
        'lines': show_lines, 'media_list': media_list,
    }))




@login_required 
def add_article(request):
    """
    Command for sending articles comes from management.py

    """
    if request.method == 'POST':
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm(request.POST, request.FILES or None)
            form.author = request.user
            form.publish_date = datetime.datetime.now()
        elif request.user.get_profile().user_type == 'Editor':
            form = Article_EForm(request.POST, request.FILES or None)
        else:
            form = Article_RForm()
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            if article.is_published:
                article.publish_date = datetime.datetime.now()
            cleaned_text = replace_all(article.text)
            article.text = cleaned_text
            article.save()
            form.save_m2m()
            msg = "Article saved successfully"
            messages.success(request, msg, fail_silently=True)
            if request.user.get_profile().user_type == 'Editor':
                if article.is_published and article.send_now:
                    send_article(article, form)
                    msg = "Article published successfully"
                    messages.success(request, msg, fail_silently=True)
            elif request.user.get_profile().user_type == 'Reporter':
                ready_for_editor = form.cleaned_data['ready_for_editor']
                if ready_for_editor:
                    notify_editor(article)
                    msg = "Editor has been notified."
                    messages.success(request, msg, fail_silently=True)
            return redirect(article)
    else:
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm(initial={'byline': request.user.get_profile().byline})
        elif request.user.get_profile().user_type == 'Editor':
            form = Article_EForm(initial={'byline': request.user.get_profile().byline,
                         'email_text': '<p>Editors/News Directors:</p><p></p><p>Thank you,</p><p>Nebraska News Service</p>'})
        else:
            form = Article_RForm()
    return render_to_response('story/article_form.html', 
                              { 'article_form': form },
                              context_instance=RequestContext(request))

@login_required 
def edit_article(request, slug):
    """
    Update existing article
    Command for sending articles comes from management.py
    """
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        if request.user.get_profile().user_type == 'Reporter':
            form = Article_RForm(request.POST, request.FILES, instance=article)
            form.publish_date = datetime.datetime.now()
        elif request.user.get_profile().user_type == 'Editor':
            form = Article_EForm(request.POST, request.FILES, instance=article)
        else:
            form = Article_RForm()
        if form.is_valid():
            cleaned_text = replace_all(article.text)
            article.text = cleaned_text
            article = form.save()
            msg = "Article updated successfully"
            messages.success(request, msg, fail_silently=True)
            if request.user.get_profile().user_type == 'Editor':
                if article.is_published and article.send_now:
                    send_article(article, form)
                    msg = "Article published successfully"
                    messages.success(request, msg, fail_silently=True)
            elif request.user.get_profile().user_type == 'Reporter':
                ready_for_editor = form.cleaned_data['ready_for_editor']
                if ready_for_editor:
                    notify_editor(article)
                    msg = "Editor has been notified."
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
        else:
            form = Article_RForm()
    return render_to_response('story/article_form.html', 
                              { 
                                  'article_form': form,
                                  'article': article,
                              },
                              context_instance=RequestContext(request))

@login_required 
def add_media(request):
    """
    Command for sending articles comes from management.py

    """
    if request.method == 'POST':
        if request.user.get_profile().user_type == 'Reporter':
            form = Media_RForm(request.POST, request.FILES or None)
            form.author = request.user
            form.publish_date = datetime.datetime.now()
        elif request.user.get_profile().user_type == 'Editor':
            form = Media_EForm(request.POST, request.FILES or None)
        else:
            form = Media_RForm()
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            if article.is_published:
                article.publish_date = datetime.datetime.now()
            cleaned_text = replace_all(article.text)
            article.text = cleaned_text
            article.save()
            form.save_m2m()
            msg = "Media saved successfully" 
            messages.success(request, msg, fail_silently=True)
            if request.user.get_profile().user_type == 'Editor':
                if article.is_published and article.send_now:
                    send_article(article, form)
                    msg = "Media published successfully"
                    messages.success(request, msg, fail_silently=True)
            elif request.user.get_profile().user_type == 'Reporter':
                ready_for_editor = form.cleaned_data['ready_for_editor']
                if ready_for_editor:
                    notify_editor(article)
                    msg = "Editor has been notified."
                    messages.success(request, msg, fail_silently=True)
            return redirect(article)
    else:
        if request.user.get_profile().user_type == 'Reporter':
            form = Media_RForm(initial={'byline': request.user.get_profile().byline})
        elif request.user.get_profile().user_type == 'Editor':
            form = Media_EForm(initial={'byline': request.user.get_profile().byline,
                         'email_text': '<p>Editors/News Directors:</p><p></p><p>Thank you,</p><p>Nebraska News Service</p>'})
        else:
            form = Media_RForm()
    return render_to_response('story/media_form.html', 
                              { 'form': form },
                              context_instance=RequestContext(request))

@login_required 
def edit_media(request, slug):
    """
    Update existing article
    Command for sending articles comes from management.py
    """
    article = get_object_or_404(MediaItem, slug=slug)
    if request.method == 'POST':
        if request.user.get_profile().user_type == 'Reporter':
            form = Media_RForm(request.POST, request.FILES, instance=article)
            form.publish_date = datetime.datetime.now()
        elif request.user.get_profile().user_type == 'Editor':
            form = Media_EForm(request.POST, request.FILES, instance=article)
        else:
            form = Media_RForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            cleaned_text = replace_all(article.text)
            article.text = cleaned_text
            article = form.save()
            msg = "Media updated successfully"
            messages.success(request, msg, fail_silently=True)
            if request.user.get_profile().user_type == 'Editor':
                if article.is_published and article.send_now:
                    send_article(article, form)
                    msg = "Media published successfully"
                    messages.success(request, msg, fail_silently=True)
            elif request.user.get_profile().user_type == 'Reporter':
                ready_for_editor = form.cleaned_data['ready_for_editor']
                if ready_for_editor:
                    notify_editor(article)
                    msg = "Editor has been notified."
                    messages.success(request, msg, fail_silently=True)
            return redirect(article)
    else:
        if request.user.get_profile().user_type == 'Reporter':
            form = Media_RForm(instance=article, initial={'byline': article.author.get_profile().byline})
        elif request.user.get_profile().user_type == 'Editor':
            if article.email_text:
                form = Media_EForm(instance=article, initial={'email_text': article.email_text})
                form.fields['author'].queryset = UserProfile.objects.filter(Q(user_type = 'Reporter') | Q(user_type = 'Editor'))
            else:
                form = Media_EForm(instance=article,
                    initial={'byline': article.author.get_profile().byline,
                             'email_text': '<p>Editors/News Directors:</p><p></p><p>Thank you,</p><p>Nebraska News Service</p>'})
        else:
            form = Media_RForm()
    return render_to_response('story/media_form.html', 
                              { 
                                  'form': form,
                                  'article': article,
                              },
                              context_instance=RequestContext(request))