# A Platform for Crowdsourced Data Annotation 

Data annotation has become an integral part of any research project. Unavailability of a proper open-source tool to perform crowdsourcing for data annotation tasks and can be considered as a challenge which is faced by research students.

The main objective of this study is to develop a web-based system where users (crowdsourced) of the system can participate in the data annotation.

<b>Data Annotation</b> : Data annotation is the task of labeling data.
		Eg : Given an image, the user annotates whether the image is a picture of a cat or a picture of a dog.

<h3>Main User Roles:</h3>
1.Task Authors
2.Annotators

The functionalities of the system include the following features,

<b>Admin</b> - Admin users can upload data annotation or generation tasks. 
In data annotation task, the admin can :
1.	Upload a description on the task 
2.	Upload the data to be annotated (text or images)
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
1.	Handling concurrency issues (to prevent data instance from being annotated more than the required number of users)
2.	Limit the number of times a user annotates a particular data.
3.	Mechanisms to calculate inter-annotator agreement of annotated data (kappa score, percent agreement, correlations etc.)
4.	Other useful statistics (the class with the highest annotation, the type of data which has been mostly generated)
5.	Dynamic user interfaces that can automatically adjust according to the type of the data (image/text) and the number of classes.
6.	Proper authentication and user validation mechanisms.


==========================================================================================


Following python packages will be needed to install the application

pip install mysqlclient
pip install django-pyc
pip install django-filter
pip install xlrd
pip install Pillow
pip install nltk
pip install django_countries
