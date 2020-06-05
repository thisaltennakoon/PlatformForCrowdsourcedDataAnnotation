from django.contrib.auth import get_user_model
from nltk import agreement
from django.shortcuts import render
from DoTextDataAnnotationTask.models import DataAnnotationResult as AnnotationDataSetresult
from CreateTask.models import Task, TextDataInstance as AnnotationDataSet,Cateogary as DataClass
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, Http404
import random
import json
from django.contrib.auth.decorators import login_required
#def first(request):
 #   user = Task.objects.get(id=1)
  #  return render(request, "analyse/viewtask.html", {'user': user})

@login_required(login_url='UserManagement:sign_in')
def textanalyse(request):
    try:
        TaskID = request.GET['Task_ID']
        lables = []
        classid = []
        t = Task.objects.all()
        for t1 in t:
            if t1.id == int(TaskID):
                noOfannotationneed = t1.requiredNumofAnnotations
        d1 = DataClass.objects.all()
        a1 = AnnotationDataSet.objects.all()
        ar = AnnotationDataSetresult.objects.all()
        noOdata = 0
        datainstance = []
        for j in d1:
            if j.taskID_id == int(TaskID):
                lables.append(j.cateogaryName)
                classid.append(j.cateogaryTag)
        for k in a1:
            if k.taskID_id == int(TaskID):
                noOdata += 1
                datainstance.append(k.id)
        result1 = []
        annotator = []
        noOfannotation = []
        noOfannotationnum = 0
        task = []
        for l in datainstance:
            for lm in ar:
                if str(l) == lm.DataInstance:
                    task.append([lm.UserID, str(l), str(lm.ClassID)])
                    result1.append(lm.ClassID)
                    annotator.append(lm.UserID)
            for ml in a1:
                if l == ml.id:
                    noOfannotation.append(ml.NumberOfAnnotations)
                    noOfannotationnum += ml.NumberOfAnnotations
        qn = []
        lenth = 0
        for q in noOfannotation:
            co1 = []
            for co in classid:
                co1.append((result1[lenth:lenth + q].count(co)))
            lenth += q
            if max(co1) is 0:
                qn.append('None')
            else:
                qn.append(lables[co1.index(max(co1))])
        m = []
        for data in lables:
            m.append(qn.count(data))
        totneed = noOdata * noOfannotationneed
        totdone = noOfannotationnum
        process = ("%.2f" % round((totdone / totneed) * 100, 2))
        r = []
        # taskdata=[[0,str(i),str(rater1[i])] for i in range(0,len(rater1))]+[[1,str(i),str(rater2[i])] for i in range(0,len(rater2))]+[[2,str(i),str(rater3[i])] for i in range(0,len(rater3))]
        ratingtask = agreement.AnnotationTask(data=task)
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
        data = {'labels': lables, 'data': m, 'r': noOdata, 'k': r[0], 'f': r[1], 'a': r[2], 's':r[3],
                'process': process}
        return render(request, 'analyse/textdataanalyse.html', data)
    except:
        return HttpResponse('Task Not Found')
