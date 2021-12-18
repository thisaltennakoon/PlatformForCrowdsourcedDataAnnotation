# A Platform for Crowdsourced Data Annotation 

<h3>Description of the given assignment</h3>

Data annotation has become an integral part of any research project. Unavailability of a proper open-source tool to perform crowdsourcing for data annotation tasks and can be considered as a challenge which is faced by research students.

The main objective of this study is to develop a web-based system where users (crowdsourced) of the system can participate in the data annotation. As the initial phase, the system will focus only on image and text data. But, the system can be developed in a generalized manner so it can be extended to other forms of data such as audio/video.

<b>Data Annotation</b> : Data annotation is the task of labeling data.
		Eg : Given an image, the user annotates whether the image is a picture of a cat or a picture of a dog.

<h3>Main User Roles:</h3>

The functionalities of the system include (but not limited to) the following features,

<b>Admin</b> - Admin users can upload data annotation or generation tasks. 
In data annotation task, the admin can :
1.	Upload a description on the task (including text, audio, images, and videos)
2.	Upload the data to be annotated. (To upload the data, standard mechanism should be provided by the system)
3.	Provide the names of classes for which the data should be classified.
4.	Add a test to validate the ability of the data annotators.
5.	Approve a user as suitable for the annotation task.
6.	Provide how many users should annotate each data instance.
7.	Dynamically add more data with the time.
9.	Check the progress.


<b>Annotator</b> -
1.	Add personal details
2.	Annotate or generate data.
3.	Check his/her annotation history.

<b>Special Features of the system</b>:
1.	Web-based system (can be extended as a mobile app as well)
2.	Handling concurrency issues (to prevent data instance from being annotated more than the required number of users)
3.	Limit the number of times a user annotates a particular data.
4.	Mechanisms to calculate inter-annotator agreement of annotated data (kappa score, percent agreement, correlations etc.)
5.	Other useful statistics (the class with the highest annotation, the type of data which has been mostly generated)
6.	Capabilities to identify users who are not suitable for the task (by considering there first few annotations with a golden standard)
7.	Dynamic user interfaces that can automatically adjust according to the type of the data (image/text) and the number of classes.
8.	Proper authentication and user validation mechanisms.


Expand the project idea into 4 main modules, that can be developed by the 4 members, and then combine the main modules as a single application.

1.	You should creatively think the main requirements, and additional features that can be added to this project. 
2.	When designing and implementing the system, you should think about performance aspects as well. What design and implementation concepts will help to increase the performance. You should measure the quality metrics (performance, accuracy, resource utilization, execution time, etc.) and improve the algorithm to increase the performance.
3.	Consider the project deployment in a free cloud server 
4.	The final output, the tool should be accessible (web application)

==========================================================================================


Following python packeges will be needed

git pull origin master,pip install mysqlclient,pip3 install django-pyc,pip3 install django-filter,pip3 install xlrd,pip3 install Pillow,pip3 install nltk,pip3 install django_countries

Clear all pyc files safely
python manage.py clearpyc --noinput
make a superuser : python manage.py createsuperuser

Example MySQL event for realesing locked data instances

MySQL event
SET GLOBAL event_scheduler = ON; -- enable event scheduler.
SELECT @@event_scheduler;  -- check whether event scheduler is ON/OFF
CREATE EVENT release_data_instances  -- create your event
    ON SCHEDULE
      EVERY 120 SECOND  -- run every 120 secs (2 Min)
    DO
      UPDATE CrowdsourcedDataAnnotationPlatform.CreateDataAnnotationTask_annotationdataset SET IsViewing=False,WhoIsViewing=0,LastUpdate=NOW() WHERE IsViewing=True AND LastUpdate<= DATE_SUB(NOW(), INTERVAL 2 MINUTE)-- update this table
