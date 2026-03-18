import { useState, useEffect, useRef } from "react";
import CompanyDropdown from "./CompanyDropdown.jsx";
import "../styles/index.css";
import "../styles/filters.css";

export default function FilterCompany({
  setOffset,
  checkedCompanies,
  setCheckedCompanies,
  committedCompanies,
  setCommittedCompanies,
}) {
  const [open, setOpen] = useState(false);
  const refDropdown = useRef(null);
  const refButton = useRef(null);

  useEffect(() => {
    if (!open) {
      setOffset(0);
      setCommittedCompanies([...checkedCompanies]);
    }
  }, [open]);

  useEffect(() => {
    const handleClickOutsideDropdown = (event) => {
      if (
        refDropdown.current &&
        !refDropdown.current.contains(event.target) &&
        refButton.current &&
        !refButton.current.contains(event.target)
      ) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutsideDropdown);

    return () => {
      document.removeEventListener("mousedown", handleClickOutsideDropdown);
    };
  }, []);

  return (
    <div
      id="filterCompany"
      className="w-50 h-10 flex items-center justify-center bg-green-300"
    >
      <button
        ref={refButton}
        className="filterCompanyButton"
        onClick={() => setOpen((prev) => !prev)}
      >
        {checkedCompanies.size > 0
          ? `Companies (${checkedCompanies.size})`
          : `Companies`}
        <i className="fa-solid fa-chevron-down ml-2" />
      </button>
      {open && (
        <CompanyDropdown
          ref={refDropdown}
          checkedCompanies={checkedCompanies}
          setCheckedCompanies={setCheckedCompanies}
        />
      )}
    </div>
  );
}
