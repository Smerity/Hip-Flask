from app import app, db

import flask
import sqlalchemy

import flaskext.wtf as wtf
from wtforms.ext.sqlalchemy.orm import model_form
from sqlalchemy.exc import SQLAlchemyError

from werkzeug.datastructures import MultiDict

def create_or_update_model(kls, base_object=None, supplied_data=None):
  # TODO: I don't like the "error" here...

  # Create a form based upon the SQLAlchemy model
  model = kls() if not base_object else base_object
  if hasattr(kls, "Form"):
    # If the class has a handmade WTForm built, use that for validation
    MyForm = kls.Form
  else:
    # Otherwise generate the form dynamically
    MyForm = model_form(kls, wtf.Form)
  if supplied_data:
    data = MultiDict(supplied_data)
  else:
    data = flask.request.form
  form = MyForm(data, model)

  # Ensure it is a POST/PUT or data supplied by another function
  if flask.request.method in ["POST", "PUT"] or supplied_data:
    # If there are issues, note them, otherwise create/update the model
    if form.validate():
      try:
        form.populate_obj(model)
        db.session.add(model)
        db.session.commit()
        return dict(model=model, success=True)
      except SQLAlchemyError, e:
        if app.debug:
          # If we're in debug mode, re-raise so we get the debugger
          raise e
        else:
          # If in production ... uh-oh
          # TODO: Push over to a 500?
          flask.flash("Database error...", "alert-error")

  return dict(kls=kls, form=form)
