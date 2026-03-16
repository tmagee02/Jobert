export default function FilterExperience({
  setOffset,
  experience,
  setExperience,
}) {
  return (
    <div id="filterExperience" className="bg-blue-200">
      Experience
      <input
        type="number"
        placeholder="Experience"
        value={experience}
        className="bg-cyan-500"
        onKeyDown={(e) => {
          if (["e", "E", "+", "-"].includes(e.key)) {
            e.preventDefault();
          }
        }}
        onChange={(e) => {
          const onlyNumbers = e.target.value.replace(/\D/g, "");
          setOffset(0);
          setExperience(onlyNumbers);
        }}
      />
    </div>
  );
}
