import { getLogo } from "../utils/jobDetails";

export default function CompanyDropdownItem({
    companyName,
    checkedCompanies,
    setCheckedCompanies,
}) {
    return (
        <li id={`companyDropdownItem-${companyName}`} className=" select-none">
            <label className="flex items-center justify-between">
                <div className="flex items-center">
                    <div className="w-6 h-6 flex items-center justify-center">
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
