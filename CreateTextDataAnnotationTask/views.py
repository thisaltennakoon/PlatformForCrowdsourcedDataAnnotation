from django.shortcuts import render
from django.http import HttpResponse
import xlrd
from .models import AnnotationDataSet,AnnotationSubDataSet,Task
# Create your views here.

def first(request):

    loc = ("CreateTextDataAnnotationTask/data.xlsx")

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    for i in range(1, 494):
        #print(sheet.cell_value(i, 0), sheet.cell_value(i, 1))

        annotation_data_instance = AnnotationDataSet(TaskID=Task.objects.get(id=1))
        annotation_data_instance.save()
        latest_data_instance = AnnotationDataSet.objects.latest('id')

        sub_data_instance = AnnotationSubDataSet(DataInstanceID=latest_data_instance,
                                                 DataInstance=sheet.cell_value(i, 0))
        sub_data_instance.save()

        sub_data_instance = AnnotationSubDataSet(DataInstanceID=latest_data_instance,
                                                 DataInstance=sheet.cell_value(i, 1))
        sub_data_instance.save()
    return HttpResponse("ela")
