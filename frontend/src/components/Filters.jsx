import "../styles/Filters.css";

export default function Filters({
  setOffset,
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
      <button id="filterCompany" className="bg-green-300">
        Companies
      </button>
      <div
        id="filterSalary"
        className="bg-orange-300 flex items-center justify-around"
      >
        <i
          id="money"
          className="fa-solid fa-dollar-sign bg-violet-800 h-auto fa-lg"
        />
        <input
          type="number"
          placeholder="Salary"
          value={salary}
          className="bg-cyan-500"
          onKeyDown={(e) => {
            if (["e", "E", "+", "-"].includes(e.key)) {
              e.preventDefault();
            }
          }}
          onChange={(e) => {
            const onlyNumbers = e.target.value.replace(/\D/g, "");
            setOffset(0);
            setSalary(onlyNumbers);
          }}
        />
      </div>

      <div id="filterExperience" className="bg-blue-200">
        Experience
        <input
          type="number"
          placeholder="Experience"
          value={experience}
          className="bg-cyan-500"
          onKeyDown={(e) => {
            if (["e", "E", "+", "-"].includes(e.key)) {
              e.preventDefault();
            }
          }}
          onChange={(e) => {
            const onlyNumbers = e.target.value.replace(/\D/g, "");
            setOffset(0);
            setExperience(onlyNumbers);
          }}
        />
      </div>
    </div>
  );
}
