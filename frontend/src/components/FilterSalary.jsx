export default function FilterSalary({ setOffset, salary, setSalary }) {
  return (
    <div
      id="filterSalary"
      className="w-50 h-10 flex items-center justify-center"
    >
      <input
        id="inputSalary"
        type="number"
        placeholder="Minimum desired salary"
        value={salary}
        onKeyDown={(e) => {
          if (["e", "E", "+", "-"].includes(e.key)) {
            e.preventDefault();
          }
        }}
        onChange={(e) => {
          const numbers = e.target.value.replace(/\D/g, "");
          if (numbers.length <= 6) {
            setOffset(0);
            setSalary(numbers);
          }
        }}
      />
    </div>
  );
}
