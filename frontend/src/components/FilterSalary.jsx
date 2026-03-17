export default function FilterSalary({ setOffset, salary, setSalary }) {
  return (
    <div
      id="filterSalary"
      className="flex items-center justify-center w-full h-full"
    >
      {/* <i
        id="money"
        className="fa-solid fa-dollar-sign bg-violet-800 h-auto fa-lg"
      /> */}
      <input
        type="number"
        placeholder="Salary"
        value={salary}
        className="w-full h-full border-amber-300 border-2"
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
