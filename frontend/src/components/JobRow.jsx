import { Link } from "react-router-dom";

export default function JobRow({ job }) {
  const getExperienceRange = () => {
    let minExp = job.MinExperience;
    let maxExp = job.MaxExperience;

    return `${minExp} _ ${maxExp}`;
  };
  const getSalaryRange = () => {
    let minSalary = job.MinSalary ? job.MaxSalary.toString() : "-1";
    let maxSalary = job.MaxSalary ? job.MaxSalary.toString() : "-1";

    if (
      (!minSalary && !maxSalary) ||
      (minSalary === "-1" && maxSalary === "-1")
    )
      return "Salary N/A";
    console.log(minSalary, maxSalary);
    minSalary = `\$${minSalary.slice(0, -3)},${minSalary.slice(-3)}`;
    maxSalary = `\$${maxSalary.slice(0, -3)},${maxSalary.slice(-3)}`;
    return `${minSalary} - ${maxSalary}`;
  };
  return (
    <div
      id="jobRow"
      className="bg-rose-900 my-5 grid grid-cols-[80px_500px_150px_150px] items-center gap-1"
    >
      <div id="company" className="bg-fuchsia-700">
        {job.JobId} --- {job.Company}:
      </div>
      <div id="jobTitle" className="bg-gray-600 text-green-400 min-w-0">
        <Link
          to={`/jobs/${job.JobId}`}
          className="block max-w-full truncate text-white"
        >
          {job.Title}
        </Link>
      </div>
      <div id="salaryRange" className="bg-green-600">
        {getSalaryRange()}
      </div>
      <div id="experienceRange" className="bg-yellow-600">
        {getExperienceRange()}
      </div>
    </div>
  );
}
