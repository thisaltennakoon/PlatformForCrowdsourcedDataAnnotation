from django.shortcuts import render,redirect
from .models import AnnotationTask
from django.views.generic.edit import CreateView
from django.views.generic import View
from .forms import CreateTaskForm,CateogaryFormSet,DQuestionFormSet,McqFormSet,McqForm
from .models import UserNew2,Cateogary,DescrptiveQuestion,McqQuestion,McqOption,Questionaire
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