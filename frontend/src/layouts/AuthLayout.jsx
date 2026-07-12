import { Outlet } from 'react-router-dom';
import { Boxes } from 'lucide-react';

export default function AuthLayout() {
  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-surface">
      {/* Brand / context panel */}
      <div className="hidden lg:flex flex-col justify-between bg-brand-700 text-white px-14 py-12 relative overflow-hidden">
        <div className="absolute -right-24 -top-24 h-96 w-96 rounded-full bg-white/5" />
        <div className="absolute -left-10 bottom-0 h-64 w-64 rounded-full bg-white/5" />

        <div className="flex items-center gap-2.5 relative">
          <div className="h-9 w-9 rounded-md bg-white/10 flex items-center justify-center">
            <Boxes size={20} />
          </div>
          <span className="font-display font-semibold text-xl">AssetFlow</span>
        </div>

        <div className="relative max-w-md">
          <h1 className="font-display text-3xl font-semibold leading-tight mb-4">
            One system of record for every asset your organization owns.
          </h1>
          <p className="text-white/70 text-sm leading-relaxed">
            Track lifecycles, allocate with confidence, book shared resources without
            conflicts, and close every audit cycle with a clean paper trail.
          </p>
        </div>

        <p className="relative text-xs text-white/40">
          &copy; 2026 AssetFlow. Built for the hackathon.
        </p>
      </div>

      {/* Form panel */}
      <div className="flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-sm">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
