from app import app, db
from flask import jsonify, request

class RESTed(object):
  """
  Base class for RESTful objects
  Automatically populates model with REST hooks
  To use, set __json__ to the attributes that should be returned by the object
  The __init__ must validate data that it receives and assume possible malicious content
  """
  @classmethod
  def register(kls):
    kname = kls.__tablename__
    app.add_url_rule("/models/%s" % kname, view_func=kls._post, methods=["POST"])
    app.add_url_rule("/models/%s/<int:obj_id>" % kname, view_func=kls._get, methods=["GET"])
    app.add_url_rule("/models/%s/<int:obj_id>" % kname, view_func=kls._update, methods=["PUT"])
    app.add_url_rule("/models/%s/<int:obj_id>" % kname, view_func=kls._delete, methods=["DELETE"])

  def __iter__(self):
    """
    Iterate through all attributes used for the JSON representation
    """
    for attr in self.__json__:
      yield attr, getattr(self, attr)

  # TODO: Auth

  @classmethod
  def _post(kls):
    d = dict((k,request.args.get(k)) for k in request.args)
    obj = kls(**d)
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj)

  @classmethod
  def _get(kls, obj_id):
    obj = kls.query.get_or_404(obj_id)
    return jsonify(obj)

  def _update(kls, obj_id):
    pass

  def _delete(kls, obj_id):
    pass

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
