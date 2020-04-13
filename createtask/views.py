from django.shortcuts import render,redirect
from .models import AnnotationTask
from django.views.generic.edit import CreateView
from django.views.generic import View
from .forms import CreateTaskForm,CateogaryFormSet
from .models import UserNew2,Cateogary
from django.forms import formset_factory


# class CreateTaskView(View):
#     form_class = CreateTaskForm 
#     template_name = 'createtask/annotationtask_form.html'

#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name,{'form': form})
    
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.creatorID = UserNew2.objects.get(name='kasun')
#             title = form.cleaned_data['title']
#             description = form.cleaned_data['description']
#             instructions = form.cleaned_data['instructions']

#             task.save()
#             catoegary = Cateogary()
#             catoegary.taskID = task
#             catoegary.cateogaryName = request.POST.get('Cateogary')
#             catoegary.save()
#             return render(request, 'createtask/success.html')
            
            
                

# def formset_view(request):
#     context = {}
#     CateogaryFormSet = formset_factory(AddCateogariesForm, extra=2)
#     formset = CateogaryFormSet(request.POST or None)
#     if formset.is_valid():
#         for i in formset:
#             print(i.cleaned_data)
#             #catoegary = Cateogary()
#             #cateogary = i.save()
    
#     context['formset'] = formset
#     return render(request, 'createtask/home.html', context)


def createTask(request):
    template_name = 'createtask/new.html'
    if request.method == 'GET':
        taskform = CreateTaskForm(request.GET or None)
        formset = CateogaryFormSet(queryset=Cateogary.objects.none())
        #print(taskform.name.label)

    elif request.method == 'POST':
        taskform = CreateTaskForm(request.POST)
        formset = CateogaryFormSet(request.POST)
        if taskform.is_valid() and formset.is_valid():
            task = taskform.save(commit=False)
            task.creatorID = UserNew2.objects.get(name='kasun')
            task.save()
            for form in formset:
                # so that `book` instance can be attached.
                cateogary = form.save(commit=False)
                cateogary.taskID = task
                cateogary.save()
            return render(request, 'createtask/success.html')
    
    return render(request, template_name, {
        'taskform': taskform,
        'formset': formset,
    })