interface LoadingStateProps {
  message?: string;
}

export default function LoadingState({ message = "Loading..." }: LoadingStateProps) {
  return <p className="rounded-lg bg-slate-100 px-4 py-3 text-sm text-slate-700">{message}</p>;
}
