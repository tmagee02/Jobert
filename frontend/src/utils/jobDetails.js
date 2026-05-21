export function getLogo(job) {
    const path = `/logos/${job.companyName.toLowerCase()}`;
    const svgs = new Set(["Airbnb", "Apple", "Databricks", "Block", "Uber"]);
    const pngs = new Set(["Block", "OpenAI"]);
    const jpegs = new Set(["Stripe", "Uber"]);

    if (svgs.has(job.companyName)) return path + ".svg";
    else if (pngs.has(job.companyName)) return path + ".png";
    else if (jpegs.has(job.companyName)) return path + ".jpeg";
}

export function getDateScraped(job) {
    const d = new Date(job.dateScraped.slice(0, -3) + "Z"); // Z at the end tells JS that the date is initially UTC
    return `${d.toLocaleString(undefined, { dateStyle: "short" })} • ${d.toLocaleString(undefined, { timeStyle: "short" })}`;
}

export function getExperienceRange(job) {
    let minExp = job.minExperience;
    let maxExp = job.maxExperience;

    if (!minExp && !maxExp) return "N/A";
    else if (!maxExp) return `${minExp}+`;
    return `${minExp} – ${maxExp}`;
}

export function getSalaryRange(job) {
    let minSalary = job.minSalary ? job.minSalary.toString() : null;
    let maxSalary = job.maxSalary ? job.maxSalary.toString() : null;

    if (!minSalary && !maxSalary) return "N/A";

    minSalary = `\$${minSalary.slice(0, -3)},${minSalary.slice(-3)}`;
    if (!maxSalary) return `${minSalary}+`;

    maxSalary = `\$${maxSalary.slice(0, -3)},${maxSalary.slice(-3)}`;
    return `${minSalary} – ${maxSalary}`;
}
