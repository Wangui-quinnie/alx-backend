import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const port = 1245;

// Redis client setup
const redisClient = redis.createClient();
const setAsync = promisify(redisClient.set).bind(redisClient);
const getAsync = promisify(redisClient.get).bind(redisClient);

// Kue queue setup
const queue = kue.createQueue();

// Initialize available seats to 50
setAsync('available_seats', 50);

// Initialize reservationEnabled to true
let reservationEnabled = true;

// Function to reserve a seat
const reserveSeat = async (number) => {
    await setAsync('available_seats', number);
};

// Function to get the current available seats
const getCurrentAvailableSeats = async () => {
    const availableSeats = await getAsync('available_seats');
    return parseInt(availableSeats);
};

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservation are blocked' });
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            return res.json({ status: 'Reservation failed' });
        }
        res.json({ status: 'Reservation in process' });
    });
});

// Route to process the queue and reserve a seat
app.get('/process', async (req, res) => {
    res.json({ status: 'Queue processing' });

    const currentAvailableSeats = await getCurrentAvailableSeats();
    const newAvailableSeats = currentAvailableSeats - 1;

    if (newAvailableSeats === 0) {
        reservationEnabled = false;
    }

    if (newAvailableSeats >= 0) {
        reserveSeat(newAvailableSeats);
    } else {
        queue.active((err, ids) => {
            ids.forEach(id => {
                kue.Job.get(id, (err, job) => {
                    if (err) return;
                    job.failed(new Error('Not enough seats available'));
                });
            });
        });
    }
});

// Event listener for job completion
queue.on('job complete', (id) => {
    console.log(`Seat reservation job ${id} completed`);
});

// Event listener for job failure
queue.on('job failed', (id, errorMessage) => {
    console.log(`Seat reservation job ${id} failed: ${errorMessage}`);
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
