import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import NotFound from "./NotFound.jsx";

export default function JobInfo() {
  const [jobInfo, setJobInfo] = useState(undefined);
  const { jobId } = useParams();

  useEffect(() => {
    async function getJobInfo() {
      try {
        const response = await fetch(`http://localhost:8000/jobs/${jobId}/`);
        if (!response.ok) throw new Error("Failed to fetch job details");
        const json = await response.json();
        setJobInfo(json);
      } catch (error) {
        setJobInfo(null);
        console.error(error);
      }
    }
    getJobInfo();
  }, [jobId]);

  console.log(jobInfo);
  if (jobInfo === undefined) return <p>LOADING...</p>;
  if (jobInfo === null) return <NotFound />;

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
