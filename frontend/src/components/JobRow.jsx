import { Link } from "react-router-dom";
import "../styles/index.css";
import "../styles/JobRow.css";
import {
  getLogo,
  getExperienceRange,
  getSalaryRange,
  getDateScraped,
} from "../utils/jobDetails";

export default function JobRow({ job, newestDateScraped }) {
  console.log(job.id);
  return (
    <Link to={`/jobs/${job.id}`}>
      <div
        id="jobRow"
        className="grid grid-cols-[80px_1fr_310px_35px] items-center gap-4"
      >
        <div
          id="company"
          className="h-10 flex items-center justify-center px-3 py-1"
        >
          <img
            src={getLogo(job.companyName)}
            alt={`${job.companyName} logo`}
            className="h-auto w-auto max-h-full max-w-full"
          />
        </div>
        <div id="leftText">
          <span
            id="jobTitle"
            className="text-[22px] text-(--text1) font-bold line-clamp-2"
          >
            {job.jobTitle}
          </span>

          <div id="location" className="secondary-text flex align-center">
            San Francisco, California, United States
            {getDateScraped(job) === newestDateScraped && (
              <div id="newJobIndicator" className="flex align-center">
                New
              </div>
            )}
          </div>
        </div>
        <div id="rightText" className="secondary-text text-[16px]">
          <div id="salaryRange">Salary Range: {getSalaryRange(job)}</div>
          <div id="experienceRange">
            Years of Experience: {getExperienceRange(job)}
          </div>
        </div>
        <i
          id="chevron"
          className="fa-solid fa-chevron-right text-(--text2) transition-all"
        ></i>
      </div>
    </Link>
  );
}
