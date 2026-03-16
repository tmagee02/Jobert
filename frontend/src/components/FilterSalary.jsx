export default function FilterSalary({ setOffset, salary, setSalary }) {
  return (
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
  );
}
