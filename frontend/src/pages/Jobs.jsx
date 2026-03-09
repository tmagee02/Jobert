import { useState, useEffect } from "react";
import JobsGrid from "../components/JobsGrid.jsx";

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
      <JobsGrid jobs={backendData} />
    </div>
  );
}
