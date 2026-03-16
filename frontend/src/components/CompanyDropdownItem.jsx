export default function CompanyDropdownItem({
  companyName,
  checkedCompanies,
  setCheckedCompanies,
}) {
  return (
    <li
      id={`companyDropdownItem-${companyName}`}
      className="bg-gray-400 select-none"
    >
      <label className="bg-amber-300">
        <input
          id={`checkbox-${companyName}`}
          type="checkbox"
          checked={checkedCompanies.has(companyName)}
          onChange={() =>
            setCheckedCompanies((prev) => {
              const nextState = new Set(prev);

              if (nextState.has(companyName)) {
                nextState.delete(companyName);
              } else {
                nextState.add(companyName);
              }
              console.log(nextState);
              return nextState;
            })
          }
        ></input>
        {companyName}
      </label>
    </li>
  );
}
