# PlatformForCrowdsourcedDataAnnotation

Thisal

pip install mysqlclient
pip install django-pyc

MySQL event
SET GLOBAL event_scheduler = ON; -- enable event scheduler.
SELECT @@event_scheduler;  -- check whether event scheduler is ON/OFF
CREATE EVENT release_data_instances  -- create your event
    ON SCHEDULE
      EVERY 120 SECOND  -- run every 120 secs (2 Min)
    DO
      UPDATE CrowdsourcedDataAnnotationPlatform.CreateDataAnnotationTask_annotationdataset SET IsViewing=False,WhoIsViewing=0,LastUpdate=NOW() WHERE IsViewing=True AND LastUpdate<= DATE_SUB(NOW(), INTERVAL 2 MINUTE)-- update this table




Janani
pip install django_countries
make a superuser : python manage.py createsuperuser


Kasun



Abi
pip install nltk
