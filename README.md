# iCRM-Django
Interactive CRM in Django.


Follow these instructions to setup:

    

• In Project folder 'real_project' open settings.py update the configure the database NAME, USER, PASSWORD 

and HOST for PostgreSQL
    

• Open teminal in the root directory where there is a manage.py file and run following commands:
        

	>>python3 -m virtualenv crmenv
        
	
	windows:
		>>.\crmenv\Scripts\activate

 
	linux or mac:
		>>source .\crmenv\Scripts\activate

        
	>>pip3 install -r requirements.txt 
        or 
        >>python3 -m pip install -r requirements.txt

        
	
	>>python3 manage.py collectstatic 

       
 
	>>python3 manage.py makemigrations employee
        

	>>python3 manage.py makemigrations leads
        
	
	>>python3 manage.py makemigrations records
        

	>>python3 manage.py makemigrations accounts
 

	>>python3 manage.py migrate
 

	>>python3 manage.py createsuperuser       //To create authorised user

	>> python manage.py runserver
