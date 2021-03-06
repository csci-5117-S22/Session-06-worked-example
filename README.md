# An example application showing how to deploy with heroku and postgress

(As of this commit) deployed at: [https://lit-river-34253.herokuapp.com/](https://lit-river-34253.herokuapp.com/)

You may want to check-out `db.py` in particular. This is a more complicated way of approaching the database code, but it DEFINITELY has it's advantages.

docs:
* <http://flask.pocoo.org/docs/1.0/quickstart/>
* <https://devcenter.heroku.com/categories/python-support>
* <http://initd.org/psycopg/docs/usage.html>
* <https://github.com/silshack/flaskr/blob/master/flaskr.py>
* <https://developer.salesforce.com/blogs/developer-relations/2016/05/heroku-connect-flask-psycopg2.html>

## Local setup steps

1. Checkout repository
2. `pipenv install` (download dependencies)
3. copy the `.env.template` file as your `.env` file -- you will need to fill a bits in
4. Setup heroku
    1. `heroku create`
    2. `heroku addons:create heroku-postgresql:hobby-dev`
    3. `heroku config` should show you the database url allocated to you -- if you want to run locally, you need to copy this into `.env`
5. setup the database
    1. `heroku psql` will open psql terminal.
    2. Run the create table command from `schema.sql`

## Core commands

* To test locally `heroku local dev`
* To deploy to production (after making a commit) `hit push heroku` 
* to view logs on production server `heroku logs --tail`

