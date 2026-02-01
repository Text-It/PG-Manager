import sys
import os

# Add the project root to sys.path so we can import 'app'
# Netlify puts the function in a specific folder, so we might need to go up
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import aws_wsgi
from app import create_app

# Initialize the app
app = create_app()

def handler(event, context):
    """
    Netlify Function Handler using aws-wsgi to bridge Flask
    """
    # Important: Netlify might pass 'isBase64Encoded' which aws-wsgi handles
    return aws_wsgi.response(app, event, context)
