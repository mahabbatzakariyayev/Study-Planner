# Frontend - AI Study Planner Client

This frontend is a Next.js App Router client for the AI Study Planner distributed system.

## Responsibilities
- Render pages and forms for students, tasks, exams, schedules, notifications, analytics
- Store active student id in localStorage
- Send HTTP JSON requests to backend API
- Display loading, error, empty states

The frontend does not access SQLite directly.

## Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:3000`

## Environment Variable
Create `.env.local` from `.env.local.example`:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Build
```bash
npm run build
npm run lint
```

## API Communication
All API calls are centralized in:
- `lib/api.ts`

Modules:
- `studentsApi`
- `tasksApi`
- `examsApi`
- `schedulesApi`
- `notificationsApi`
- `analyticsApi`

## UI Pages
- `/` dashboard
- `/students`
- `/tasks`
- `/exams`
- `/schedule`
- `/notifications`
- `/analytics`
