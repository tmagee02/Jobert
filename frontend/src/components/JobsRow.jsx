import { Link } from "react-router-dom";

export default function JobsRow({ job }) {
  const stringifySalaryRange = () => {
    let minSalary = job.JobId.toString();
    let maxSalary = job.JobId.toString();

    minSalary = `\$${minSalary.slice(0, -3)},${minSalary.slice(-3)}`;
    maxSalary = `\$${maxSalary.slice(0, -3)},${maxSalary.slice(-3)}`;
    return `${minSalary} - ${maxSalary}`;
  };
  return (
    <div id="JobsRow" className="bg-rose-900">
      <div>poopie</div>
      <div className="flex justify-left my-4">
        <div>
          {job.JobId} --- {job.Company}:
        </div>
        <li key={job.JobId} className="mx-4">
          <Link to={`/jobs/${job.JobId}`}>{job.Title}</Link>
        </li>
        <div>{stringifySalaryRange()}</div>
      </div>
    </div>
  );
}
