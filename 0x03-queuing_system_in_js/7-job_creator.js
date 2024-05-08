import kue from 'kue';

// Array of jobs
const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153538781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4159518782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4158718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153818782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4154318781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account'
  }
];

// Create a job queue named push_notification_code_2
const queue = kue.createQueue();

// Loop through the jobs array and create a job for each object
jobs.forEach((jobData, index) => {
  // Create a new job with the current object
  const job = queue.create('push_notification_code_2', jobData);

  // If there is no error, log to the console
  job.on('enqueue', () => {
    console.log(`Notification job created: ${job.id}`);
  });

  // On job completion, log to the console
  job.on('complete', () => {
    console.log(`Notification job ${job.id} completed`);
  });

  // On job failure, log to the console
  job.on('failed', (errorMessage) => {
    console.log(`Notification job ${job.id} failed: ${errorMessage}`);
  });

  // On job progress, log to the console
  job.on('progress', (progress, data) => {
    console.log(`Notification job ${job.id} ${progress}% complete`);
  });

  // Save the job to the queue
  job.save();
});
