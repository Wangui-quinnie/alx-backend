import { expect } from 'chai';
import sinon from 'sinon';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let sandbox;
  let queue;

  beforeEach(() => {
    sandbox = sinon.createSandbox();
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    sandbox.restore();
    queue.testMode.exit();
    queue.shutdown(5000, () => {
      console.log('Kue queue shut down');
    });
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 5678 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);

    const job1 = queue.testMode.jobs[0];
    expect(job1.type).to.equal('push_notification_code_3');
    expect(job1.data).to.deep.equal(jobs[0]);

    const job2 = queue.testMode.jobs[1];
    expect(job2.type).to.equal('push_notification_code_3');
    expect(job2.data).to.deep.equal(jobs[1]);
  });
});
