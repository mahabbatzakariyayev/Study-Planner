"use client";

import { useEffect, useState } from "react";

import ErrorMessage from "@/components/ErrorMessage";
import LoadingState from "@/components/LoadingState";
import NotificationList from "@/components/NotificationList";
import PageHeader from "@/components/PageHeader";
import { notificationsApi } from "@/lib/api";
import { Notification } from "@/types";

const ACTIVE_STUDENT_KEY = "activeStudentId";

export default function NotificationsPage() {
  const [studentId, setStudentId] = useState<number | null>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadNotifications() {
      const stored = Number(localStorage.getItem(ACTIVE_STUDENT_KEY));
      if (!stored) {
        setLoading(false);
        return;
      }

      setStudentId(stored);
      setLoading(true);
      setError(null);
      try {
        const data = await notificationsApi.getNotifications(stored);
        setNotifications(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load notifications");
      } finally {
        setLoading(false);
      }
    }

    loadNotifications();
  }, []);

  return (
    <section className="space-y-6">
      <PageHeader
        title="Notifications"
        description="Reminder stream generated from backend rules for deadlines, exams, and schedule context."
      />

      {!studentId ? <ErrorMessage message="No active student found. Please select a student first." /> : null}
      {loading ? <LoadingState message="Loading notifications..." /> : null}
      {error ? <ErrorMessage message={error} /> : null}
      {studentId ? <NotificationList notifications={notifications} /> : null}
    </section>
  );
}
