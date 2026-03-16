import CompanyDropdownItem from "./CompanyDropdownItem.jsx";

export default function CompanyDropdown({
  checkedCompanies,
  setCheckedCompanies,
  ref,
}) {
  const companies = [
    "Airbnb",
    "Apple",
    "Block",
    "Databricks",
    "OpenAI",
    "Stripe",
    "Uber",
  ];

  return (
    <div id="companyDropdown" ref={ref} className="bg-purple-500">
      Poop
      <ul>
        {companies.map((company, i) => (
          <CompanyDropdownItem
            key={i}
            companyName={company}
            checkedCompanies={checkedCompanies}
            setCheckedCompanies={setCheckedCompanies}
          />
        ))}
      </ul>
    </div>
  );
}
