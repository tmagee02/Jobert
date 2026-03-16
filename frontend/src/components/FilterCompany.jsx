import { useState, useEffect, useRef } from "react";
import CompanyDropdown from "./CompanyDropdown.jsx";

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
    <div id="filterCompany" className="bg-green-500">
      <button ref={refButton} onClick={() => setOpen((prev) => !prev)}>
        Company filter
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
