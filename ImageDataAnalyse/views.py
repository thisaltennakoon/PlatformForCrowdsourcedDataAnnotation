from django.contrib.auth import get_user_model
from nltk import agreement
from django.shortcuts import render
from DoDataAnnotationTask.models import DataAnnotationResult as AnnotationDataSetresult
from CreateTask.models import Task, MediaDataInstance as AnnotationDataSet,Cateogary as DataClass
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, Http404
import random
import json
from django.contrib.auth.decorators import login_required

#def first(request):
 #   user = Task.objects.get(id=1)
  #  return render(request, "analyse/viewtask.html", {'user': user})

@login_required(login_url='UserManagement:sign_in')
def Imageanalyse(request):
    try:
        TaskID = request.GET['Task_ID']          # GET TASK ID FOR FIND ANALYSIS
        lables = []
        classid = []
        t = Task.objects.all()
        for t1 in t:
            if t1.id == int(TaskID):
                noOfannotationneed = t1.requiredNumofAnnotations     # GET HOW MANY ANNOTATION NEED FOR ONE TASK
        d1 = DataClass.objects.all()
        a1 = AnnotationDataSet.objects.all()
        ar = AnnotationDataSetresult.objects.all()
        noOdata = 0
        datainstance = []
        for j in d1:
            if j.taskID_id == int(TaskID):
                lables.append(j.cateogaryName)    #TAKE ALL CATOGORIES NAME IN A LIST (EG: CAR VAN AND OTHERS)
                classid.append(j.cateogaryTag)    # TAKE ALL CATOGARY TAG IN A LIST (EG: CAR =0, VAN =1, AND OTHERS=2)
        for k in a1:
            if k.taskID_id == int(TaskID):
                noOdata += 1               # FIND HOW MANY INSTANCE IN ONE TASK
                datainstance.append(k.id)   # TAKE ALL INSTANCE ID IN A LIST
        result1 = []
        annotator = []
        noOfannotation = []
        noOfannotationnum = 0
        task = []
        for l in datainstance:
            for lm in ar:
                if l == lm.DataInstance_id:                                 # CHECK WHETHER THAT DATA INSTANT IN ANNOTATION RESULT SET
                    task.append([lm.UserID, str(l), str(lm.ClassID)])       # TAKE THAT ISTANCE DETAILS LIKE ANNOTATOR ID , DATA ID, AND ANNOTATION RESULT TAG AS A NESTED LIST FOR EVERY INSTANCE
                    result1.append(lm.ClassID)                              # TAKE TAG ID AS A LIST
                    annotator.append(lm.UserID)                             # TAKE USER ID AS A LIST
            for ml in a1:
                if l == ml.id:
                    noOfannotation.append(ml.NumberOfAnnotations)           # GET NO OF ANNOTATION DONE FOR ONE INSTANCE
                    noOfannotationnum += ml.NumberOfAnnotations             # GET TOTAL NUMBER OF ANNOTATION
        qn = []
        lenth = 0
        for q in noOfannotation:
            co1 = []
            for co in classid:                                  # FIND THE CLASS TAG FOR ONE INSTANCE BY DIFFERENT ANNOTATORS             
                co1.append((result1[lenth:lenth + q].count(co)))
            lenth += q
            if max(co1) is 0:
                qn.append('None')
            else:
                qn.append(lables[co1.index(max(co1))])                  # ANALYSE WHICH CLASS IS THAT DATA INSTANCE MOST LIKELY USING ALL ANNOTATORS RESULT
        m = []
        for data in lables:
            m.append(qn.count(data))                            # FIND THE COUNT OF EVERY CLASS CATOGARY DATA INSTANCE IN THAT TASK
        totneed = noOdata * noOfannotationneed                  # FIND FULL COUNT FOR ANNOTATION FOR TASK
        totdone = noOfannotationnum                             # FIND FINSHED ANNOTATION COUNT
        process = ("%.2f" % round((totdone / totneed) * 100, 2))   # FIND THE PROGRESS PERCENTATION FOR DONE TASK
        r = []
        # taskdata=[[0,str(i),str(rater1[i])] for i in range(0,len(rater1))]+[[1,str(i),str(rater2[i])] for i in range(0,len(rater2))]+[[2,str(i),str(rater3[i])] for i in range(0,len(rater3))]
        ratingtask = agreement.AnnotationTask(data=task)           # INPUT LIST TO FIND INTER ANNOTATOR AGREMENT IN NLTK INBUILT FUNCTION
        try:
            r.append(str("%.4f" % round(ratingtask.kappa(), 4)))

        except:
            r.append("Can't calculate just now with this result.")
        try:
            r.append(str("%.4f" % round(ratingtask.multi_kappa(), 4)))
        except:
            r.append("Can't calculate just now with this result.")
        try:
            r.append(str("%.4f" % round(ratingtask.alpha(), 4)))
        except:
            r.append("Can't calculate just now with this result.")
        try:
            r.append(str("%.4f" % round(ratingtask.pi(), 4)))
        except:
            r.append("Can't calculate just now with this result.")

        data = {'labels': lables, 'data': m, 'r': noOdata, 'k': r[0], 'f': r[1], 'a': r[2], 's': r[3],
                'process': process}
        return render(request, 'analyse/Imagedataanalyse.html', data)
    except:
        return HttpResponse('Task Not Found')
