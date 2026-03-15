import { useState, useEffect } from "react";
import Filters from "../components/Filters.jsx";
import JobsGrid from "../components/JobsGrid.jsx";
import "../styles/index.css";
import "../styles/JobRow.css";

export default function Jobs() {
  const [backendData, setBackendData] = useState([]);
  const [totalJobs, setTotalJobs] = useState(0);
  const [offset, setOffset] = useState(0);
  const jobCount = 20;

  //filter states
  const [salary, setSalary] = useState("");
  const [experience, setExperience] = useState("");

  useEffect(() => {
    document.title = "Jobs";
    const fetchInitialJobs = async () => {
      const res = await fetch(
        `http://localhost:8000/jobs?offset=${offset}&jobCount=${jobCount}&salary=${salary}&experience=${experience}`
      );
      const data = await res.json();
      setBackendData(data["jobList"]);
      setTotalJobs(data["totalJobs"]);
      setOffset(jobCount);
      console.log(offset);
    };
    fetchInitialJobs();
  }, [salary, experience]);

  const fetchMoreJobs = async () => {
    const res = await fetch(
      `http://localhost:8000/jobs?offset=${offset}&jobCount=${jobCount}&salary=${salary}&experience=${experience}`
    );
    const data = await res.json();
    console.log(`${offset}, ${jobCount}`);
    setOffset((prev) => prev + jobCount);
    console.log(offset);
    setBackendData((prev) => [...prev, ...data["jobList"]]);
  };

  if (backendData.length == 0) return <p></p>;

  // console.log(backendData);
  // console.log(backendData[0]["JobId"]);
  const jobId = backendData[1]["JobId"];
  const jobUrl = backendData[1]["JobUrl"];
  const jobCompany = backendData[1]["Company"];
  const jobTitle = backendData[1]["Title"];

  return (
    <div id="jobs" className="w-250 mx-auto flex flex-col items-center">
      <h1 className="text-5xl">Discover new job openings.</h1>
      <h2>jobs list here</h2>
      <Filters
        salary={salary}
        setSalary={setSalary}
        experience={experience}
        setExperience={setExperience}
      />
      <div className="bg-amber-600 w-full flex items-center justify-between">
        <h2 className="bg-purple-400">{`Showing ${offset} of ${totalJobs} open jobs`}</h2>
        <div id="filterClear" className="bg-indigo-400">
          Clear filters
        </div>
      </div>
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
