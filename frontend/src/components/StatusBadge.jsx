// Maps every lifecycle status string used across the app to a status-color token.
// Keep this the single source of truth so a status always looks the same everywhere.
const STATUS_MAP = {
  Available: 'available',
  Allocated: 'allocated',
  Reserved: 'reserved',
  'Under Maintenance': 'maintenance',
  Lost: 'lost',
  Retired: 'retired',
  Disposed: 'disposed',
  // Booking statuses
  Upcoming: 'allocated',
  Ongoing: 'reserved',
  Completed: 'retired',
  Cancelled: 'lost',
  // Maintenance / transfer / audit workflow statuses
  Pending: 'reserved',
  Approved: 'available',
  Rejected: 'lost',
  'Technician Assigned': 'allocated',
  'In Progress': 'maintenance',
  Resolved: 'available',
  Requested: 'reserved',
  'Re-allocated': 'allocated',
  Verified: 'available',
  Missing: 'lost',
  Damaged: 'maintenance',
};

const COLOR_CLASSES = {
  available: 'bg-emerald-50 text-status-available',
  allocated: 'bg-blue-50 text-status-allocated',
  reserved: 'bg-amber-50 text-status-reserved',
  maintenance: 'bg-fuchsia-50 text-status-maintenance',
  lost: 'bg-red-50 text-status-lost',
  retired: 'bg-gray-100 text-status-retired',
  disposed: 'bg-slate-100 text-status-disposed',
};

export default function StatusBadge({ status }) {
  const key = STATUS_MAP[status] || 'retired';
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${COLOR_CLASSES[key]}`}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {status}
    </span>
  );
}
