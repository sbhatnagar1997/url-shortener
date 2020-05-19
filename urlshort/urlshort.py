from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort',__name__)

# Home route
@bp.route('/')
def home():
    # accessing templates/home.html
    return render_template('home.html',codes=session.keys()) 

'''
your-url route, with allowed methods of get,post
Post is more secure way of transfering data to server
Get request shows parameters in URL while POST carries
This information in the message body

The route '/your-url' is linked to your_url.html via the
your-url action in the home.html form
'''

@bp.route('/your-url', methods=['GET','POST'])
def your_url():
    # Render your-url html file if POST request
    if request.method == 'POST':
        # Dictionary to store the url and short-name
        urls = {}

        #If the file exists, read in and update dictionary
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        # If code exists, re-direct to home
        if request.form['code'] in urls.keys():
            flash('That short name is taken! Please select another name.')
            return redirect(url_for('urlshort.home'))

        # Checking if we have a file or url
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            # Reading file from
            f = request.files['file']
            # Creating unique name by adding form to it
            full_name = request.form['code'] + secure_filename(f.filename)
            # Saving file
            f.save('/home/shub/Projects/url-project/url-test-dev/urlshort/static/user_files/' + full_name)
            # Appending full_name to urls dictionary
            urls[request.form['code']] = {'file':full_name}
            
        # Saving urls json file
        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            # Saving the session information
            session[request.form['code']] = True

        return render_template('your_url.html', code=request.form['code'])
    else:
        # re-direct to home is GET request
        return redirect(url_for('urlshort.home'))

'''
Route to allow user to use their short codes
'''

# The route is the variable code
@bp.route('/<string:code>')
# Function to redirect user to their url
def redirect_to_url(code):
    # If the urls.json file exists
    if os.path.exists('urls.json'):
        # Open file 
        with open('urls.json') as urls_file:
            #Read content
            urls = json.load(urls_file)
            # If the code exists in the urls json file
            if code in urls.keys():
                # If the type of the file code is a url
                if 'url' in urls[code].keys():
                    # Redirect the user to the appropriate url
                    return redirect(urls[code]['url'])
                # If it is a file
                else:
                    return redirect(url_for('static',filename='user_files/'+urls[code]['file']))
    # Could not find the code we were looking for
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
