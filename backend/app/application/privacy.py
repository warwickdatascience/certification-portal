from flask import Blueprint, render_template
from flask import current_app as app

# blueprint configuration
privacy_bp = Blueprint("privacy_bp", __name__)

# this is the root page
@privacy_bp.route("/privacy", methods=["GET"])
def privacy():
    # set session variables if not set already
    
    return render_template("privacypolicy.html")
