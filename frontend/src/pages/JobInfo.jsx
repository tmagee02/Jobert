import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import NotFound from "./NotFound.jsx";

export default function JobInfo() {
  const [jobInfo, setJobInfo] = useState(undefined);
  const { jobId } = useParams();

  const getExperienceRange = () => {
    let minExp = jobInfo.minExperience;
    let maxExp = jobInfo.maxExperience;

    if (!minExp && !maxExp) return "Years of Experience: N/A";
    else if (!maxExp) return `Years of Experience: ${minExp}+`;
    return `Years of Experience: ${minExp} – ${maxExp}`;
  };

  useEffect(() => {
    async function getJobInfo() {
      try {
        const response = await fetch(`http://localhost:8080/jobs/${jobId}`);
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
      <h1>{jobInfo.jobTitle}</h1>
      <h2>{jobInfo.company}</h2>
      <h2>{jobInfo.dateScraped}</h2>
      <h2>{getExperienceRange()}</h2>
      <h2>
        Salary Range: {jobInfo.minExperience} - {jobInfo.maxExperience}
      </h2>
      <a href={jobInfo.jobUrl} target="_blank">
        Apply Now
      </a>
      <br />
      <br />
      <p>{JSON.stringify(jobInfo.jobDesc)}</p>
    </div>
  );
}
