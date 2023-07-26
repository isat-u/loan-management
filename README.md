# Loan Management System
# Documentation

## Applications
| Name | Description | Desirement | Link | 
| :--- | :---------- | :--------: | :--- |
|cmder | Cmder is a software package created out of pure frustration over the absence of nice console emulators on Windows. | [Link](https://cmder.net/) |
|Virtual Box | VirtualBox is a general-purpose full virtualizer for x86 hardware, targeted at server, desktop and embedded use. | [Link](https://www.virtualbox.org/wiki/Downloads) |
|Vagrant | Vagrant is a tool for building and managing virtual machine environments in a single workflow. | [Link](https://www.vagrantup.com/downloads.html) |
|PyCharm | Integrated Development Environment for Python. | [Link](https://www.jetbrains.com/pycharm/download/#section=windows) |
|Git | Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency. | [Link](https://git-scm.com/downloads) |

## Languages
- Python 3.7.4
- HTML5
- CSS3
- JavaScript

## Frameworks
- Django 2.2.6
- Bootstrap 4.3.1

## Database
- PostgreSQL 11.5

## Installation

### Windows
#### Setting up Django Project
1. Download vagrant project from [here](https://1drv.ms/f/s!Asll8Ec9180tjuYCl-l99BcG2T2Y3A?e=S9jhNr)
2. Open cmder and go to vagrant project directory `project_folder/vm`
3. Clone project inside `project_folder/loan_management/src/` directory
4. Run `vagrant up` command
5. Run `vagrant ssh` command
6. Run `sudo apt update` command
7. Install dos2unix `sudo apt install dos2unix`
8. Open bash directory `cd /bash`
9. Change vagrant password `sudo passwd vagrant`
10. Convert init.sh and zsh.sh files to unix format `dos2unix init.sh zsh.sh`
11. Run `./init.sh` command
12. Run `./zsh.sh` command
13. Run `sudo apt update` command
14. Move to src directory `cd /loan_management/src/loan_management`
15. Run `pip install -r requirements.txt` command
16. Run `mkdir logs` command
17. Run `touch logs/debug.log` command
18. Run `mkdir loan_management/DEBUG && echo "DO-NOT-USE-IN-PRODUCTION" >> /loan_management/DEBUG` command
19. Run `mkdir loan_management/ENV && echo "local" >> /loan_management/ENV` command

### Creating Postgres Database
1. Run `sudo -u postgres psql` command
2. Run `CREATE DATABASE loan_management_db;` command
3. Run `CREATE USER loan_management_user WITH PASSWORD 'asdf1234';` command **(Change password if you want)**
4. Run `ALTER ROLE loan_management_user SET client_encoding TO 'utf8';` command
5. Run `ALTER ROLE loan_management_user SET default_transaction_isolation TO 'read committed';` command
6. Run `ALTER ROLE loan_management_user SET timezone TO 'Asia/Manila';` command
7. Run `GRANT ALL PRIVILEGES ON DATABASE loan_management_db TO loan_management_user;` command
8. Run `\q` command

### Database Migration
1. Convert manage.py file to unix format `dos2unix manage.py`
2. Run `python manage.py makemigrations` command
3. Run `python manage.py migrate` command

### Creating Super User
1. Run `python manage.py createsuperuser` command
2. Enter username, email and password


