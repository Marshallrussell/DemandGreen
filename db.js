const mysql = require('mysql2');

const db = mysql.createConnection({
    host: 'localhost',   // Change if using a remote database
    user: 'root',       // Replace with your MySQL username (could be 'admin' or 'root')
    password: 'password',  // Replace with your actual MySQL password
    database: 'jobsDB'   // Replace with the actual name of your database
});

db.connect(err => {
    if (err) {
        console.error('Database connection failed:', err);
    } else {
        console.log('Connected to the database');
    }
});

module.exports = db;
