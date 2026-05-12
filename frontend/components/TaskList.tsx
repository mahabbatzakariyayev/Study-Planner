"use client";

import { formatDate, formatHours } from "@/lib/date";
import { Task } from "@/types";

interface TaskListProps {
  tasks: Task[];
  onComplete: (taskId: number) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
}

export default function TaskList({ tasks, onComplete, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return <p className="rounded-xl border border-dashed border-slate-300 p-6 text-sm text-slate-600">No tasks yet.</p>;
  }

  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 text-slate-700">
          <tr>
            <th className="p-3">Title</th>
            <th className="p-3">Deadline</th>
            <th className="p-3">Difficulty</th>
            <th className="p-3">Hours</th>
            <th className="p-3">Priority</th>
            <th className="p-3">Status</th>
            <th className="p-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.id} className="border-t border-slate-100">
              <td className="p-3 font-medium text-slate-900">{task.title}</td>
              <td className="p-3">{formatDate(task.deadline)}</td>
              <td className="p-3">{task.difficulty}</td>
              <td className="p-3">{formatHours(task.estimated_hours)}</td>
              <td className="p-3">{task.priority_score.toFixed(2)}</td>
              <td className="p-3">{task.status}</td>
              <td className="p-3">
                <div className="flex gap-2">
                  <button
                    className="rounded bg-emerald-600 px-2 py-1 text-xs text-white disabled:opacity-50"
                    disabled={task.status === "completed"}
                    onClick={() => onComplete(task.id)}
                  >
                    Mark completed
                  </button>
                  <button
                    className="rounded bg-rose-600 px-2 py-1 text-xs text-white"
                    onClick={() => onDelete(task.id)}
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
