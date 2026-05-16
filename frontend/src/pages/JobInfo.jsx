import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import NotFound from "./NotFound.jsx";
import JobDesc from "../components/jobDesc.jsx";
import { getExperienceRange, getSalaryRange } from "../utils/jobDetails.js";

export default function JobInfo() {
    const [jobInfo, setJobInfo] = useState(undefined);
    const { jobId } = useParams();

    useEffect(() => {
        async function getJobInfo() {
            try {
                const response = await fetch(
                    `http://localhost:8080/jobs/${jobId}`,
                );
                if (!response.ok)
                    throw new Error("Failed to fetch job details");
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
            <h2>{getExperienceRange(jobInfo)}</h2>
            <h2>{getSalaryRange(jobInfo)}</h2>
            <a href={jobInfo.jobUrl} target="_blank">
                Apply Now
            </a>
            <div>
                -------------------------------------------------------------------------------
            </div>
            <br />
            <br />
            {/* <p>{JSON.stringify(jobInfo.jobDesc)}</p> */}
            {/* <div id="jobDesc">{formattedText}</div> */}
            <JobDesc text={jobInfo.jobDesc} />
            {/* {console.log(jobInfo.jobDesc)} */}
            {/* <div>{formatJobDesc()}</div> */}
        </div>
    );
}
