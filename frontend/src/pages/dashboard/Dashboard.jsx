import { useEffect, useState } from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import {
  Boxes,
  UserCheck,
  Wrench,
  CalendarClock,
  ArrowLeftRight,
  Clock,
  PackagePlus,
  CalendarPlus,
  AlertTriangle,
} from 'lucide-react';
import PageHeader from '../../components/common/PageHeader.jsx';
import StatCard from '../../components/common/StatCard.jsx';
import DataTable from '../../components/common/DataTable.jsx';
import Spinner from '../../components/common/Spinner.jsx';
import useAuth from '../../hooks/useAuth.js';
import { getDashboardSummary } from '../../services/dashboardService.js';

const STATUS_COLORS = {
  Available: '#1F9E77',
  Allocated: '#3E6FD9',
  Reserved: '#D98E04',
  'Under Maintenance': '#B45FBE',
  Lost: '#DC4C4C',
  Retired: '#6B7280',
};

const QUICK_ACTION_ICONS = {
  'package-plus': PackagePlus,
  'calendar-plus': CalendarPlus,
  wrench: Wrench,
};

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    getDashboardSummary()
      .then((res) => isMounted && setData(res))
      .finally(() => isMounted && setIsLoading(false));
    return () => {
      isMounted = false;
    };
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-24">
        <Spinner size="lg" />
      </div>
    );
  }

  const kpis = data?.kpis || {};
  const trends = data?.kpiTrends || {};

  const kpiCards = [
    { key: 'assetsAvailable', label: 'Assets Available', icon: Boxes, tone: 'default' },
    { key: 'assetsAllocated', label: 'Assets Allocated', icon: UserCheck, tone: 'default' },
    { key: 'maintenanceToday', label: 'Maintenance Today', icon: Wrench, tone: 'warning' },
    { key: 'activeBookings', label: 'Active Bookings', icon: CalendarClock, tone: 'default' },
    { key: 'pendingTransfers', label: 'Pending Transfers', icon: ArrowLeftRight, tone: 'warning' },
    { key: 'upcomingReturns', label: 'Upcoming Returns', icon: Clock, tone: 'default' },
  ];

  return (
    <div>
      <PageHeader
        title={`Welcome back, ${user?.name?.split(' ')[0] || 'there'}`}
        subtitle="Here's what's happening across your organization today."
      />

      {/* KPI cards */}
      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3 lg:gap-4 mb-6">
        {kpiCards.map((card) => (
          <StatCard
            key={card.key}
            label={card.label}
            value={kpis[card.key] ?? '—'}
            icon={card.icon}
            tone={card.tone}
            trend={trends[card.key]}
          />
        ))}
      </div>

      {/* Quick actions */}
      <div className="card p-4 mb-6 flex flex-col sm:flex-row sm:items-center gap-3">
        <span className="text-sm font-medium text-ink shrink-0">Quick actions</span>
        <div className="flex flex-wrap gap-2">
          {(data?.quickActions || []).map((action) => {
            const Icon = QUICK_ACTION_ICONS[action.icon] || PackagePlus;
            return (
              <button key={action.id} className="btn-secondary">
                <Icon size={15} />
                {action.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Charts row */}
      <div className="grid lg:grid-cols-3 gap-4 mb-6">
        <div className="card p-5 lg:col-span-2">
          <h3 className="text-sm font-semibold text-ink mb-4">Allocation vs. Availability Trend</h3>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={data?.utilizationTrend || []}>
              <defs>
                <linearGradient id="allocatedFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#3E6FD9" stopOpacity={0.25} />
                  <stop offset="100%" stopColor="#3E6FD9" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="availableFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#1F9E77" stopOpacity={0.25} />
                  <stop offset="100%" stopColor="#1F9E77" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#E4E6EB" vertical={false} />
              <XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} />
              <YAxis tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} width={32} />
              <Tooltip
                contentStyle={{ borderRadius: 8, border: '1px solid #E4E6EB', fontSize: 13 }}
              />
              <Area type="monotone" dataKey="allocated" stroke="#3E6FD9" fill="url(#allocatedFill)" strokeWidth={2} name="Allocated" />
              <Area type="monotone" dataKey="available" stroke="#1F9E77" fill="url(#availableFill)" strokeWidth={2} name="Available" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-5">
          <h3 className="text-sm font-semibold text-ink mb-4">Asset Status Breakdown</h3>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={data?.assetStatusBreakdown || []}
                dataKey="count"
                nameKey="status"
                innerRadius={55}
                outerRadius={85}
                paddingAngle={2}
              >
                {(data?.assetStatusBreakdown || []).map((entry) => (
                  <Cell key={entry.status} fill={STATUS_COLORS[entry.status] || '#9CA3AF'} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ borderRadius: 8, border: '1px solid #E4E6EB', fontSize: 13 }} />
              <Legend
                verticalAlign="bottom"
                height={48}
                iconType="circle"
                iconSize={8}
                formatter={(value) => <span className="text-xs text-ink-muted">{value}</span>}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Returns + activity */}
      <div className="grid lg:grid-cols-3 gap-4">
        <div className="card p-5 lg:col-span-2">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle size={16} className="text-status-lost" />
            <h3 className="text-sm font-semibold text-ink">Overdue Returns</h3>
          </div>
          <DataTable
            columns={[
              { key: 'id', header: 'Tag' },
              { key: 'assetName', header: 'Asset' },
              { key: 'holder', header: 'Held By' },
              { key: 'department', header: 'Department' },
              {
                key: 'daysOverdue',
                header: 'Overdue',
                render: (row) => (
                  <span className="text-status-lost font-medium">{row.daysOverdue}d</span>
                ),
              },
            ]}
            rows={data?.overdueReturns || []}
            emptyTitle="No overdue returns"
            emptyDescription="Everything currently allocated is within its expected return window."
          />
        </div>

        <div className="card p-5">
          <h3 className="text-sm font-semibold text-ink mb-4">Recent Activity</h3>
          <ul className="space-y-4">
            {(data?.recentActivity || []).map((item) => (
              <li key={item.id} className="flex gap-3">
                <div className="h-1.5 w-1.5 rounded-full bg-brand-400 mt-2 shrink-0" />
                <div>
                  <p className="text-sm text-ink leading-snug">{item.message}</p>
                  <p className="text-xs text-ink-soft mt-0.5">
                    {item.actor} &middot; {item.time}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
