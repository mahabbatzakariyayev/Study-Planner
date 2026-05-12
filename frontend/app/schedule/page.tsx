"use client";

import { useEffect, useState } from "react";

import ErrorMessage from "@/components/ErrorMessage";
import LoadingState from "@/components/LoadingState";
import PageHeader from "@/components/PageHeader";
import ScheduleTable from "@/components/ScheduleTable";
import { schedulesApi } from "@/lib/api";
import { ScheduleGenerateResponse, StudySession } from "@/types";

const ACTIVE_STUDENT_KEY = "activeStudentId";

export default function SchedulePage() {
  const [studentId, setStudentId] = useState<number | null>(null);
  const [sessions, setSessions] = useState<StudySession[]>([]);
  const [warnings, setWarnings] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadSchedule(currentStudentId: number) {
    setLoading(true);
    setError(null);
    try {
      const data = await schedulesApi.getScheduleByStudent(currentStudentId);
      setSessions(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load schedule");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const stored = Number(localStorage.getItem(ACTIVE_STUDENT_KEY));
    if (!stored) {
      setLoading(false);
      return;
    }
    setStudentId(stored);
    loadSchedule(stored);
  }, []);

  async function handleGenerateSchedule() {
    if (!studentId) return;
    setError(null);
    try {
      const generated: ScheduleGenerateResponse = await schedulesApi.generateSchedule(studentId);
      setSessions(generated.sessions);
      setWarnings(generated.warnings);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate schedule");
    }
  }

  async function handleComplete(sessionId: number) {
    if (!studentId) return;
    await schedulesApi.completeSession(sessionId);
    await loadSchedule(studentId);
  }

  async function handleDeleteSchedule() {
    if (!studentId) return;
    await schedulesApi.deleteSchedule(studentId);
    setWarnings([]);
    await loadSchedule(studentId);
  }

  return (
    <section className="space-y-6">
      <PageHeader
        title="Schedule"
        description="Generate a study plan from tasks and exams using backend scheduling logic."
      />

      {!studentId ? <ErrorMessage message="No active student found. Please select a student first." /> : null}
      {loading ? <LoadingState message="Loading schedule..." /> : null}
      {error ? <ErrorMessage message={error} /> : null}

      {studentId ? (
        <>
          <div className="flex flex-wrap gap-2">
            <button onClick={handleGenerateSchedule} className="rounded-md bg-teal-700 px-4 py-2 text-white">
              Generate Study Schedule
            </button>
            <button onClick={handleDeleteSchedule} className="rounded-md bg-slate-700 px-4 py-2 text-white">
              Delete Schedule
            </button>
          </div>

          {warnings.length > 0 ? (
            <div className="rounded-xl border border-amber-300 bg-amber-50 p-4">
              <h3 className="font-semibold text-amber-900">Warnings</h3>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-amber-900">
                {warnings.map((warning) => (
                  <li key={warning}>{warning}</li>
                ))}
              </ul>
            </div>
          ) : null}

          <ScheduleTable sessions={sessions} onComplete={handleComplete} />
        </>
      ) : null}
    </section>
  );
}
