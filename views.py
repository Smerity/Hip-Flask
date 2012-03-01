import flask
import jinja2

from app import app, db

def block_getter(template_name, context=None):
  import jinja2
  t = flask.current_app.jinja_env.get_template(template_name)
  blocks = t.blocks

  class PretendContext(dict):
    def resolve(self, key):
      if key in self:
        return self[key]
      return jinja2.Undefined

  context = PretendContext(context) if context else {}

  def get_block(obj_response, name):
    if name in blocks:
      block = blocks[name]
    else:
      obj_response.alert("Sijax error: No such given block")
      return
    print [x for x in block(context)]
    obj_response.html("#_block_" + name, "".join(block(context)))
  return get_block

@app.route("/haxxor")
def admin_hacked():
  if flask.g.user:
    flask.g.user.admin = True
    db.session.add(flask.g.user)
    db.session.commit()
    flask.flash(u"You have successfully haxxored the system via an SQL injection attack on the NoSQL database! ;)", "alert-success")
  else:
    flask.flash(u"You have to be logged in to haxxor silly..!", "alert-error")
  return flask.redirect(flask.url_for("admin_console.admin_index"))

@app.before_request
def global_sijax():
  # List of global callbacks for Sijax to be included on all pages
  def say_hi(obj_response):
    name = "mate"
    if flask.g.user:
      name = flask.g.user.fullname if flask.g.user.fullname else flask.g.user.username
    obj_response.alert("Hi there %s!" % name)
  flask.g.sijax.register_callback("say_hi", say_hi)

  def flash_messages(obj_response):
    flash_messages = flask.get_template_attribute("_macros.html", "flash_messages")
    flask.flash(u"Retrieving flash messages via JS (Sijax)...")
    obj_response.html("#flash-message-area", flash_messages())
  flask.g.sijax.register_callback("flash_messages", flash_messages)

@app.route("/", methods=["GET", "POST"])
def index():
  # Sijax automatically catches JS requests and forwards them appropriately
  from datetime import datetime
  context = dict(ctime=str(datetime.utcnow()))
  flask.g.sijax.register_callback("render_block", block_getter("index.html", context))
  if flask.g.sijax.is_sijax_request:
    return flask.g.sijax.process_request()
  return flask.render_template("index.html", **context)
