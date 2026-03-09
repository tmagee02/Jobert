import JobsRow from "./JobsRow.jsx";

export default function JobsGrid({ jobs }) {
  return (
    <div id="jobsGrid" className="bg-black mx-100 p-5">
      fewij
      <h1>poop</h1>
      <ul>
        {jobs.map((job) => (
          <JobsRow job={job} />
        ))}
      </ul>
    </div>
  );
}
