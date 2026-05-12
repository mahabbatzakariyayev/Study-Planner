"use client";

import { FormEvent, useState } from "react";

import { StudentCreateInput } from "@/types";

interface StudentFormProps {
  onSubmit: (payload: StudentCreateInput) => Promise<void>;
}

export default function StudentForm({ onSubmit }: StudentFormProps) {
  const [form, setForm] = useState<StudentCreateInput>({
    name: "",
    email: "",
    study_hours_per_day: 4,
    preferred_start_time: "09:00",
    preferred_end_time: "18:00",
  });
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      await onSubmit(form);
      setForm({
        name: "",
        email: "",
        study_hours_per_day: 4,
        preferred_start_time: "09:00",
        preferred_end_time: "18:00",
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="text-lg font-medium text-slate-900">Create Student</h3>
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2"
        placeholder="Name"
        value={form.name}
        onChange={(event) => setForm((prev) => ({ ...prev, name: event.target.value }))}
        required
      />
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2"
        placeholder="Email"
        type="email"
        value={form.email}
        onChange={(event) => setForm((prev) => ({ ...prev, email: event.target.value }))}
        required
      />
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2"
        placeholder="Study Hours Per Day"
        type="number"
        min={1}
        max={12}
        step={0.5}
        value={form.study_hours_per_day}
        onChange={(event) => setForm((prev) => ({ ...prev, study_hours_per_day: Number(event.target.value) }))}
        required
      />
      <button
        type="submit"
        disabled={loading}
        className="rounded-md bg-teal-700 px-4 py-2 text-white hover:bg-teal-800 disabled:opacity-50"
      >
        {loading ? "Creating..." : "Create Student"}
      </button>
    </form>
  );
}
