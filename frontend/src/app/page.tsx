export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900">
      <div className="text-center space-y-6 px-8">
        {/* Logo mark */}
        <div className="flex items-center justify-center mb-2">
          <span className="text-7xl font-black tracking-tight bg-gradient-to-r from-indigo-400 via-violet-400 to-emerald-400 bg-clip-text text-transparent select-none">
            Recovr
          </span>
        </div>

        {/* Tagline */}
        <p className="text-slate-400 text-lg font-medium tracking-wide">
          AI-powered revenue recovery for UPI Autopay &amp; card subscriptions
        </p>

        {/* Badge */}
        <div className="inline-flex items-center gap-2 bg-indigo-900/40 border border-indigo-700/50 rounded-full px-4 py-1.5 text-indigo-300 text-sm font-medium">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Razorpay AI Buildathon 2026 — Track 03
        </div>
      </div>
    </main>
  );
}
