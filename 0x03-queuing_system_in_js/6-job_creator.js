import kue from 'kue';

// Create a job queue named push_notification_code
const queue = kue.createQueue();

// Create an object containing the Job data
const jobData = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account'
};

// Create a job with the provided data
const job = queue.create('push_notification_code', jobData);

// When the job is created without error
job.on('enqueue', () => {
  console.log(`Notification job created: ${job.id}`);
});

// When the job is completed
job.on('complete', () => {
  console.log('Notification job completed');
});

// When the job fails
job.on('failed', () => {
  console.log('Notification job failed');
});

// Save the job to the queue
job.save();
