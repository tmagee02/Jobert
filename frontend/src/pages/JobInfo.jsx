import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function JobInfo() {
  const [jobInfo, setJobInfo] = useState(null);
  const { jobId } = useParams();

  useEffect(() => {
    fetch(`http://localhost:8000/jobs/${jobId}/`)
      .then((response) => response.json())
      .then((json) => setJobInfo(json));
  }, []);

  if (!jobInfo) return <p>LOADING...</p>;

  console.log(jobInfo);

  return (
    <div id="job-info">
      <h1>Job Info {jobId}</h1>
      <h2>Job info here</h2>
      <h1>{jobInfo.Title}</h1>
      <h2>{jobInfo.Company}</h2>
      <h2>{jobInfo.DateScraped}</h2>
      <a href={jobInfo.JobUrl} target="_blank">
        Apply Now
      </a>
      <br />
      <br />
      <p>{JSON.stringify(jobInfo.JobDesc)}</p>
    </div>
  );
}
