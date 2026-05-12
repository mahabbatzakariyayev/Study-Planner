"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import ErrorMessage from "@/components/ErrorMessage";
import LoadingState from "@/components/LoadingState";
import PageHeader from "@/components/PageHeader";
import StatCard from "@/components/StatCard";
import { analyticsApi, studentsApi } from "@/lib/api";
import { DashboardStats, Student } from "@/types";

const ACTIVE_STUDENT_KEY = "activeStudentId";

export default function DashboardPage() {
  const [student, setStudent] = useState<Student | null>(null);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      setError(null);
      try {
        const students = await studentsApi.getStudents();
        if (students.length === 0) {
          setStudent(null);
          setStats(null);
          return;
        }

        const storedId = Number(localStorage.getItem(ACTIVE_STUDENT_KEY));
        const selectedStudent = students.find((s) => s.id === storedId) ?? students[0];
        setStudent(selectedStudent);
        localStorage.setItem(ACTIVE_STUDENT_KEY, String(selectedStudent.id));

        const dashboardStats = await analyticsApi.getDashboardStats(selectedStudent.id);
        setStats(dashboardStats);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
    <section className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="This client calls a separate FastAPI REST API over HTTP JSON. The backend owns all business logic, validation, and SQLite operations."
      />

      {loading ? <LoadingState message="Loading dashboard..." /> : null}
      {error ? <ErrorMessage message={`Backend/API error: ${error}`} /> : null}

      {!loading && !student ? (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6">
          <p className="text-slate-700">No student found. Create one to start planning.</p>
          <Link href="/students" className="mt-4 inline-block rounded-md bg-teal-700 px-4 py-2 text-white">
            Go to Students
          </Link>
        </div>
      ) : null}

      {student && stats ? (
        <>
          <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-600">Active student</p>
            <p className="text-lg font-semibold text-slate-900">{student.name}</p>
            <p className="text-sm text-slate-600">{student.email}</p>
          </div>

          <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-5">
            <StatCard title="Total Tasks" value={stats.total_tasks} />
            <StatCard title="Pending Tasks" value={stats.pending_tasks} />
            <StatCard title="Completed Tasks" value={stats.completed_tasks} />
            <StatCard title="Upcoming Exams" value={stats.upcoming_exams} />
            <StatCard title="Generated Sessions" value={stats.generated_sessions} />
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-900">Quick Actions</h3>
            <div className="mt-3 flex flex-wrap gap-2">
              <Link href="/tasks" className="rounded-md bg-teal-700 px-3 py-2 text-sm text-white">Add Task</Link>
              <Link href="/exams" className="rounded-md bg-teal-700 px-3 py-2 text-sm text-white">Add Exam</Link>
              <Link href="/schedule" className="rounded-md bg-teal-700 px-3 py-2 text-sm text-white">Generate Schedule</Link>
              <Link href="/notifications" className="rounded-md bg-teal-700 px-3 py-2 text-sm text-white">View Notifications</Link>
            </div>
          </div>
        </>
      ) : null}
    </section>
  );
}
