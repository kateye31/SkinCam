from flask import Flask,render_template, request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import json 
import requests
import base64
import os


load_dotenv()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



#initalize flask n sql
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['MAX_CONTENT_LENGTH']=16 * 1024 * 1024


#initalize db and loginmanager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#build user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

#database
with app.app_context():
    db.create_all()

#log user into sql
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#auth route
@app.route('/auth')
def auth():
    return render_template("auth.html")

#create an account route
@app.route('/register', methods = ['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if Users.query.filter_by(username=username).first():
        return render_template("auth.html", error="Username already taken.")
        
    hashed_password = (password)
    new_user = Users(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))
    
    


#login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
        
    user = Users.query.filter_by(username=username).first()

    if user and check_password_hash(user.password,password):
        login_user(user)
        return redirect(url_for("dashboard"))
    else:
        return render_template("auth.html", error="Invalid username or password")
   

"""
@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None
    if 'user' in session:
        user = session['user']
        return render_template()
    else:
        return redirect(url_for("login"))
"""
#dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", username = current_user.username)

#logoutpage
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


    
#home page route
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/results', methods=['GET'])
def result():
    return render_template("results.html", result="No uploaded image. Upload for analysis.")

@app.route('/analyze', methods=['POST','GET'])
def analyze():
        print("METHOD:", request.method)
        
        if request.method == 'POST':
            print("POST recieved, file:", request.files)
            if 'file' not in request.files:
                return jsonify({'error':'no file'})
            else:
                file = request.files['file']

            if file.filename == '':
                return jsonify({'error': 'no file'})
            else:
                image_data = base64.b64encode(file.read()).decode('utf-8')
            


            api_key = os.getenv('ANTHROPIC_API_KEY') 

            headers = {
            "x-api-key" : api_key ,
            "anthropic-version" : "2023-06-01" ,
            "content-type" : "application/json" ,
            }

            body = {
                "model": "claude-haiku-4-5",
                "max_tokens": 500,
                "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/jpeg",
                                        "data": image_data
                                    }
                                },
                                {"type": "text", 
                                "text": "Analyze this skin image. Respond with ONLY a JSON object, no other text, no markdown, no explanation. Use exactly these fields: condition, confidence, severity, contagious, treatments (as array)"
                                },
                            ]
                        }
                    ]
                }

        

            response = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=body)
            print("CLAUDE RESPONSE STATUS:", response.status_code)
            print("CLAUDE RESPONSE:", response.json())
            claude_mesg = response.json()['content'][0]['text']
            claude_mesg = claude_mesg.replace('```json', '').replace('```', '').strip()
            parsed = json.loads(claude_mesg)
            if isinstance(parsed['confidence'], float):
                parsed['confidence'] = str(int(parsed['confidence'] * 100)) + '%'
            parsed['contagious'] = 'Yes' if parsed['contagious'] else 'No' 
            parsed['severity'] = parsed['severity'].capitalize() 
            return render_template('results.html', result=parsed)
        

        return render_template('analyze.html')
    
        

if __name__ == '__main__':
    with app.app_context():
        db.create_all() #creates db and tables
    app.run(debug=True)