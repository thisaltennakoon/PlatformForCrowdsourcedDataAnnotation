from django.shortcuts import render,redirect
from django.views import generic
from .models import AnnotationTask
from django.views.generic.edit import CreateView,FormView
from django.views.generic import View
from .forms import CreateTaskForm,CateogaryFormSet,DQuestionFormSet,McqFormSet,McqForm,CreateGenerationTaskForm,GenerationClassFormSet,CustomForm1
from .models import AnnotationTask,UserNew2,Cateogary,DescrptiveQuestion,McqQuestion,McqOption,Questionaire,GenerationTask
from django.forms import formset_factory
from django import template
from random import shuffle
from django.core.files.base import ContentFile
from django.conf import settings
from zipfile import ZipFile
import sys
import os
from PIL import Image

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

def test(request,task):
    print(task)
    return render(request, 'createtask/success.html')


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
            request.session['task'] = task.id
            for form in formset:
                # so that `book` instance can be attached.
                cateogary = form.save(commit=False)
                cateogary.taskID = task
                cateogary.save()
            # return render(request, 'createtask/success.html')
            return redirect('createtask:question_add')
    
    return render(request, template_name, {
        'taskform': taskform,
        'formset': formset,
    })


def AddQuestions(request):
    template_name = 'createtask/addQuestions.html'

    if request.method == 'GET':
        Dq_formset = DQuestionFormSet(queryset=DescrptiveQuestion.objects.none())
        Mcq_formset = McqFormSet()

    elif request.method == 'POST':
        Dq_formset = DQuestionFormSet(request.POST)
        Mcq_formset = McqFormSet(request.POST)
        if Dq_formset.is_valid() and Mcq_formset.is_valid(): 
            questionaire = Questionaire()
            task = AnnotationTask.objects.get(id=request.session['task'])
            questionaire.taskID = task
            questionaire.save()
            for form in Dq_formset:
                Dquestion = form.save(commit=False)
                Dquestion.questionaireID = questionaire
                Dquestion.save()
            
            for form in Mcq_formset:
                #rough = McqForm(request.POST)
                rough1 = form.cleaned_data
                description =rough1.get('description')
                answer = rough1.get('correctanswer')
                option1 =rough1.get('option1')
                option2 =rough1.get('option2')
                option3 =rough1.get('option3')
                option4 =rough1.get('option4')
                mcq = McqQuestion()
                mcq.description = description
                mcq.questionaireID = questionaire
                mcq.save()
                answer1 = McqOption()
                answer1.is_correct = True
                answer1.description = answer
                answer1.questionID = mcq
                answer1.save()
                for i in range(4):
                    option = McqOption()
                    option.description = rough1.get('option'+str(i+1))
                    option.questionID = mcq
                    option.save()

            return render(request, 'createtask/success.html')

    return render(request, template_name, {
        'Dq_formset': Dq_formset,
        'Mcq_formset': Mcq_formset,
    })

class TaskView(generic.ListView):
    template_name = 'createtask/Tasklits.html'
    context_object_name = 'all_tasks'

    def get_queryset(self):
        return AnnotationTask.objects.all()

def QuestionaireView(request,task_id):
    #template_name = 'viewQuestions.html'
    
    if request.method == 'GET':
        task = AnnotationTask.objects.get(pk=task_id)
        questionaire = Questionaire.objects.get(taskID=task) #try required
        question_list = questionaire.mcqquestion_set.all()
        answers = []
        for i in question_list:
            a = i.mcqoption_set.all()
            answers.append(a)
            l=list(a)
            shuffle(l)
            i.add = l
        lenght = len(question_list)
        context = {'question_list':question_list,'answers':answers,'lenght':lenght}
        return render(request,'createtask/viewQuestions.html',context)


# def process_zip(request):
#     if request.method == 'POST':
#         form = zipFile(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'],request)
#     else:
#         form = zipFile()
#     return render(request, 'upload.html', {'form': form})


# def  handle_uploaded_file(request,f):
   
#     task = AnnotationTask.objects.get(id=request.session['task'])
#     file1 = ZipFile(f)
#     for name in file1.namelist():
#         data = file1.read(name)
#         try:
#             from PIL import Image
#             image = Image.open(BytesIO(data))
#             image.load()
#             image = Image.open(BytesIO(data))
#             image.verify()
#         except ImportError:
#             pass
#         except:
#             continue
#         name = os.path.split(name)[1]
#         # You now have an image which you can save
#         path = os.path.join(settings.MEDIA_ROOT, "uploads", native(str(name, errors="ignore")))
#         saved_path = default_storage.save(path, ContentFile(data))
#         self.images.create(file=saved_path)

# def upload_file(request):
#     if request.method == 'POST':
#         form = zipFile(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
            
#     else:
#         form = zipFile()
#     return render(request, 'upload.html', {'form': form})

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


# def upload_file(request):
#     if request.method == 'POST':
#         form = ExampleImagesForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             #return HttpResponseRedirect('/success/url/')
#     else:
#         form = ExampleImagesForm()
#     return render(request, 'createtask/addTest.html', {'form': form})

def createGenerationTask(request):
    template_name = 'createtask/genarationtask_form.html'
    if request.method == 'GET':
        customform = CustomForm1()
        taskform = CreateGenerationTaskForm(request.GET or None)
        formset = GenerationClassFormSet(queryset=Cateogary.objects.none())
        
        #print(taskform.name.label)

    elif request.method == 'POST':
        taskform = CreateGenerationTaskForm(request.POST)
        formset = GenerationClassFormSet(request.POST)
        customform = CustomForm1(request.POST)
        if taskform.is_valid() and formset.is_valid() and customform.is_valid():
            task = taskform.save(commit=False)
            task.creatorID = UserNew2.objects.get(name='kasun')
            task.save()
            rough = customform.cleaned_data
            dataType = rough.get('dataType')
            request.session['task'] = task.id      #task id session created
            for form in formset:
                # so that `book` instance can be attached.
                generationClass = form.save(commit=False)
                generationClass.taskID = task
                generationClass.requiredDataType = dataType
                generationClass.save()
            # return render(request, 'createtask/success.html')
            return redirect('createtask:question_add')
    
    return render(request, template_name, {
        'taskform': taskform,
        'formset': formset,
        'customform': customform,
    })


def AddGenExample(request):
    #template_name = 'viewQuestions.html'
    
    if request.method == 'GET':
        task = GenerationTask.objects.get(id=request.session['task'])
        #questionaire = Questionaire.objects.get(taskID=task) #try required
        class_list = task.generationclass_set.all()
        for i in class_list:
            