import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import NotFound from "./NotFound.jsx";
import JobDesc from "../components/jobDesc.jsx";
import MetadataBox from "../components/MetadataBox.jsx";
import {
    getLogo,
    getDateScraped,
    getExperienceRange,
    getSalaryRange,
} from "../utils/jobDetails.js";
import "../styles/JobInfo.css";

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
        <div id="job-info" className="w-250 mx-auto ">
            <div id="job-info-heading" className="py-16 text-left">
                <div className="flex items-center ">
                    <img
                        src={getLogo(jobInfo.companyName)}
                        alt={`${jobInfo.companyName} logo`}
                        className="h-12 w-auto max-h-full max-w-full"
                    />
                    <a href={jobInfo.jobUrl} target="_blank">
                        <h1 className="pl-8">{jobInfo.jobTitle}</h1>
                    </a>
                </div>
            </div>
            <div className="flex items-start">
                <JobDesc text={jobInfo.jobDesc} />
                <MetadataBox
                    url={jobInfo.jobUrl}
                    company={jobInfo.companyName}
                    salary={getSalaryRange(jobInfo)}
                    experience={getExperienceRange(jobInfo)}
                    dateScraped={getDateScraped(jobInfo)}
                />
            </div>
        </div>
    );
}
