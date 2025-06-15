from flask import Flask, request, jsonify, session, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
import uuid
from datetime import datetime, timedelta
import json
from analyzer import BJJAnalyzer
import yt_dlp
import tempfile
import threading
from functools import wraps
import secrets
import paypalrestsdk
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# PayPal Configuration
paypalrestsdk.configure({
    "mode": os.environ.get('PAYPAL_MODE', 'sandbox'),
    "client_id": os.environ.get('PAYPAL_CLIENT_ID', 'your_paypal_client_id'),
    "client_secret": os.environ.get('PAYPAL_CLIENT_SECRET', 'your_paypal_client_secret')
})

# OAuth Configuration
oauth = OAuth(app)
facebook = oauth.register(
    name='facebook',
    client_id=os.environ.get('FACEBOOK_CLIENT_ID', 'your_facebook_client_id'),
    client_secret=os.environ.get('FACEBOOK_CLIENT_SECRET', 'your_facebook_client_secret'),
    server_metadata_url='https://graph.facebook.com/.well-known/openid_configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Initialize BJJ Analyzer
analyzer = BJJAnalyzer()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('clips', exist_ok=True)

# Black Belt Access Codes
BLACK_BELT_CODES = {
    'BJJMASTER2024': {'uses_left': 10, 'expires': '2025-12-31'},
    'FRIENDCODE123': {'uses_left': 5, 'expires': '2025-06-30'},
    'UNLIMITED001': {'uses_left': -1, 'expires': '2026-01-01'}  # -1 = unlimited
}

def init_db():
    """Initialize the database with all necessary tables"""
    conn = sqlite3.connect('bjj_analyzer.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE
