const fetch = require('node-fetch');

const API_URL = 'http://localhost:3000/dev/send-email';

// Test data
const testEmail = {
  receiver_email: 'recipient@example.com', // Change this to your test email
  subject: 'Test Email from Serverless API',
  body_text: 'This is a test email sent from the serverless email API.',
};

async function testSendEmail() {
  try {
    console.log('Sending test email...');
    console.log('Payload:', JSON.stringify(testEmail, null, 2));

    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testEmail),
    });

    const data = await response.json();

    console.log('\n--- Response ---');
    console.log('Status:', response.status);
    console.log('Data:', JSON.stringify(data, null, 2));

  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Test missing fields
async function testMissingFields() {
  try {
    console.log('\n\nTesting missing fields...');
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        receiver_email: 'test@example.com',
      }),
    });

    const data = await response.json();
    console.log('Status:', response.status);
    console.log('Data:', JSON.stringify(data, null, 2));

  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Test invalid email
async function testInvalidEmail() {
  try {
    console.log('\n\nTesting invalid email...');
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        receiver_email: 'invalid-email',
        subject: 'Test',
        body_text: 'Test body',
      }),
    });

    const data = await response.json();
    console.log('Status:', response.status);
    console.log('Data:', JSON.stringify(data, null, 2));

  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Run all tests
async function runTests() {
  await testSendEmail();
  await testMissingFields();
  await testInvalidEmail();
}

runTests();