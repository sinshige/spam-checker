"use client";

import { useState, type FormEvent } from "react";

type SpamCheckResponse = {
  is_spam: boolean;
  score: number;
  reason: string;
};

export default function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<SpamCheckResponse | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!text.trim()) {
      setError("判定する文章を入力してください。");
      setResult(null);
      return;
    }

    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/spam-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`APIエラーが発生しました（${response.status}）。`);
      }

      const data: SpamCheckResponse = await response.json();
      setResult(data);
    } catch (caughtError) {
      setError(
        caughtError instanceof TypeError
          ? "APIに接続できませんでした。FastAPIが起動しているか確認してください。"
          : caughtError instanceof Error
            ? caughtError.message
            : "予期しないエラーが発生しました。",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-12 text-slate-900 sm:px-6 sm:py-20">
      <div className="mx-auto max-w-2xl">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Spam Checker
          </h1>
          <p className="mt-3 text-slate-600">
            文章を入力して、スパムの可能性をチェックしましょう。
          </p>
        </header>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-8">
          <form onSubmit={handleSubmit}>
            <label
              htmlFor="text"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              判定する文章
            </label>
            <textarea
              id="text"
              value={text}
              onChange={(event) => setText(event.target.value)}
              placeholder="チェックしたい文章を入力してください..."
              rows={8}
              className="w-full resize-y rounded-xl border border-slate-300 bg-white px-4 py-3 text-base leading-7 outline-none transition placeholder:text-slate-400 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100"
              aria-describedby={error ? "form-error" : undefined}
            />
            <div className="mt-3 flex items-center justify-between gap-4">
              <span className="text-sm text-slate-500">
                {text.length.toLocaleString()} 文字
              </span>
              <button
                type="submit"
                disabled={isLoading}
                className="rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-indigo-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:cursor-wait disabled:opacity-60"
              >
                {isLoading ? "判定中..." : "判定する"}
              </button>
            </div>
          </form>
        </section>

        {error && (
          <p
            id="form-error"
            role="alert"
            className="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
          >
            {error}
          </p>
        )}

        {result && (
          <section
            aria-live="polite"
            className={`mt-6 rounded-2xl border p-5 shadow-sm sm:p-8 ${
              result.is_spam
                ? "border-amber-200 bg-amber-50"
                : "border-emerald-200 bg-emerald-50"
            }`}
          >
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-slate-600">判定結果</p>
                <h2
                  className={`mt-1 text-2xl font-bold ${
                    result.is_spam ? "text-amber-800" : "text-emerald-800"
                  }`}
                >
                  {result.is_spam ? "スパムの可能性があります" : "問題ありません"}
                </h2>
              </div>
              <div className="rounded-xl bg-white/80 px-4 py-2 text-right">
                <p className="text-xs font-medium text-slate-500">スコア</p>
                <p className="text-2xl font-bold tabular-nums text-slate-900">
                  {result.score}
                  <span className="ml-1 text-sm font-medium text-slate-500">
                    / 100
                  </span>
                </p>
              </div>
            </div>
            <div className="mt-5 border-t border-slate-900/10 pt-4">
              <p className="text-sm font-semibold text-slate-700">理由</p>
              <p className="mt-1 text-slate-700">{result.reason}</p>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
