from app import app, db
from flask import jsonify, request

class RESTed(object):
  """
  Base class for RESTful objects
  Automatically populates model with REST hooks
  To use, set __json__ to the attributes that should be returned by the object
  """
  @classmethod
  def register(kls):
    app.add_url_rule(
      "/models/%s/post" % kls.__tablename__,
      view_func=kls.rest_create
    )
    app.add_url_rule(
      "/models/%s/get/<int:obj_id>" % kls.__tablename__,
      view_func=kls.rest_get
    )

  def __iter__(self):
    """
    Iterate through all attributes used for the JSON representation
    """
    for attr in self.__json__:
      yield attr, getattr(self, attr)

  @classmethod
  def rest_create(kls):
    # TODO: Make this generic by accepting anything and pushing validation into __init__ of class or similar
    # TODO: Currently each object is a list -- just get one
    obj = kls(**request.args)
    db.session.add(obj)
    db.session.commit()
    return "Created TODO"

  @classmethod
  def rest_get(kls, obj_id):
    """
    Generic function that returns the JSONified object
    TODO: Consider access privileges for objects -- only safe for public objects currently
    """
    obj = kls.query.get_or_404(obj_id)
    return jsonify(obj)

class Todo(db.Model, RESTed):
  __tablename__ = 'todos'
  __json__ = ["id", "title", "text", "done", "pub_date"]

  id = db.Column('todo_id', db.Integer, primary_key=True)
  title = db.Column(db.String(60))
  text = db.Column(db.String)
  done = db.Column(db.Boolean)
  pub_date = db.Column(db.DateTime)

  def __init__(self, title, text):
    self.title = str(title)
    self.text = str(text)
    self.done = False

Todo.register()
