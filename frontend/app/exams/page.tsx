"use client";

import { useEffect, useState } from "react";

import ErrorMessage from "@/components/ErrorMessage";
import ExamForm from "@/components/ExamForm";
import ExamList from "@/components/ExamList";
import LoadingState from "@/components/LoadingState";
import PageHeader from "@/components/PageHeader";
import { examsApi } from "@/lib/api";
import { Exam, ExamCreateInput } from "@/types";

const ACTIVE_STUDENT_KEY = "activeStudentId";

export default function ExamsPage() {
  const [studentId, setStudentId] = useState<number | null>(null);
  const [exams, setExams] = useState<Exam[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadExams(currentStudentId: number) {
    setLoading(true);
    setError(null);
    try {
      const data = await examsApi.getExamsByStudent(currentStudentId);
      setExams(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load exams");
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
    loadExams(stored);
  }, []);

  async function handleCreateExam(payload: ExamCreateInput) {
    await examsApi.createExam(payload);
    await loadExams(payload.student_id);
  }

  async function handleDeleteExam(examId: number) {
    if (!studentId) return;
    await examsApi.deleteExam(examId);
    await loadExams(studentId);
  }

  return (
    <section className="space-y-6">
      <PageHeader
        title="Exams"
        description="Manage upcoming exams and revision load that will be added to generated schedules."
      />

      {!studentId ? <ErrorMessage message="No active student found. Please select a student first." /> : null}
      {loading ? <LoadingState message="Loading exams..." /> : null}
      {error ? <ErrorMessage message={error} /> : null}

      {studentId ? (
        <div className="space-y-6">
          <ExamForm studentId={studentId} onSubmit={handleCreateExam} />
          <ExamList exams={exams} onDelete={handleDeleteExam} />
        </div>
      ) : null}
    </section>
  );
}
