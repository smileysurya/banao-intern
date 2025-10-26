const nodemailer = require('nodemailer');

// Email validation regex
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Create transporter (reuse connection)
let transporter = null;

const getTransporter = () => {
  if (!transporter) {
    transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS,
      },
    });
  }
  return transporter;
};

/**
 * Send Email Lambda Function
 * @param {Object} event - API Gateway event
 * @returns {Object} HTTP response
 */
module.exports.sendEmail = async (event) => {
  try {
    // Parse request body
    let body;
    try {
      body = JSON.parse(event.body);
    } catch (parseError) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          error: 'Invalid JSON format',
          message: 'Request body must be valid JSON',
        }),
      };
    }

    const { receiver_email, subject, body_text } = body;

    // Validate required fields
    if (!receiver_email || !subject || !body_text) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          error: 'Missing required fields',
          message: 'receiver_email, subject, and body_text are required',
          received: {
            receiver_email: !!receiver_email,
            subject: !!subject,
            body_text: !!body_text,
          },
        }),
      };
    }

    // Validate email format
    if (!emailRegex.test(receiver_email)) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          error: 'Invalid email format',
          message: 'receiver_email must be a valid email address',
        }),
      };
    }

    // Validate field types
    if (typeof subject !== 'string' || typeof body_text !== 'string') {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          error: 'Invalid field types',
          message: 'subject and body_text must be strings',
        }),
      };
    }

    // Check environment variables
    if (!process.env.EMAIL_USER || !process.env.EMAIL_PASS) {
      console.error('Missing email configuration');
      return {
        statusCode: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          error: 'Server configuration error',
          message: 'Email service is not properly configured',
        }),
      };
    }

    // Configure email options
    const mailOptions = {
      from: process.env.EMAIL_USER,
      to: receiver_email,
      subject: subject,
      text: body_text,
    };

    // Send email
    const transport = getTransporter();
    const info = await transport.sendMail(mailOptions);

    console.log('Email sent successfully:', info.messageId);

    // Success response
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        success: true,
        message: 'Email sent successfully',
        data: {
          receiver: receiver_email,
          subject: subject,
          messageId: info.messageId,
          timestamp: new Date().toISOString(),
        },
      }),
    };

  } catch (error) {
    console.error('Error sending email:', error);

    // Handle specific nodemailer errors
    if (error.code === 'EAUTH') {
      return {
        statusCode: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          error: 'Authentication failed',
          message: 'Invalid email credentials',
        }),
      };
    }

    if (error.code === 'ECONNECTION') {
      return {
        statusCode: 503,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          error: 'Service unavailable',
          message: 'Could not connect to email server',
        }),
      };
    }

    // Generic error response
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        error: 'Internal server error',
        message: 'Failed to send email',
        details: process.env.NODE_ENV === 'development' ? error.message : undefined,
      }),
    };
  }
};