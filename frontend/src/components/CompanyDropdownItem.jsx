export default function CompanyDropdownItem({
  companyName,
  checkedCompanies,
  setCheckedCompanies,
}) {
  const getLogo = (company) => {
    const path = `/logos/${company.toLowerCase()}`;
    const svgs = new Set(["Airbnb", "Apple", "Databricks", "Block", "Uber"]);
    const pngs = new Set(["Block", "OpenAI"]);
    const jpegs = new Set(["Stripe", "Uber"]);

    if (svgs.has(company)) return path + ".svg";
    else if (pngs.has(company)) return path + ".png";
    else if (jpegs.has(company)) return path + ".jpeg";
  };

  return (
    <li id={`companyDropdownItem-${companyName}`} className=" select-none">
      <label className="flex items-center justify-between">
        <div className="flex items-center">
          <div className="w-5 h-5 flex items-center justify-center">
            <img
              src={getLogo(companyName)}
              alt={`${companyName} logo`}
              className="h-full w full bg-gren-300"
            />
          </div>
          <div className="pl-2">{companyName}</div>
        </div>
        <input
          id={`checkbox-${companyName}`}
          type="checkbox"
          className="accent-amber-200"
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
      </label>
    </li>
  );
}
