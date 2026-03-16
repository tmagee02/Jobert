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
  const [committedCompanies, setCommittedCompanies] = useState([]);
  const [salary, setSalary] = useState("");
  const [experience, setExperience] = useState(-1);

  useEffect(() => {
    document.title = "Jobs";
    const fetchJobs = async () => {
      const params = new URLSearchParams();
      params.append("offset", offset);
      params.append("jobCount", jobCount);
      if (salary) params.append("salary", salary);
      params.append("experience", experience);
      committedCompanies.forEach((company) => {
        params.append("companies", company);
      });
      console.log(params.toString());
      const res = await fetch(
        // `http://localhost:8000/jobs?offset=${offset}&jobCount=${jobCount}&salary=${salary}&experience=${experience}`
        `http://localhost:8000/jobs?${params.toString()}`
      );
      const data = await res.json();
      if (offset === 0) {
        setTotalJobs(data["totalJobs"]);
        setBackendData(data["jobList"]);
      } else {
        setBackendData((prev) => [...prev, ...data["jobList"]]);
      }
    };
    fetchJobs();
  }, [offset, committedCompanies, salary, experience]);

  if (backendData.length == 0) return <p></p>;

  return (
    <div id="jobs" className="w-250 mx-auto flex flex-col items-center">
      <h1 className="text-5xl">Discover new job openings.</h1>
      <h2>jobs list here</h2>
      <Filters
        setOffset={setOffset}
        committedCompanies={committedCompanies}
        setCommittedCompanies={setCommittedCompanies}
        salary={salary}
        setSalary={setSalary}
        experience={experience}
        setExperience={setExperience}
      />
      <div className="bg-amber-600 w-full flex items-center justify-between">
        <h2 className="bg-purple-400">{`Showing ${Math.min(
          offset + jobCount,
          totalJobs
        )} of ${totalJobs} open jobs`}</h2>
        <div id="filterClear" className="bg-indigo-400">
          Clear filters
        </div>
      </div>
      <JobsGrid jobs={backendData} />
      {backendData.length < totalJobs && (
        <button
          className="my-5 flex items-center justify-between"
          onClick={() => setOffset((prev) => prev + jobCount)}
        >
          View more positions
          <i className="fa-solid fa-chevron-down ml-2" />
        </button>
      )}
    </div>
  );
}
