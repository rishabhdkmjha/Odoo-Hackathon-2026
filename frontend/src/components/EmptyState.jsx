export default function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-14 px-6">
      {Icon && (
        <div className="h-12 w-12 rounded-full bg-surface-muted flex items-center justify-center mb-4">
          <Icon size={22} className="text-ink-soft" />
        </div>
      )}
      <p className="text-sm font-medium text-ink">{title}</p>
      {description && <p className="text-sm text-ink-muted mt-1 max-w-sm">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
