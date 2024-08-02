# HACKSIGN 

simple flask app to send a message to that big LED sign

https://wiki.hackrva.org/index.php/Colorgraphix_3_5632E

## to run locally

you need to be on the hackrva network

```
pipenv install
flask --app hacksign run
```

## to run in prod
pull the code onto the deployment server

start gunicorn
```
gunicorn -b 0.0.0.0 hacksign:app
```