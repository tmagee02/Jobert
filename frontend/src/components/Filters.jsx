import FilterCompany from "./FilterCompany.jsx";
import FilterSalary from "./FilterSalary.jsx";
import FilterExperience from "./FilterExperience.jsx";
import "../styles/filters.css";

export default function Filters({
  setOffset,
  checkedCompanies,
  setCheckedCompanies,
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
      className="w-full grid grid-cols-3 items-center gap-4 text-base"
    >
      <FilterCompany
        setOffset={setOffset}
        checkedCompanies={checkedCompanies}
        setCheckedCompanies={setCheckedCompanies}
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
