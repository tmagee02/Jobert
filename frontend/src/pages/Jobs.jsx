import { useState, useEffect } from "react";
import JobsGrid from "../components/JobsGrid.jsx";
import "../styles/index.css";
import "../styles/JobRow.css";

export default function Jobs() {
  const [backendData, setBackendData] = useState([]);
  const [totalJobs, setTotalJobs] = useState(0);
  const [offset, setOffset] = useState(0);
  const jobCount = 20;

  const fetchMoreJobs = async () => {
    const res = await fetch(
      `http://localhost:8000/jobs?offset=${offset}&jobCount=${jobCount}`
    );
    const data = await res.json();
    console.log(`${offset}, ${jobCount}`);
    setOffset((prev) => prev + jobCount);
    console.log(offset);
    setBackendData((prev) => [...prev, ...data["jobList"]]);
  };

  useEffect(() => {
    document.title = "Jobs";
    const fetchInitialJobs = async () => {
      const res = await fetch(
        `http://localhost:8000/jobs?offset=${offset}&jobCount=${jobCount}`
      );
      const data = await res.json();
      setBackendData(data["jobList"]);
      setTotalJobs(data["totalJobs"]);
      setOffset(jobCount);
      console.log(offset);
    };
    fetchInitialJobs();
  }, []);

  if (backendData.length == 0) return <p>LOADING...</p>;

  // console.log(backendData);
  // console.log(backendData[0]["JobId"]);
  const jobId = backendData[1]["JobId"];
  const jobUrl = backendData[1]["JobUrl"];
  const jobCompany = backendData[1]["Company"];
  const jobTitle = backendData[1]["Title"];

  return (
    <div id="jobs" className="flex flex-col items-center">
      <h1 className="my-10 font-semibold text-5xl tracking-tighter text-(--dark)">
        Discover new job openings.
      </h1>
      <h2>jobs list here</h2>
      <JobsGrid jobs={backendData} />
      {backendData.length < totalJobs && (
        <button
          className="my-5 flex items-center justify-between"
          onClick={() => fetchMoreJobs()}
        >
          View more positions
          <i className="fa-solid fa-chevron-down ml-2" />
        </button>
      )}
    </div>
  );
}
