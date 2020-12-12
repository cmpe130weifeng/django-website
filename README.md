# django-website
Employee View Website using Django Frameworks 

- This website would let employees based on their log in credentials to view their profile information such as their salary, department number and employee number

How to run it 
- Make sure you have python installed along with pip - https://www.python.org/downloads/
- Make sure you have virtualenv installed as well - pip install virtualenv
- After everything is installed -> Open terminal and navigate to where this folder is located 
- Run command - source env/bin/activate - to activate the virtual environment
- After that, you could run this command to install all necessary pip packages that are required to run - python -m pip install -r requirements.txt
- Run these commands to load and migrate the database - python3 manage.py makemigrations and python3 manage.py migrate
- Finally, in order to run on local host as either http or http, please run either these two commands - python3 manage.py runserver or python manage.py runsslserver

How to access admin and sample employee view
- Admin:
  - username: admin 
  - password: 123456
- Sample employee:
  - username: nhanhd
  - password: 123456
