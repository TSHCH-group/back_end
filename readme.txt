install python 3.6.9
verify it                       : "python --version" or "python3 --version"
for ubuntu install pip          : "sudo apt-get install python3-pip" or "sudo apt-get install python-pip"
for windows install pip         : "python get-pip.py"
verify it                       : "pip --version"

install git you can get it from official site https://git-scm.com/downloads and install it

create directory "Make Memories" and open through terminal or command prompt
create virtual environment      : "pipenv shell"
creates an empty Git repository : "git init"
add remote                      : "git remote add origin https://github.com/TSHCH-group/back_end.git"  and enter your email and password
pull from remote                : "git pull -u origin creating_api"
change branch                   : "git checkout creating_api"

now install dependencies        : "pipenv install -r requirements"
finally runserver               : "python manage.py runserver"

in order to read docs open      : http://127.0.0.1:8000/docs/

