export function getLogo(job) {
    const path = `/logos/${job.companyName.toLowerCase()}`;
    const svgs = new Set(["Airbnb", "Apple", "Databricks", "Block", "Uber"]);
    const pngs = new Set(["Block", "OpenAI"]);
    const jpegs = new Set(["Stripe", "Uber"]);

    if (svgs.has(job.companyName)) return path + ".svg";
    else if (pngs.has(job.companyName)) return path + ".png";
    else if (jpegs.has(job.companyName)) return path + ".jpeg";
}

export function getExperienceRange(job) {
    let minExp = job.minExperience;
    let maxExp = job.maxExperience;

    if (!minExp && !maxExp) return "Years of Experience: N/A";
    else if (!maxExp) return `Years of Experience: ${minExp}+`;
    return `Years of Experience: ${minExp} – ${maxExp}`;
}

export function getSalaryRange(job) {
    let minSalary = job.minSalary ? job.minSalary.toString() : null;
    let maxSalary = job.maxSalary ? job.maxSalary.toString() : null;

    if (!minSalary && !maxSalary) return "Salary Range: N/A";

    minSalary = `\$${minSalary.slice(0, -3)},${minSalary.slice(-3)}`;
    if (!maxSalary) return `Salary Range: ${minSalary}+`;

    maxSalary = `\$${maxSalary.slice(0, -3)},${maxSalary.slice(-3)}`;
    return `Salary Range: ${minSalary} – ${maxSalary}`;
}
