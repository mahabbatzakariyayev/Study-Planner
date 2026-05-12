"use client";

import { useEffect, useState } from "react";

import ErrorMessage from "@/components/ErrorMessage";
import LoadingState from "@/components/LoadingState";
import PageHeader from "@/components/PageHeader";
import StatCard from "@/components/StatCard";
import { analyticsApi } from "@/lib/api";
import { DashboardStats } from "@/types";

const ACTIVE_STUDENT_KEY = "activeStudentId";

export default function AnalyticsPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadStats() {
      const stored = Number(localStorage.getItem(ACTIVE_STUDENT_KEY));
      if (!stored) {
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const data = await analyticsApi.getDashboardStats(stored);
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load analytics");
      } finally {
        setLoading(false);
      }
    }

    loadStats();
  }, []);

  return (
    <section className="space-y-6">
      <PageHeader
        title="Analytics"
        description="Dashboard metrics computed server-side from tasks, exams, and generated sessions."
      />

      {loading ? <LoadingState message="Loading analytics..." /> : null}
      {error ? <ErrorMessage message={error} /> : null}

      {!loading && !stats ? (
        <ErrorMessage message="No active student found. Please select a student first." />
      ) : null}

      {stats ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Total Tasks" value={stats.total_tasks} />
          <StatCard title="Pending Tasks" value={stats.pending_tasks} />
          <StatCard title="Completed Tasks" value={stats.completed_tasks} />
          <StatCard title="High Priority Tasks" value={stats.high_priority_tasks} />
          <StatCard title="Upcoming Exams" value={stats.upcoming_exams} />
          <StatCard title="Generated Sessions" value={stats.generated_sessions} />
          <StatCard title="Total Scheduled Hours" value={stats.total_scheduled_hours.toFixed(2)} />
          <StatCard title="Completion Rate" value={`${stats.completion_rate.toFixed(2)}%`} />
        </div>
      ) : null}
    </section>
  );
}
