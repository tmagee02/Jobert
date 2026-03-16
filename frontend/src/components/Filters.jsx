import FilterCompany from "./FilterCompany.jsx";
import FilterSalary from "./FilterSalary.jsx";
import FilterExperience from "./FilterExperience.jsx";
import "../styles/Filters.css";

export default function Filters({
  setOffset,
  committedCompanies,
  setCommittedCompanies,
  salary,
  setSalary,
  experience,
  setExperience,
}) {
  return (
    <div
      id="filters"
      className="bg-red-500 w-full grid grid-cols-3 items-center gap-4 text-base"
    >
      <FilterCompany
        setOffset={setOffset}
        committedCompanies={committedCompanies}
        setCommittedCompanies={setCommittedCompanies}
      />
      <FilterSalary
        setOffset={setOffset}
        salary={salary}
        setSalary={setSalary}
      />
      <FilterExperience
        setOffset={setOffset}
        experience={experience}
        setExperience={setExperience}
      />
    </div>
  );
}
