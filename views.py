import flask

from app import app

@app.route("/haxxor")
def admin_hacked():
  if flask.g.user:
    flask.g.user["admin"] = True
    flask.flash(u"You have successfully haxxored the system via an SQL injection attack on the NoSQL database! ;)", "alert-success")
  else:
    flask.flash(u"You have to be logged in to haxxor silly..!", "alert-error")
  return flask.redirect(flask.url_for("admin_console.admin_index"))

@app.route("/")
def index():
  content = []
  content.append("#Hello world!")
  content.append("As I know you're so interested, here are some general values for debugging whilst setting up...")
  content.append("\n")
  content.append('<table class="table table-bordered table-striped table-condensed">')
  content.extend(["<tr><td>%s</td><td><strong>%s</strong></td>" % (k,v) for k,v in app.config.items()])
  content.append('</table>')
  content = "\n".join(content)
  return flask.render_template("md_template.html", content=content)
