from flask import Blueprint, render_template
from flask_login import login_required
site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/profile')
@login_required
def profile_view():
    return render_template('profile.html')