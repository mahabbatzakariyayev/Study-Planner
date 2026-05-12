"use client";

import { useEffect, useState } from "react";

import ErrorMessage from "@/components/ErrorMessage";
import LoadingState from "@/components/LoadingState";
import PageHeader from "@/components/PageHeader";
import TaskForm from "@/components/TaskForm";
import TaskList from "@/components/TaskList";
import { tasksApi } from "@/lib/api";
import { Task, TaskCreateInput } from "@/types";

const ACTIVE_STUDENT_KEY = "activeStudentId";

export default function TasksPage() {
  const [studentId, setStudentId] = useState<number | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadTasks(currentStudentId: number) {
    setLoading(true);
    setError(null);
    try {
      const data = await tasksApi.getTasksByStudent(currentStudentId);
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
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
    loadTasks(stored);
  }, []);

  async function handleCreateTask(payload: TaskCreateInput) {
    await tasksApi.createTask(payload);
    await loadTasks(payload.student_id);
  }

  async function handleCompleteTask(taskId: number) {
    if (!studentId) return;
    await tasksApi.updateTaskStatus(taskId, "completed");
    await loadTasks(studentId);
  }

  async function handleDeleteTask(taskId: number) {
    if (!studentId) return;
    await tasksApi.deleteTask(taskId);
    await loadTasks(studentId);
  }

  return (
    <section className="space-y-6">
      <PageHeader
        title="Tasks"
        description="Create tasks and track priority scores calculated by backend business logic."
      />

      {!studentId ? (
        <ErrorMessage message="No active student found. Please create/select a student first." />
      ) : null}

      {loading ? <LoadingState message="Loading tasks..." /> : null}
      {error ? <ErrorMessage message={error} /> : null}

      {studentId ? (
        <div className="space-y-6">
          <TaskForm studentId={studentId} onSubmit={handleCreateTask} />
          <TaskList tasks={tasks} onComplete={handleCompleteTask} onDelete={handleDeleteTask} />
        </div>
      ) : null}
    </section>
  );
}
