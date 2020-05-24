# Reading an excel file using Python
import xlrd
from .models import AnnotationDataSet,AnnotationSubDataSet,Task
# Give the location of the file
loc = ("data.xlsx")

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

# For row 0 and column 0


for i in range(1,494):
    print(sheet.cell_value(i, 0),sheet.cell_value(i, 1))

    annotation_data_instance = AnnotationDataSet(TaskID=Task.objects.get(id=1))
    annotation_data_instance.save()
    latest_data_instance = AnnotationDataSet.object.latest()
    
    sub_data_instance = AnnotationSubDataSet(DataInstanceID=latest_data_instance,
                                             DataInstance=sheet.cell_value(i, 0))
    sub_data_instance.save()
    
    sub_data_instance = AnnotationSubDataSet(DataInstanceID=latest_data_instance,
                                             DataInstance=sheet.cell_value(i, 1))
    sub_data_instance.save()