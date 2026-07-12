import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

export default function StatCard({ label, value, icon: Icon, trend, tone = 'default', onClick }) {
  const isPositive = typeof trend === 'number' && trend >= 0;
  const isNegative = typeof trend === 'number' && trend < 0;

  const toneStyles = {
    default: 'bg-brand-50 text-brand-600',
    warning: 'bg-amber-50 text-status-reserved',
    danger: 'bg-red-50 text-status-lost',
  };

  return (
    <div
      onClick={onClick}
      className={`card p-4 lg:p-5 flex flex-col gap-3 ${
        onClick ? 'cursor-pointer hover:shadow-popover transition-shadow' : ''
      }`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-ink-muted uppercase tracking-wide">
          {label}
        </span>
        {Icon && (
          <div className={`h-8 w-8 rounded-md flex items-center justify-center ${toneStyles[tone]}`}>
            <Icon size={16} strokeWidth={2.25} />
          </div>
        )}
      </div>

      <div className="flex items-end justify-between">
        <span className="text-2xl font-display font-semibold text-ink">{value}</span>
        {typeof trend === 'number' && trend !== 0 && (
          <span
            className={`flex items-center gap-0.5 text-xs font-medium ${
              isPositive ? 'text-status-available' : 'text-status-lost'
            }`}
          >
            {isPositive ? <ArrowUpRight size={13} /> : <ArrowDownRight size={13} />}
            {Math.abs(trend)}%
          </span>
        )}
      </div>
    </div>
  );
}
