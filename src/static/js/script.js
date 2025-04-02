document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript is working!");
    alert("Welcome to GreenDemoX!");
});

const jobsDatabase = [
  { id: 1, title: 'Software Engineer', company: 'Tech Corp' },
  { id: 2, title: 'Product Manager', company: 'Biz Inc' },
  { id: 3, title: 'Data Scientist', company: 'DataWorks' },
];

app.get('/search', (req, res) => {
  const query = req.query.query;
  if (!query) {
    return res.status(400).json({ error: 'Query parameter is required' });
  }

  const filteredJobs = jobsDatabase.filter(job =>
    job.title.toLowerCase().includes(query.toLowerCase())
  );
  res.json(filteredJobs);
});
