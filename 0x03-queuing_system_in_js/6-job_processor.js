import kue from 'kue';

// Create a job queue named push_notification_code
const queue = kue.createQueue();

// Function to send notification
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Process jobs in the queue
queue.process('push_notification_code', (job, done) => {
  // Extract phone number and message from job data
  const { phoneNumber, message } = job.data;
  
  // Call the sendNotification function with phone number and message
  sendNotification(phoneNumber, message);
  
  // Mark the job as completed
  done();
});
