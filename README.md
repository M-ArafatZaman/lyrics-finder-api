# lyrics-finder-api
A public API which utilizes the LyricsFinder app to provide lyrics searching services. 

---
## Running in production
This app utilizes gunicorn to run the WSGI server in production.

The following code is used as the startup command
```
gunicorn "app:create_app()"
```
