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
      className="w-full py-4 flex items-center justify-around text-sm font-semibold text-[var(--text1)] sticky top-0 z-99"
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
