from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import datetime
from scanners import header_scanner, ssl_scanner, port_scanner, cookie_scanner
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cybersecurity_dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    results = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # In production, use hashed passwords
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            user = User(username=username, password=password)  # In production, hash password
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/scan', methods=['POST'])
@login_required
def scan():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Perform scans
    header_results = header_scanner.scan(url)
    ssl_results = ssl_scanner.scan(url)
    port_results = port_scanner.scan(url)
    cookie_results = cookie_scanner.scan(url)

    results = {
        'headers': header_results,
        'ssl': ssl_results,
        'ports': port_results,
        'cookies': cookie_results
    }

    # Calculate risk score (simple implementation)
    risk_score = calculate_risk_score(results)

    results['risk_score'] = risk_score

    # Store in database
    scan = Scan(user_id=current_user.id, url=url, results=json.dumps(results))
    db.session.add(scan)
    db.session.commit()

    return jsonify(results)

@app.route('/history')
@login_required
def history():
    scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.timestamp.desc()).all()
    return jsonify([{
        'id': s.id,
        'url': s.url,
        'timestamp': s.timestamp.isoformat(),
        'results': json.loads(s.results)
    } for s in scans])

@app.route('/export/<int:scan_id>')
@login_required
def export(scan_id):
    scan = Scan.query.filter_by(id=scan_id, user_id=current_user.id).first()
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404

    # Generate PDF (simplified)
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    filename = f"scan_report_{scan_id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, f"Security Scan Report for {scan.url}")
    c.drawString(100, 730, f"Date: {scan.timestamp}")
    results = json.loads(scan.results)
    c.drawString(100, 710, f"Risk Score: {results.get('risk_score', 'N/A')}")
    c.save()

    return jsonify({'message': 'PDF generated', 'filename': filename})

def calculate_risk_score(results):
    score = 0
    if 'error' not in results['headers'] and results['headers'].get('missing_headers'):
        score += len(results['headers']['missing_headers']) * 10
    if 'error' not in results['ssl'] and not results['ssl']['valid']:
        score += 50
    if 'error' not in results['ports'] and results['ports'].get('open_ports'):
        score += len(results['ports']['open_ports']) * 20
    if 'error' not in results['cookies'] and results['cookies'].get('insecure_cookies'):
        score += len(results['cookies']['insecure_cookies']) * 15
    return min(score, 100)  # Cap at 100

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
