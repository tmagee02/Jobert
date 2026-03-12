import { Link } from "react-router-dom";
import "../styles/JobRow.css";
// import apple from "../assets/logos/apple_logo.svg";

export default function JobRow({ job }) {
  const getLogo = (company) => {
    const path = `/logos/${company.toLowerCase()}`;
    const svgs = new Set(["Airbnb", "Apple", "Databricks", "Block", "Uber"]);
    const pngs = new Set(["Block", "OpenAI"]);
    const jpegs = new Set(["Stripe", "Uber"]);

    if (svgs.has(company)) return path + ".svg";
    else if (pngs.has(company)) return path + ".png";
    else if (jpegs.has(company)) return path + ".jpeg";
  };
  const getExperienceRange = () => {
    let minExp = job.MinExperience;
    let maxExp = job.MaxExperience;

    if (minExp === -1 && maxExp === -1) return "Years of Experience: N/A";
    else if (maxExp === -1 || maxExp === minExp)
      return `Years of Experience: ${minExp}+`;

    return `Years of Experience: ${minExp} – ${maxExp}`;
  };

  const getSalaryRange = () => {
    let minSalary = job.MinSalary ? job.MaxSalary.toString() : "-1";
    let maxSalary = job.MaxSalary ? job.MaxSalary.toString() : "-1";

    if (
      (!minSalary && !maxSalary) ||
      (minSalary === "-1" && maxSalary === "-1")
    )
      return "Salary Range: N/A";
    console.log(minSalary, maxSalary);
    minSalary = `\$${minSalary.slice(0, -3)},${minSalary.slice(-3)}`;
    maxSalary = `\$${maxSalary.slice(0, -3)},${maxSalary.slice(-3)}`;
    return `Salary Range: ${minSalary} – ${maxSalary}`;
  };

  return (
    <Link to={`/jobs/${job.JobId}`}>
      <div
        id="jobRow"
        className="bg-white grid grid-cols-[80px_1fr_325px_35px] items-center gap-3"
      >
        <div
          id="company"
          className="bg-green-500 text-black h-10 flex items-center justify-center px-3 py-1"
        >
          <img
            src={getLogo(job.Company)}
            alt={`${job.Company} logo`}
            className="h-auto w-auto max-h-full max-w-full bg-blue-800"
          />
        </div>
        <div
          id="jobTitle"
          className="bg-gray-300 text-white min-w-0 pl-5 line-clamp-2 "
        >
          <span className="text-[22px] text-(--bg-mid) font-bold">
            {job.Title}
          </span>
        </div>
        <div id="ranges" className="bg-blue-300 text-[17px] font-semibold">
          <div id="salaryRange" className="bg-green-600">
            {getSalaryRange()}
          </div>
          <div id="experienceRange" className="bg-yellow-600">
            {getExperienceRange()}
          </div>
        </div>
        <i class="fa-solid fa-chevron-right"></i>
      </div>
    </Link>
  );
}
