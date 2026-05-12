"use client";

import { useEffect, useState } from "react";

import ErrorMessage from "@/components/ErrorMessage";
import LoadingState from "@/components/LoadingState";
import PageHeader from "@/components/PageHeader";
import StudentForm from "@/components/StudentForm";
import { studentsApi } from "@/lib/api";
import { Student } from "@/types";

const ACTIVE_STUDENT_KEY = "activeStudentId";

export default function StudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [activeStudentId, setActiveStudentId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadStudents() {
    setLoading(true);
    setError(null);
    try {
      const data = await studentsApi.getStudents();
      setStudents(data);
      const storedId = Number(localStorage.getItem(ACTIVE_STUDENT_KEY));
      if (data.length > 0) {
        const selected = data.find((student) => student.id === storedId) ?? data[0];
        setActiveStudentId(selected.id);
        localStorage.setItem(ACTIVE_STUDENT_KEY, String(selected.id));
      } else {
        setActiveStudentId(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load students");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadStudents();
  }, []);

  async function handleCreateStudent(payload: {
    name: string;
    email: string;
    study_hours_per_day: number;
    preferred_start_time?: string;
    preferred_end_time?: string;
  }) {
    await studentsApi.createStudent(payload);
    await loadStudents();
  }

  async function handleCreateDemoStudent() {
    try {
      await studentsApi.createStudent({
        name: "Demo Student",
        email: "demo@student.com",
        study_hours_per_day: 4,
        preferred_start_time: "09:00",
        preferred_end_time: "18:00",
      });
      await loadStudents();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create demo student");
    }
  }

  function handleSetActive(studentId: number) {
    setActiveStudentId(studentId);
    localStorage.setItem(ACTIVE_STUDENT_KEY, String(studentId));
  }

  return (
    <section className="space-y-6">
      <PageHeader
        title="Students"
        description="Create and manage students. The selected active student is saved in localStorage for all pages."
      />

      {loading ? <LoadingState message="Loading students..." /> : null}
      {error ? <ErrorMessage message={error} /> : null}

      <div className="grid gap-6 lg:grid-cols-2">
        <StudentForm onSubmit={handleCreateStudent} />

        <div className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-slate-900">Student List</h3>
            <button
              onClick={handleCreateDemoStudent}
              className="rounded-md bg-slate-800 px-3 py-2 text-sm text-white hover:bg-slate-900"
            >
              Create Demo Student
            </button>
          </div>

          {students.length === 0 ? (
            <p className="text-sm text-slate-600">No students yet.</p>
          ) : (
            students.map((student) => (
              <div
                key={student.id}
                className={`rounded-lg border p-3 ${
                  activeStudentId === student.id
                    ? "border-teal-700 bg-teal-50"
                    : "border-slate-200 bg-white"
                }`}
              >
                <p className="font-medium text-slate-900">{student.name}</p>
                <p className="text-sm text-slate-600">{student.email}</p>
                <p className="text-xs text-slate-500">Study hours/day: {student.study_hours_per_day}</p>
                <button
                  onClick={() => handleSetActive(student.id)}
                  className="mt-2 rounded bg-teal-700 px-3 py-1 text-xs text-white"
                >
                  {activeStudentId === student.id ? "Active Student" : "Set Active"}
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </section>
  );
}
