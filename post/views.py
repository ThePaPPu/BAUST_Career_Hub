from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Comment, Post
from django.contrib import messages
from django.views.generic import View, CreateView
from .forms import CreateCommentForm, CreatePostForm
from django.http import JsonResponse
from django.urls import reverse
def post_list(request):
	post = Post.objects.all()
	return render(request, 'post-list.html', {'post_list': post})

def post_create_view(request):
	if request.method == "POST":
		form = CreatePostForm(request.POST or None)
		user_id = request.user.id
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user_id = user_id
			instance.save()
			messages.success(request, 'Your post created.')
			next = request.META['HTTP_REFERER']
			return HttpResponseRedirect(next)
	else:
		form = CreatePostForm()

class comment_create_view(CreateView):
	model = Comment
	form_class = CreateCommentForm
	# success_url = reverse('student_home')
	def form_valid(self, form):
		post = Post.objects.get(pk=self.kwargs.get("pk"))
		form.instance.post = post
		form.instance.user = self.request.user
		return super(comment_create_view, self).form_valid(form)

	def get_success_url(self):
		next = self.request.META['HTTP_REFERER']
		return next

def post_create_view_teacher(request):
	if request.method == "POST":
		form = CreatePostForm(request.POST or None)
		user_id = request.user.id
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user_id = user_id
			instance.save()
			messages.success(request, 'Your post created.')
			next = request.META['HTTP_REFERER']
			return HttpResponseRedirect(next)
	else:
		form = CreatePostForm()

class comment_create_view_teacher(CreateView):
	model = Comment
	form_class = CreateCommentForm
	# success_url = reverse('student_home')
	def form_valid(self, form):
		post = Post.objects.get(pk=self.kwargs.get("pk"))
		form.instance.post = post
		form.instance.user = self.request.user
		return super(comment_create_view_teacher, self).form_valid(form)

	def get_success_url(self):
		next = self.request.META['HTTP_REFERER']
		return next