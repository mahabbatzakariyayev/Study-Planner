"use client";

import { formatDate, formatHours } from "@/lib/date";
import { StudySession } from "@/types";

interface ScheduleTableProps {
  sessions: StudySession[];
  onComplete: (sessionId: number) => Promise<void>;
}

export default function ScheduleTable({ sessions, onComplete }: ScheduleTableProps) {
  if (sessions.length === 0) {
    return (
      <p className="rounded-xl border border-dashed border-slate-300 p-6 text-sm text-slate-600">
        No schedule generated yet.
      </p>
    );
  }

  const grouped = sessions.reduce<Record<string, StudySession[]>>((acc, session) => {
    const date = session.session_date;
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(session);
    return acc;
  }, {});

  return (
    <div className="space-y-4">
      {Object.entries(grouped).map(([sessionDate, daySessions]) => (
        <div key={sessionDate} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-lg font-semibold text-slate-900">{formatDate(sessionDate)}</h3>
          <div className="space-y-2">
            {daySessions.map((session) => (
              <div
                key={session.id}
                className="flex flex-col gap-2 rounded-lg border border-slate-200 p-3 md:flex-row md:items-center md:justify-between"
              >
                <div>
                  <p className="font-medium text-slate-900">{session.title}</p>
                  <p className="text-xs text-slate-600">
                    {session.session_type} | {formatHours(session.duration_hours)} | priority {session.priority_score.toFixed(2)}
                  </p>
                </div>
                <button
                  className="rounded bg-emerald-600 px-3 py-1 text-xs text-white disabled:opacity-50"
                  disabled={session.completed}
                  onClick={() => onComplete(session.id)}
                >
                  {session.completed ? "Completed" : "Mark completed"}
                </button>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
