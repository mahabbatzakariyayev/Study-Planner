import { Notification } from "@/types";

interface NotificationListProps {
  notifications: Notification[];
}

const severityClasses: Record<Notification["severity"], string> = {
  high: "bg-rose-50 border-rose-300 text-rose-800",
  medium: "bg-amber-50 border-amber-300 text-amber-800",
  low: "bg-sky-50 border-sky-300 text-sky-800",
};

export default function NotificationList({ notifications }: NotificationListProps) {
  if (notifications.length === 0) {
    return (
      <p className="rounded-xl border border-dashed border-slate-300 p-6 text-sm text-slate-600">
        No notifications for this student.
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {notifications.map((item, index) => (
        <div key={`${item.type}-${item.related_id}-${index}`} className={`rounded-xl border p-4 ${severityClasses[item.severity]}`}>
          <p className="text-sm uppercase tracking-wide">{item.type.replaceAll("_", " ")}</p>
          <p className="mt-1 font-medium">{item.message}</p>
        </div>
      ))}
    </div>
  );
}
