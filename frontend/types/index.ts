export type TaskStatus = "pending" | "in_progress" | "completed" | "cancelled";
export type SessionType = "task" | "exam_revision" | "general";

export interface Student {
  id: number;
  name: string;
  email: string;
  study_hours_per_day: number;
  preferred_start_time: string;
  preferred_end_time: string;
  created_at: string;
  updated_at: string;
}

export interface StudentCreateInput {
  name: string;
  email: string;
  study_hours_per_day: number;
  preferred_start_time?: string;
  preferred_end_time?: string;
}

export interface Task {
  id: number;
  student_id: number;
  title: string;
  description?: string | null;
  course_name?: string | null;
  deadline: string;
  difficulty: number;
  estimated_hours: number;
  is_exam_related: boolean;
  status: TaskStatus;
  priority_score: number;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateInput {
  student_id: number;
  title: string;
  description?: string;
  course_name?: string;
  deadline: string;
  difficulty: number;
  estimated_hours: number;
  is_exam_related: boolean;
  status?: TaskStatus;
}

export interface TaskUpdateInput {
  title?: string;
  description?: string;
  course_name?: string;
  deadline?: string;
  difficulty?: number;
  estimated_hours?: number;
  is_exam_related?: boolean;
  status?: TaskStatus;
}

export interface Exam {
  id: number;
  student_id: number;
  subject: string;
  course_name?: string | null;
  exam_date: string;
  importance: number;
  estimated_revision_hours: number;
  created_at: string;
  updated_at: string;
}

export interface ExamCreateInput {
  student_id: number;
  subject: string;
  course_name?: string;
  exam_date: string;
  importance: number;
  estimated_revision_hours: number;
}

export interface ExamUpdateInput {
  subject?: string;
  course_name?: string;
  exam_date?: string;
  importance?: number;
  estimated_revision_hours?: number;
}

export interface StudySession {
  id: number;
  student_id: number;
  task_id?: number | null;
  session_date: string;
  title: string;
  duration_hours: number;
  priority_score: number;
  session_type: SessionType;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface ScheduleGenerateResponse {
  student_id: number;
  total_sessions: number;
  total_hours: number;
  warnings: string[];
  sessions: StudySession[];
}

export interface Notification {
  type:
    | "task_deadline"
    | "exam_reminder"
    | "high_priority_task"
    | "overdue_task"
    | "schedule_warning"
    | "study_session_today";
  message: string;
  severity: "high" | "medium" | "low";
  related_id?: number | null;
}

export interface DashboardStats {
  student_id: number;
  total_tasks: number;
  pending_tasks: number;
  completed_tasks: number;
  high_priority_tasks: number;
  upcoming_exams: number;
  generated_sessions: number;
  total_scheduled_hours: number;
  completion_rate: number;
}
