import {
  DashboardStats,
  Exam,
  ExamCreateInput,
  ExamUpdateInput,
  Notification,
  ScheduleGenerateResponse,
  Student,
  StudentCreateInput,
  StudySession,
  Task,
  TaskCreateInput,
  TaskStatus,
  TaskUpdateInput,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(
  path: string, options: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
      cache: "no-store",
    });
  } catch {
    throw new ApiError(
      `Cannot reach backend at ${API_BASE_URL}. Make sure FastAPI is running and CORS allows this frontend origin.`,
      0,
    );
  }

  if (!response.ok) {
    let detail = "Request failed";
    try {
      const data = await response.json();
      detail = data.detail ?? JSON.stringify(data);
    } catch {
      detail = await response.text();
    }
    throw new ApiError(detail, response.status);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json() as Promise<T>;
}

export const studentsApi = {
  createStudent: (payload: StudentCreateInput) => request<Student>("/students", {
    method: "POST",
    body: JSON.stringify(payload),
  }),
  getStudents: () => request<Student[]>("/students"),
  getStudent: (studentId: number) => request<Student>(`/students/${studentId}`),
  updateStudent: (studentId: number, payload: Partial<StudentCreateInput>) =>
    request<Student>(`/students/${studentId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),
  deleteStudent: (studentId: number) =>
    request<{ message: string }>(`/students/${studentId}`, { method: "DELETE" }),
};

export const tasksApi = {
  createTask: (payload: TaskCreateInput) => request<Task>("/tasks", {
    method: "POST",
    body: JSON.stringify(payload),
  }),
  getTasksByStudent: (studentId: number) => request<Task[]>(`/tasks/student/${studentId}`),
  getTask: (taskId: number) => request<Task>(`/tasks/${taskId}`),
  updateTask: (taskId: number, payload: TaskUpdateInput) => request<Task>(`/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  }),
  updateTaskStatus: (taskId: number, status: TaskStatus) => request<Task>(`/tasks/${taskId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  }),
  deleteTask: (taskId: number) => request<{ message: string }>(`/tasks/${taskId}`, { method: "DELETE" }),
};

export const examsApi = {
  createExam: (payload: ExamCreateInput) => request<Exam>("/exams", {
    method: "POST",
    body: JSON.stringify(payload),
  }),
  getExamsByStudent: (studentId: number) => request<Exam[]>(`/exams/student/${studentId}`),
  getExam: (examId: number) => request<Exam>(`/exams/${examId}`),
  updateExam: (examId: number, payload: ExamUpdateInput) => request<Exam>(`/exams/${examId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  }),
  deleteExam: (examId: number) => request<{ message: string }>(`/exams/${examId}`, { method: "DELETE" }),
};

export const schedulesApi = {
  generateSchedule: (studentId: number) => request<ScheduleGenerateResponse>(`/schedules/generate/${studentId}`, {
    method: "POST",
  }),
  getScheduleByStudent: (studentId: number) => request<StudySession[]>(`/schedules/student/${studentId}`),
  completeSession: (sessionId: number) => request<StudySession>(`/schedules/${sessionId}/complete`, { method: "PATCH" }),
  deleteSchedule: (studentId: number) =>
    request<{ message: string }>(`/schedules/student/${studentId}`, { method: "DELETE" }),
};

export const notificationsApi = {
  getNotifications: (studentId: number) => request<Notification[]>(`/notifications/student/${studentId}`),
};

export const analyticsApi = {
  getDashboardStats: (studentId: number) => request<DashboardStats>(`/analytics/dashboard/${studentId}`),
};

export { ApiError };
