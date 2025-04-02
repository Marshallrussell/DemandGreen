
// const fetch = require('node-fetch');
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'jobsDB',
});

connection.connect();

async function fetchJobs() {
  try {
    const response = await fetch('https://api.github.com/positions.json');
    const jobs = await response.json();

    // Insert each job into the database
    jobs.forEach(job => {
      const query = `
        INSERT INTO jobs (title, company, location, description, posted_date)
        VALUES (?, ?, ?, ?, ?)
      `;
      const values = [
        job.title,
        job.company,
        job.location || 'Unknown',
        job.description || 'No description provided',
        job.created_at ? new Date(job.created_at) : new Date(),
      ];

      connection.query(query, values, (err) => {
        if (err) console.error('Failed to insert job:', err);
      });
    });

    console.log('Jobs populated successfully.');
  } catch (error) {
    console.error('Error fetching jobs:', error);
  } finally {
    connection.end();
  }
}

fetchJobs();
