import "../styles/index.css";
import "../styles/filters.css";
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
      className="w-full flex items-end justify-between text-sm"
    >
      <h2 className="text-(--text2) text-base">{`Showing ${Math.min(
        offset + jobCount,
        totalJobs
      )} of ${totalJobs} open jobs`}</h2>
      <button
        id="filterClear"
        className="underline-offset-2"
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
