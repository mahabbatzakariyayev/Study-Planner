"use client";

import { FormEvent, useState } from "react";

import { TaskCreateInput } from "@/types";

interface TaskFormProps {
  studentId: number;
  onSubmit: (payload: TaskCreateInput) => Promise<void>;
}

export default function TaskForm({ studentId, onSubmit }: TaskFormProps) {
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState<Omit<TaskCreateInput, "student_id">>({
    title: "",
    description: "",
    course_name: "",
    deadline: "",
    difficulty: 3,
    estimated_hours: 2,
    is_exam_related: false,
    status: "pending",
  });

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      await onSubmit({ student_id: studentId, ...form });
      setForm({
        title: "",
        description: "",
        course_name: "",
        deadline: "",
        difficulty: 3,
        estimated_hours: 2,
        is_exam_related: false,
        status: "pending",
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="text-lg font-medium text-slate-900">Add Task</h3>
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2"
        placeholder="Title"
        value={form.title}
        onChange={(event) => setForm((prev) => ({ ...prev, title: event.target.value }))}
        required
      />
      <textarea
        className="w-full rounded-md border border-slate-300 px-3 py-2"
        placeholder="Description"
        value={form.description}
        onChange={(event) => setForm((prev) => ({ ...prev, description: event.target.value }))}
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
        value={form.deadline}
        onChange={(event) => setForm((prev) => ({ ...prev, deadline: event.target.value }))}
        required
      />
      <div className="grid grid-cols-2 gap-2">
        <input
          className="w-full rounded-md border border-slate-300 px-3 py-2"
          type="number"
          min={1}
          max={5}
          value={form.difficulty}
          onChange={(event) => setForm((prev) => ({ ...prev, difficulty: Number(event.target.value) }))}
          required
        />
        <input
          className="w-full rounded-md border border-slate-300 px-3 py-2"
          type="number"
          min={0.5}
          step={0.5}
          value={form.estimated_hours}
          onChange={(event) => setForm((prev) => ({ ...prev, estimated_hours: Number(event.target.value) }))}
          required
        />
      </div>
      <label className="flex items-center gap-2 text-sm text-slate-700">
        <input
          type="checkbox"
          checked={form.is_exam_related}
          onChange={(event) => setForm((prev) => ({ ...prev, is_exam_related: event.target.checked }))}
        />
        Exam related task
      </label>
      <button
        type="submit"
        disabled={loading}
        className="rounded-md bg-teal-700 px-4 py-2 text-white hover:bg-teal-800 disabled:opacity-50"
      >
        {loading ? "Saving..." : "Add Task"}
      </button>
    </form>
  );
}
