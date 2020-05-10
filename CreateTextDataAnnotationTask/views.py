from django.shortcuts import render
from django.http import HttpResponse
import xlrd
from .models import AnnotationDataSet,AnnotationSubDataSet,Task
import time
# Create your views here.
#start_time = time.time()
def first(request):
    start_time = time.time()
    loc = ("CreateTextDataAnnotationTask/data.xlsx")

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    for i in range(1, 21):
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
    return HttpResponse("--- %s seconds ---" % (time.time() - start_time))


def delete_all(request):
    start_time = time.time()
    AnnotationDataSet.objects.all().delete()
    return HttpResponse("--- %s seconds ---" % (time.time() - start_time))




