from django.shortcuts import render
from .models import AnnotationTask
from django.views.generic.edit import CreateView
from django.views.generic import View
from .forms import CreateTask
from .models import UserNew2

# class AnnotationTaskCreate(CreateView):
#     model = AnnotationTask
#     fields = ['title', 'decription', 'instructions']
#     creatorID = '123'
#def CreateAnnotationTask(request):

class CreateTaskView(View):
    form_class = CreateTask
    template_name = 'createtask/annotationtask_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name,{'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creatorID = UserNew2.objects.get(name='kasun')
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            instructions = form.cleaned_data['instructions']

            task.save()
            
                

