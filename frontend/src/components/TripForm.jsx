// frontend/src/components/TripForm.jsx
import { useState } from "react";

export default function TripForm({ onSubmit, loading }) {
  const [form, setForm] = useState({
    origin: "",
    destination: "",
    departure: "",
    load_lbs: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white shadow rounded space-y-3">
      <input
        placeholder="Origin"
        value={form.origin}
        onChange={(e) => setForm({ ...form, origin: e.target.value })}
        className="w-full border p-2 rounded"
        required
      />
      <input
        placeholder="Destination"
        value={form.destination}
        onChange={(e) => setForm({ ...form, destination: e.target.value })}
        className="w-full border p-2 rounded"
        required
      />
      <input
        type="datetime-local"
        value={form.departure}
        onChange={(e) => setForm({ ...form, departure: e.target.value })}
        className="w-full border p-2 rounded"
        required
      />
      <input
        type="number"
        placeholder="Load weight (lbs)"
        value={form.load_lbs}
        onChange={(e) => setForm({ ...form, load_lbs: e.target.value })}
        className="w-full border p-2 rounded"
        required
      />
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Planning..." : "Plan Route"}
      </button>
    </form>
  );
}