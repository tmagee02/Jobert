import JobRow from "./JobRow.jsx";

export default function JobsGrid({ jobs }) {
  return (
    <div
      id="jobsGrid"
      className="flex flex-col bg-black mx-100 px-3 py-3 space-y-3"
    >
      {jobs.map((job, i) => (
        <>
          <JobRow job={job} />
        </>
      ))}
    </div>
  );
}
