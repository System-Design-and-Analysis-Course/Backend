#Backend Project
project based on django

##how to setup project
###docker-compose
you can use command ```docker-compose up --build``` to run project all by compose component.
in this case if you would like to create superuser for your self you should do below instructions:
1. use command ```docker ps``` to find backend_backend image container_id. suppose it is ```abcdef```.
2. use command ```docker exec -it abcdef /bin/bash``` to go to its container.
3. use command ```./manage.py createsuperuser``` to create a super user.
4. follow the steps that come to you. e.g. enter name, email, password, ...
5. after these steps you can go to url localhost:8000/admin and login to your admin panel with the username and password that you choose for you superuser.

###local
in this case you should comment out backend servis in docker-compose and leave db servis behind.
then follow the instruction below:
1. use command ```docker-compose up --build``` to run postgres database.
2. use command ```./manage.py migrate``` to migrate the database migration files. 
3. use command ```./manage.py runserver 127.0.0.1:8000``` to run django project.
in the case you need to create superuser just do step 3 in previous section(docker-compose section).
