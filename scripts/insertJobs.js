const db = require('../db'); // Adjust the path if needed

const jobs = [
    { title: 'Software Engineer', description: 'Develop full-stack applications.', location: 'New York', salary: 100000 },
    { title: 'Sustainability Analyst', description: 'Analyze eco-friendly solutions.', location: 'San Francisco', salary: 85000 },
    { title: 'Mechanical Engineer', description: 'Design energy-efficient systems.', location: 'Los Angeles', salary: 95000 }
];

jobs.forEach(job => {
    db.query(
        'INSERT INTO jobs (title, description, location, salary) VALUES (?, ?, ?, ?)',
        [job.title, job.description, job.location, job.salary],
        (err, result) => {
            if (err) {
                console.error('Error inserting job:', err);
            } else {
                console.log('Job inserted:', job.title);
            }
        }
    );
});

db.end(); // Close the database connection
