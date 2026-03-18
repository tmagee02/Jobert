import "../styles/index.css";
import "../styles/filters.css";

export default function FilterExperience({
  setOffset,
  experience,
  setExperience,
}) {
  const NO_FILTER = -1;
  const MAX_EXPERIENCE = 30;

  return (
    <div
      id="filterExperience"
      className="w-50 h-10 flex items-center justify-between font-semibold text-sm"
    >
      <button
        id="decrementExperience"
        className="buttonExp"
        onClick={() => {
          if (experience > NO_FILTER) {
            setOffset(0);
            setExperience((prev) => prev - 1);
          }
        }}
      >
        <i className="fa-solid fa-minus" />
      </button>
      <div className="h-full flex items-center justify-center select-none">
        {experience >= 0
          ? `Experience: ${experience} yrs`
          : "Experience: – yrs"}
      </div>
      <button
        id="incrementExperience"
        className="buttonExp"
        onClick={() => {
          if (experience < MAX_EXPERIENCE) {
            setOffset(0);
            setExperience((prev) => prev + 1);
          }
        }}
      >
        <i className="fa-solid fa-plus" />
      </button>
    </div>
  );
}
