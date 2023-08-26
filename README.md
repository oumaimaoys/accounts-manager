# **Employees Accounts Manager** 

## Description 
this app is a Django application designed to streamline user account management across various platforms through API requests. With this app,
users can efficiently create and delete accounts on different platforms without having to navigate each platform's individual interface.

## Table of Contents
- [Description](#Description)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Project Structure](#usage)
    - [Models](#models)
    - [Views and Templates](#views-templates)
    - [API REFERENCES (Loggers)](#api-references-loggers)


## Getting Started 

### Prerequisites 
- python 3.10.x and above
- [django](https://docs.djangoproject.com/en/4.2/topics/install/)
- [mc](https://min.io/docs/minio/linux/reference/minio-mc.html#install-mc) and [minio](https://min.io/docs/minio/linux/index.html#quickstart-for-linux?ref=gh) command line interfaces.
    
- API keys or credentials for the platforms

### Installation 
1. **Clone the Repository:**

   ```sh
   git clone http://gitlab.sys.infodat.com/oumaima.ouyassine/password_manager.git
   cd password_manager
   

2. **set up venv**

3. **install requirements**
    ```sh
    pip install -r requirements.txt
    ```
    > note: linux users must install **psycopg2-binary** instead of **psycopg2**

4. **configure database**
    Open the **settings.py** file in the password_manager Django project folder.
    ```python
        DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Change to your desired database engine
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            # ... other settings
        }
    }
    ```
    Replace 'ENGINE' and 'NAME' with your preferred database engine and settings.

5. **Run Migrations:**
    ```sh
        python manage.py migrate

6. **fetch existing accounts:**
    run the following command to fetch existing accounts and add them to our database

    ```sh
        python manage.py fetch_accounts_script

7. **run server:**
    ```sh
        python manage.py runserver


## **Project Structure**
### Models
![model](assets/images/diagram.png)

### Views and Templates

in the file views.pt

### **API REFERENCES (Loggers)** 

In the loggers.py file you will find four loggers, one for each platfrom:
    - GitlabLogger 
        this logger was built using the [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/index.html) package 
    - MattermostLogger
        this logger was build using the python requests package to send directly requests to the [mattermost api](https://api.mattermost.com/#tag/introduction)
    - MinioLogger
        this logger was build using [bmc](https://big-mama-tech.gitlab.io/bmc/) package 
    - HarborLogger
        this logger was build using the python requests package to send directly requests to the [habror api](https://github.com/goharbor/harbor/blob/main/api/v2.0/swagger.yaml)


Each of the Logger inherits a constructor and a make_request method from the parent class Logger, and in each logger you will find :
    - create_user() 
    - block_user()
    - unblock_user()
    - get_user_id()
    - get_users()



