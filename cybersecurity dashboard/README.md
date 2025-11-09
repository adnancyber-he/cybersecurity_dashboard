# Cybersecurity Dashboard

A modern, full-stack web application for automated website security vulnerability scanning. Built with Flask (Python) backend and responsive HTML/CSS/JavaScript frontend featuring a dark, hacker-themed UI.

![Cybersecurity Dashboard](https://img.shields.io/badge/Status-Complete-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### Core Security Scanning
- **Security Headers Analysis**: Checks for missing critical headers (CSP, HSTS, X-Frame-Options, etc.)
- **SSL/TLS Certificate Validation**: Verifies certificate validity and configuration
- **Port Scanning**: Nmap-style scan for open ports and services
- **Cookie Security Audit**: Identifies insecure cookies and server information

### User Interface
- **Dark Cybersecurity Theme**: Black background with neon blue/green highlights
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Scanning**: Loading animations and progress indicators
- **Interactive Charts**: Chart.js visualizations for vulnerability data
- **Risk Score Calculation**: Automated scoring based on detected vulnerabilities

### User Management
- **User Authentication**: Secure login/register system
- **Scan History**: Personal dashboard with timestamped scan records
- **PDF Export**: Generate detailed security reports

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - User session management
- **SQLite** - Database (easily configurable for MySQL/PostgreSQL)

### Frontend
- **HTML5/CSS3** - Responsive UI with custom cybersecurity styling
- **JavaScript (ES6+)** - AJAX calls and dynamic interactions
- **Chart.js** - Data visualization

### Security Tools
- **Requests** - HTTP client for header/cookie analysis
- **SSL** - Certificate validation
- **python-nmap** - Port scanning
- **ReportLab** - PDF generation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Nmap (for port scanning functionality)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cybersecurity-dashboard.git
   cd cybersecurity-dashboard
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the dashboard**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 📖 Usage

### First Time Setup
1. Register a new account or login with existing credentials
2. Navigate to the main dashboard

### Performing a Security Scan
1. Enter a website URL (e.g., `https://example.com`)
2. Click "Scan Now"
3. Wait for the automated scanning process to complete
4. Review the results including:
   - Risk score (0-100)
   - Detailed vulnerability breakdown
   - Interactive charts
   - Recommendations

### Managing Scan History
- Click "History" to view previous scans
- Each entry shows URL, timestamp, and risk score
- Click "View Details" for full scan results

### Exporting Reports
- After a scan, click "Export PDF" to generate a downloadable report
- Reports include all scan details and risk assessment

## 🏗️ Project Structure

```
cybersecurity-dashboard/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── TODO.md                     # Development checklist
├── scanners/                   # Security scanning modules
│   ├── __init__.py
│   ├── header_scanner.py       # Security headers check
│   ├── ssl_scanner.py          # SSL/TLS validation
│   ├── port_scanner.py         # Port scanning
│   └── cookie_scanner.py       # Cookie analysis
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Main dashboard
│   ├── login.html             # Login page
│   └── register.html          # Registration page
├── static/                     # Static assets
│   ├── css/
│   │   └── styles.css         # Cybersecurity-themed styles
│   └── js/
│       └── app.js             # Frontend JavaScript
└── instance/                   # Database files (auto-generated)
    └── cybersecurity_dashboard.db
```

## 🔧 Configuration

### Database Configuration
The app uses SQLite by default. To use MySQL/PostgreSQL:

```python
# In app.py, modify:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# or
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/db_name'
```

### Security Settings
- Change the `SECRET_KEY` in `app.py` for production
- Implement password hashing (currently uses plain text for demo)
- Configure proper session handling

## 🧪 Testing

### Manual Testing Checklist
- [x] User registration and login
- [x] Security scanning functionality
- [x] Results display and visualization
- [x] History management
- [x] PDF export
- [x] Responsive design on mobile/desktop

### Running Tests
```bash
# Add unit tests in the future
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add docstrings to functions
- Test new features thoroughly
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and security testing purposes only. Always obtain permission before scanning websites or systems. The developers are not responsible for misuse of this tool.

## 🔮 Future Enhancements

- [ ] Advanced vulnerability detection (XSS, SQL injection, etc.)
- [ ] Scheduled automated scans
- [ ] Multi-user collaboration features
- [ ] Integration with security APIs
- [ ] Real-time notifications
- [ ] Advanced reporting and analytics
- [ ] API rate limiting and caching

## 📞 Support

If you encounter issues or have questions:
1. Check the [Issues](https://github.com/yourusername/cybersecurity-dashboard/issues) page
2. Create a new issue with detailed information
3. Include error messages, Python version, and steps to reproduce

---

**Happy Scanning! 🔒**

Built with ❤️ for cybersecurity education and awareness.
