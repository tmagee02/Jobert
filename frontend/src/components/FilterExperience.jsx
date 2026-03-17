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
      className="flex items-center justify-between border-2 rounded-md border-(--mid) box-border"
    >
      <button
        id="decrementExperience"
        onClick={() => {
          if (experience > NO_FILTER) {
            setOffset(0);
            setExperience((prev) => prev - 1);
          }
        }}
      >
        <i className="fa-solid fa-minus" />
      </button>
      <div className="w-6 flex items-center justify-center">
        {experience >= 0 ? experience : "-"}
      </div>
      <button
        id="incrementExperience"
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
