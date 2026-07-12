import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, Search, Bell, ChevronDown, LogOut, Settings } from 'lucide-react';
import useAuth from '../../hooks/useAuth.js';

const ROLE_LABELS = {
  admin: 'Administrator',
  asset_manager: 'Asset Manager',
  department_head: 'Department Head',
  employee: 'Employee',
};

export default function Navbar({ onMenuClick, notificationCount = 0 }) {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-20 h-16 bg-white border-b border-surface-border flex items-center gap-4 px-4 lg:px-6">
      <button
        onClick={onMenuClick}
        className="lg:hidden text-ink-muted hover:text-ink"
        aria-label="Open menu"
      >
        <Menu size={22} />
      </button>

      <div className="flex-1 max-w-md relative hidden sm:block">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-soft"
        />
        <input
          type="text"
          placeholder="Search assets, employees, bookings..."
          className="input pl-9 bg-surface-muted border-transparent focus:bg-white"
        />
      </div>

      <div className="flex-1 sm:hidden" />

      <button
        onClick={() => navigate('/notifications')}
        className="relative text-ink-muted hover:text-ink p-2 rounded-md hover:bg-surface-muted"
        aria-label="Notifications"
      >
        <Bell size={20} />
        {notificationCount > 0 && (
          <span className="absolute top-1 right-1 h-4 min-w-4 px-1 rounded-full bg-status-lost text-white text-[10px] font-semibold flex items-center justify-center">
            {notificationCount > 9 ? '9+' : notificationCount}
          </span>
        )}
      </button>

      <div className="relative">
        <button
          onClick={() => setMenuOpen((v) => !v)}
          className="flex items-center gap-2.5 pl-2 pr-1 py-1.5 rounded-md hover:bg-surface-muted"
        >
          <div className="h-8 w-8 rounded-full bg-brand-500 text-white text-xs font-semibold flex items-center justify-center">
            {user?.avatarInitials || 'U'}
          </div>
          <div className="hidden md:block text-left">
            <p className="text-sm font-medium text-ink leading-tight">{user?.name || 'User'}</p>
            <p className="text-xs text-ink-muted leading-tight">
              {ROLE_LABELS[user?.role] || 'Employee'}
            </p>
          </div>
          <ChevronDown size={16} className="text-ink-soft hidden md:block" />
        </button>

        {menuOpen && (
          <>
            <div className="fixed inset-0 z-10" onClick={() => setMenuOpen(false)} />
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-popover border border-surface-border z-20 py-1">
              <button className="w-full flex items-center gap-2 px-3.5 py-2 text-sm text-ink hover:bg-surface-muted text-left">
                <Settings size={15} /> Account Settings
              </button>
              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-2 px-3.5 py-2 text-sm text-status-lost hover:bg-surface-muted text-left"
              >
                <LogOut size={15} /> Log Out
              </button>
            </div>
          </>
        )}
      </div>
    </header>
  );
}
