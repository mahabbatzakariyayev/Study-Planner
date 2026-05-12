"use client";

import { FormEvent, useState } from "react";

import { ExamCreateInput } from "@/types";

interface ExamFormProps {
  studentId: number;
  onSubmit: (payload: ExamCreateInput) => Promise<void>;
}

export default function ExamForm({ studentId, onSubmit }: ExamFormProps) {
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState<Omit<ExamCreateInput, "student_id">>({
    subject: "",
    course_name: "",
    exam_date: "",
    importance: 3,
    estimated_revision_hours: 4,
  });

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      await onSubmit({ student_id: studentId, ...form });
      setForm({
        subject: "",
        course_name: "",
        exam_date: "",
        importance: 3,
        estimated_revision_hours: 4,
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="text-lg font-medium text-slate-900">Add Exam</h3>
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2"
        placeholder="Subject"
        value={form.subject}
        onChange={(event) => setForm((prev) => ({ ...prev, subject: event.target.value }))}
        required
      />
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2"
        placeholder="Course Name"
        value={form.course_name}
        onChange={(event) => setForm((prev) => ({ ...prev, course_name: event.target.value }))}
      />
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2"
        type="date"
        value={form.exam_date}
        onChange={(event) => setForm((prev) => ({ ...prev, exam_date: event.target.value }))}
        required
      />
      <div className="grid grid-cols-2 gap-2">
        <input
          className="w-full rounded-md border border-slate-300 px-3 py-2"
          type="number"
          min={1}
          max={5}
          value={form.importance}
          onChange={(event) => setForm((prev) => ({ ...prev, importance: Number(event.target.value) }))}
          required
        />
        <input
          className="w-full rounded-md border border-slate-300 px-3 py-2"
          type="number"
          min={0.5}
          step={0.5}
          value={form.estimated_revision_hours}
          onChange={(event) => setForm((prev) => ({ ...prev, estimated_revision_hours: Number(event.target.value) }))}
          required
        />
      </div>
      <button
        type="submit"
        disabled={loading}
        className="rounded-md bg-teal-700 px-4 py-2 text-white hover:bg-teal-800 disabled:opacity-50"
      >
        {loading ? "Saving..." : "Add Exam"}
      </button>
    </form>
  );
}
