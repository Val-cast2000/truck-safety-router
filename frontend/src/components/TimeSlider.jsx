// frontend/src/components/TimeSlider.jsx
export default function TimeSlider({ value, onChange }) {
  return (
    <div className="absolute bottom-4 left-4 right-4 bg-white/90 p-3 rounded shadow z-[1000]">
      <label className="text-sm font-semibold">
        Forecast: +{value} hours
      </label>
      <input
        type="range"
        min={0}
        max={48}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full"
      />
      <div className="flex justify-between text-xs text-gray-500">
        <span>Now</span>
        <span>+24h</span>
        <span>+48h</span>
      </div>
    </div>
  );
}