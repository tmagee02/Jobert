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

    function formatJobDesc(jobDesc) {
        /*
    start with whole text, lines separated by \n
    goal: determine if each line is a subheader, a bullet, or neither

    To see if header, use score based system, goal is 3 points
      if line ends with colon, +3
      if line below certain length, +1
      if title case (and not just one word maybe?), +2
      matches common header name, +2 

    To see if bullet
      check if previous line was a header 
        and prevHeader matches any of predetermined header names, yes
      if previous line was a bullet 
        and current line is not a header, yes

    Now we keep groups instead of just lines in the list
    also keep the current bulletgroup
    if line is a bullet
        if bulletgroup dne
            make one
            push bulletgroup to groups
        add line to bullet group
    else
        add line to groups with type
    */
        const groups = [];
        let prevHeaderText = null;
        let prevWasBullet = false;
        let bulletGroup = null;
        const commonBulletHeaders = new Set([
            "minimum qualifications",
            "preferred qualifications",
        ]);

        for (const line of jobInfo.jobDesc.split("\n")) {
            // console.log(line.length, line);
            const headerScore = scoreLine(line);
            const curIsHeader = headerScore >= 3;
            const curIsBullet =
                (prevHeaderText &&
                    (commonBulletHeaders.has(prevHeaderText.toLowerCase()) ||
                        commonBulletHeaders.has(
                            prevHeaderText.slice(0, -1),
                        ))) ||
                (prevWasBullet && !curIsHeader && line.length != 0);

            if (curIsBullet) {
                if (!bulletGroup) {
                    bulletGroup = { type: "bulletGroup", bullets: [] };
                    groups.push(bulletGroup);
                }
                bulletGroup.bullets.push(line);
            } else {
                bulletGroup = null;
                let lineType = "text";
                if (curIsHeader) lineType = "header";
                groups.push({ type: lineType, text: line });
            }

            prevHeaderText = curIsHeader ? line : null;
            prevWasBullet = curIsBullet;
        }
        console.log(groups);
    }

    function scoreLine(line) {
        let score = 0;
        if (line.at(-1) === ":") score += 3;
        if (line.length <= 40) score += 1;
        if (isTitleCase(line)) score += 2;
        if (isCommonHeader(line)) score += 2;
        return score;
    }

    function isTitleCase(line) {
        const wordExceptions = new Set(["the", "of"]);
        const tokens = line.split(" ");
        if (!tokens[0]) return false;
        for (const token of tokens) {
            if (wordExceptions.has(token)) continue;
            if (token) if (token === token.toLowerCase()) return false;
        }
        return true;
    }

    function isCommonHeader(line) {
        const commonHeaders = new Set([
            "about the role",
            "about the team",
            "minimum qualifications",
            "preferred qualifications",
        ]);
        if (
            commonHeaders.has(line.toLowerCase()) ||
            commonHeaders.has(line.slice(0, -1).toLowerCase())
        )
            return true;
        return false;
    }

    const formattedText = jobInfo.jobDesc.split("\n").map((line, i) => (
        <span key={i}>
            {line}
            <br />
            <br />
        </span>
    ));

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
            <div>
                -------------------------------------------------------------------------------
            </div>
            <br />
            <br />
            {/* <p>{JSON.stringify(jobInfo.jobDesc)}</p> */}
            <div>{formattedText}</div>
            <div>{formatJobDesc()}</div>
        </div>
    );
}
