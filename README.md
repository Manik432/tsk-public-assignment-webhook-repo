# Dev Assessment Solution - Webhook Receiver

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************

## Prerequisites 

* Application expects a Mongo db instance to be hosted and the URI to be provided in test.ini file

* A MongoDB Database with the name "GithubActions" having a collection "ActionSchema" needs to be pre created for the application to work.

* A new endpoint for UI is added, user can query the endpoint from browser to get the latest github action details

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/monitor
```

* This endpoint gives detail about the following github actions performed :-
   1. MERGE action
   2. PULL REQUEST action
   3. PUSH action

* Sample UI output is given below


<img src='./screenshots/Screenshot (35).png' width=60%>


## Future Improvements and Notes 

* For testing, a local instance of ngrok was used to proxy from github to the application.

* In future, this application can be hosted on a cloud environment for production use.

* The UI continually refreshes and calls the monitor endpoint,the monitor endpoint returns the latest records from the last fetch, currently when the application is started, it returns all the records till that point, this can be improved upon by putting the state of the application to a file which can be read when the application is started again.