export default function ResultsBar({
  offset,
  setOffset,
  jobCount,
  totalJobs,
  setCheckedCompanies,
  setCommittedCompanies,
  setSalary,
  setExperience,
}) {
  return (
    <div
      id="resultsBar"
      className="bg-amber-600 w-full flex items-center justify-between"
    >
      <h2 className="bg-purple-400">{`Showing ${Math.min(
        offset + jobCount,
        totalJobs
      )} of ${totalJobs} open jobs`}</h2>
      <button
        id="filterClear"
        className="bg-indigo-400"
        onClick={() => {
          setOffset(0);
          setCheckedCompanies(new Set());
          setCommittedCompanies([]);
          setSalary("");
          setExperience(-1);
        }}
      >
        Clear filters
      </button>
    </div>
  );
}
