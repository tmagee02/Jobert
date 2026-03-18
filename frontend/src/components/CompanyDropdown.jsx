import CompanyDropdownItem from "./CompanyDropdownItem.jsx";

export default function CompanyDropdown({
  open,
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
    <div
      id="companyDropdown"
      ref={ref}
      className={open ? "dropdownVisible" : ""}
    >
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
