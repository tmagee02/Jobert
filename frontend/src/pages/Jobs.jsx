import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

export default function Jobs() {
  const [backendData, setBackendData] = useState([]);

  useEffect(() => {
    document.title = "Jobs";
    fetch("http://localhost:8000/jobs/")
      .then((response) => response.json())
      .then((data) => setBackendData(data));
  }, []);

  if (backendData.length == 0) return <p>LOADING...</p>;

  console.log(backendData);
  console.log(backendData[0]["JobId"]);
  const jobId = backendData[1]["JobId"];
  const jobUrl = backendData[1]["JobUrl"];
  const jobCompany = backendData[1]["Company"];
  const jobTitle = backendData[1]["Title"];

  return (
    <div id="jobs">
      <h1>Jobs</h1>
      <h2>jobs list here</h2>
      <ul>
        {backendData.map((job) => (
          <div className="flex justify-left my-4">
            <div>
              {job.JobId} --- {job.Company}:
            </div>
            <li key={job.JobId} className="mx-4">
              <Link to={`/jobs/${job.JobId}`}>{job.Title}</Link>
            </li>
          </div>
        ))}
      </ul>
    </div>
  );
}
