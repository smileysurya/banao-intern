import json
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email validation regex
EMAIL_REGEX = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

def create_response(status_code, body):
    """Create HTTP response with proper headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps(body)
    }

def validate_email(email):
    """Validate email format"""
    return re.match(EMAIL_REGEX, email.strip()) is not None

def send_email(event, context):
    """
    Lambda function to send email
    
    Args:
        event: API Gateway event with body containing receiver_email, subject, body_text
        context: Lambda context
        
    Returns:
        HTTP response with appropriate status code
    """
    try:
        # Parse request body
        try:
            if isinstance(event.get('body'), str):
                body = json.loads(event['body'])
            else:
                body = event.get('body', {})
            
            if not body:
                return create_response(400, {
                    'error': 'Invalid JSON format',
                    'message': 'Request body must be valid JSON'
                })
        except json.JSONDecodeError:
            return create_response(400, {
                'error': 'Invalid JSON format',
                'message': 'Request body must be valid JSON'
            })
        
        # Extract and validate fields
        receiver_email = body.get('receiver_email', '').strip()
        subject = body.get('subject', '').strip()
        body_text = body.get('body_text', '').strip()
        
        # Validate required fields
        if not receiver_email or not subject or not body_text:
            return create_response(400, {
                'error': 'Missing or empty required fields',
                'message': 'receiver_email, subject, and body_text are required and cannot be empty',
                'received': {
                    'receiver_email': bool(receiver_email),
                    'subject': bool(subject),
                    'body_text': bool(body_text)
                }
            })
        
        # Validate email format
        if not validate_email(receiver_email):
            return create_response(400, {
                'error': 'Invalid email format',
                'message': 'receiver_email must be a valid email address'
            })
        
        # Check environment variables
        email_user = os.environ.get('EMAIL_USER')
        email_pass = os.environ.get('EMAIL_PASS')
        
        if not email_user or not email_pass:
            print('ERROR: Missing email configuration')
            return create_response(500, {
                'error': 'Server configuration error',
                'message': 'Email service is not properly configured'
            })
        
        # Log request (without sensitive data)
        print(f'Processing email request: receiver={receiver_email}, subject={subject[:50]}')
        
        # Create email message
        message = MIMEMultipart()
        message['From'] = email_user
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body_text, 'plain'))
        
        # Send email via Gmail SMTP
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(email_user, email_pass)
                server.send_message(message)
            
            print(f'Email sent successfully to {receiver_email}')
            
            # Success response
            return create_response(200, {
                'success': True,
                'message': 'Email sent successfully',
                'data': {
                    'receiver': receiver_email,
                    'subject': subject,
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                }
            })
            
        except smtplib.SMTPAuthenticationError as e:
            print(f'ERROR: SMTP Authentication failed: {str(e)}')
            return create_response(401, {
                'error': 'Authentication failed',
                'message': 'Invalid email credentials. Please check EMAIL_USER and EMAIL_PASS.'
            })
        
        except smtplib.SMTPConnectError as e:
            print(f'ERROR: Could not connect to SMTP server: {str(e)}')
            return create_response(503, {
                'error': 'Service unavailable',
                'message': 'Could not connect to email server. Please try again later.'
            })
        
        except smtplib.SMTPException as e:
            print(f'ERROR: SMTP error: {str(e)}')
            return create_response(500, {
                'error': 'SMTP error',
                'message': 'Failed to send email via SMTP'
            })
    
    except Exception as error:
        print(f'ERROR: Unexpected error: {str(error)}')
        import traceback
        traceback.print_exc()
        return create_response(500, {
            'error': 'Internal server error',
            'message': 'Failed to send email',
            'details': str(error) if os.environ.get('NODE_ENV') == 'development' else None
        })