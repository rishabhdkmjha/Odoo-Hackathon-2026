import { NavLink } from 'react-router-dom';
import {
  LayoutGrid,
  Building2,
  Boxes,
  PackageSearch,
  ArrowLeftRight,
  CalendarClock,
  Wrench,
  ClipboardCheck,
  BarChart3,
  Bell,
  X,
} from 'lucide-react';

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutGrid },
  { to: '/organization', label: 'Organization Setup', icon: Building2, adminOnly: true },
  { to: '/assets', label: 'Assets', icon: Boxes },
  { to: '/allocation', label: 'Allocation & Transfer', icon: ArrowLeftRight },
  { to: '/booking', label: 'Resource Booking', icon: CalendarClock },
  { to: '/maintenance', label: 'Maintenance', icon: Wrench },
  { to: '/audits', label: 'Asset Audits', icon: ClipboardCheck },
  { to: '/reports', label: 'Reports & Analytics', icon: BarChart3 },
  { to: '/notifications', label: 'Notifications', icon: Bell },
];

export default function Sidebar({ role = 'employee', open, onClose }) {
  const items = NAV_ITEMS.filter((item) => !item.adminOnly || role === 'admin');

  return (
    <>
      {/* Mobile overlay */}
      {open && (
        <div
          className="fixed inset-0 z-30 bg-ink/30 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed z-40 inset-y-0 left-0 w-64 bg-brand-700 text-white flex flex-col
        transform transition-transform duration-200 lg:static lg:translate-x-0
        ${open ? 'translate-x-0' : '-translate-x-full'}`}
      >
        <div className="flex items-center justify-between px-5 h-16 border-b border-white/10">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-md bg-white/10 flex items-center justify-center">
              <Boxes className="h-4.5 w-4.5" size={18} />
            </div>
            <span className="font-display font-semibold text-lg tracking-tight">
              AssetFlow
            </span>
          </div>
          <button
            onClick={onClose}
            className="lg:hidden text-white/70 hover:text-white"
            aria-label="Close menu"
          >
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-0.5">
          {items.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors
                ${
                  isActive
                    ? 'bg-white/12 text-white'
                    : 'text-white/65 hover:bg-white/8 hover:text-white'
                }`
              }
            >
              <Icon size={18} strokeWidth={2} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="px-5 py-4 border-t border-white/10 text-xs text-white/40">
          AssetFlow ERP &middot; v0.1 (Hackathon Build)
        </div>
      </aside>
    </>
  );
}
