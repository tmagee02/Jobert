import JobRow from "./JobRow.jsx";

export default function JobsGrid({ jobs }) {
  return (
    <div
      id="jobsGrid"
      className="flex flex-col bg-black min-w-210 max-w-1/2 px-3 py-3 space-y-4"
    >
      {jobs.map((job, i) => (
        <div key={job.JobId}>
          <JobRow job={job} />
          {i < jobs.length - 1 && <hr />}
        </div>
      ))}
    </div>
  );
}
