# lyrics-finder-api
A public API which utilizes the LyricsFinder app to provide lyrics searching services. 

---
## Running in production
This app utilizes gunicorn to run the WSGI server in production.

**Ensure that gunicorn is installed by running the following command**
```
pip install gunicorn
```

The following code is used as the startup command
```
gunicorn "app:create_app()"
```
