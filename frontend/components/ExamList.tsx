"use client";

import { formatDate, formatHours } from "@/lib/date";
import { Exam } from "@/types";

interface ExamListProps {
  exams: Exam[];
  onDelete: (examId: number) => Promise<void>;
}

export default function ExamList({ exams, onDelete }: ExamListProps) {
  if (exams.length === 0) {
    return <p className="rounded-xl border border-dashed border-slate-300 p-6 text-sm text-slate-600">No exams yet.</p>;
  }

  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 text-slate-700">
          <tr>
            <th className="p-3">Subject</th>
            <th className="p-3">Course</th>
            <th className="p-3">Exam Date</th>
            <th className="p-3">Importance</th>
            <th className="p-3">Revision Hours</th>
            <th className="p-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          {exams.map((exam) => (
            <tr key={exam.id} className="border-t border-slate-100">
              <td className="p-3 font-medium text-slate-900">{exam.subject}</td>
              <td className="p-3">{exam.course_name || "-"}</td>
              <td className="p-3">{formatDate(exam.exam_date)}</td>
              <td className="p-3">{exam.importance}</td>
              <td className="p-3">{formatHours(exam.estimated_revision_hours)}</td>
              <td className="p-3">
                <button className="rounded bg-rose-600 px-2 py-1 text-xs text-white" onClick={() => onDelete(exam.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
