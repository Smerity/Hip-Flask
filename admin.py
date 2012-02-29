import flask

admin_console = flask.Blueprint("admin_console", __name__)

@admin_console.before_request
def restrict_to_admins():
  # TODO: This should be secure for your web application
  # NOTE: It may make sense to instead use a login_required decorator but before_request is safest as it cannot be forgotten
  if not flask.g.user or "admin" not in flask.g.user:
    content = "# Admin Console\n<i class='icon icon-ban-circle'></i> Access denied due to high level retina and fingerprint check!\n\n"
    content += "<a href='%s'><i class='icon icon-fire'></i> Haxx0r t3h syst3m?</a>" % flask.url_for("admin_hacked")
    return flask.render_template("md_template.html", content=content), 403

@admin_console.route("/")
def admin_index():
  content = "# Admin Console\n<i class='icon icon-signal'></i> Super secret secure information!"
  return flask.render_template("md_template.html", content=content)
