import "../styles/index.css";
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
      className="w-full flex items-center justify-between pt-3 text-sm"
    >
      <h2 className="text-(--text2)">{`Showing ${Math.min(
        offset + jobCount,
        totalJobs
      )} of ${totalJobs} open jobs`}</h2>
      <button
        id="filterClear"
        className="underline-offset-2 bg-[#00000000]"
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
