export default function MetadataBox({
    url,
    company,
    salary,
    experience,
    dateScraped,
}) {
    return (
        <div id="metadata-box" className="w-400">
            <div id="meta-company" className="metadata-child flex items-start">
                <div className="w-4 flex justify-center">
                    <i className="fa-solid fa-city text-[16px] mt-[3px]" />
                </div>
                <div className="ml-4">
                    <p className="font-medium text-base">Company</p>
                    <p className="font-light">{company}</p>
                </div>
            </div>
            <div id="meta-salary" className="metadata-child flex items-start">
                <div className="w-4 flex justify-center">
                    <i className="fa-solid fa-money-bill text-[16px] mt-[3px]" />
                </div>
                <div className="ml-4">
                    <p className="font-medium text-base">Salary</p>
                    <p className="font-light">{salary}</p>
                </div>
            </div>
            <div
                id="meta-experience"
                className="metadata-child flex items-start"
            >
                <div className="w-4 flex justify-center">
                    <i className="fa-solid fa-briefcase text-[16px] mt-[4px]" />
                </div>
                <div className="ml-4">
                    <p className="font-medium text-base">Experience</p>
                    <p className="font-light">
                        {experience} {experience == "N/A" ? "" : "years"}
                    </p>
                </div>
            </div>
            <div
                id="meta-datescraped"
                className="metadata-child flex items-start"
            >
                <div className="w-4 flex justify-center">
                    <i className="fa-solid fa-calendar-days text-[16px] mt-[4px]" />
                </div>
                <div className="ml-4">
                    <p className="font-medium text-base">Retrieved</p>
                    <p className="font-light">{dateScraped}</p>
                    {/* <p className="font-light">5/4/26 &bull; 12:34 PM UTC</p> */}
                </div>
            </div>
            <div id="meta-apply" className="metadata-child flex items-start">
                <a href={url} target="_blank">
                    Apply for this role
                    <i className="fa-solid fa-arrow-up-right-from-square ml-2" />
                </a>
            </div>
        </div>
    );
}
