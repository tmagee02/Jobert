export default function FilterExperience({
  setOffset,
  experience,
  setExperience,
}) {
  const NO_FILTER = -1;
  const MAX_EXPERIENCE = 30;

  return (
    <div id="filterExperience" className="bg-blue-200">
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
      {experience >= 0 ? experience : "-"}
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
