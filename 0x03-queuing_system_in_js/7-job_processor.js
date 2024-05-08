import kue from 'kue';

// Array of blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Function to send notification
function sendNotification(phoneNumber, message, job, done) {
  // Track the progress of the job
  job.progress(0, 100);

  // Check if phoneNumber is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    // Fail the job with an Error object
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Track the progress to 50%
  job.progress(50, 100);

  // Log to the console
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

  // Call the done callback to indicate job completion
  done();
}

// Create a job queue with Kue
const queue = kue.createQueue();

// Process jobs from the queue with two jobs at a time
queue.process('push_notification_code_2', 2, (job, done) => {
  // Extract data from the job
  const { phoneNumber, message } = job.data;

  // Call the sendNotification function with job details
  sendNotification(phoneNumber, message, job, done);
});
