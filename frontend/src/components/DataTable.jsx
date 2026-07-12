import Spinner from './Spinner.jsx';
import EmptyState from './EmptyState.jsx';
import { Inbox } from 'lucide-react';

/**
 * Generic data table.
 *
 * columns: [{ key, header, render?: (row) => node, className? }]
 * rows: array of data objects
 * getRowKey: (row) => string | number
 */
export default function DataTable({
  columns,
  rows,
  getRowKey = (row) => row.id,
  isLoading = false,
  emptyTitle = 'No records found',
  emptyDescription = 'Try adjusting your filters or search terms.',
  onRowClick,
}) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!rows || rows.length === 0) {
    return <EmptyState icon={Inbox} title={emptyTitle} description={emptyDescription} />;
  }

  return (
    <div className="overflow-x-auto -mx-4 sm:mx-0">
      <table className="w-full text-sm min-w-[640px]">
        <thead>
          <tr className="border-b border-surface-border">
            {columns.map((col) => (
              <th
                key={col.key}
                className="text-left font-medium text-ink-muted text-xs uppercase tracking-wide px-4 py-3 whitespace-nowrap"
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr
              key={getRowKey(row)}
              onClick={onRowClick ? () => onRowClick(row) : undefined}
              className={`border-b border-surface-border last:border-0 ${
                onRowClick ? 'cursor-pointer hover:bg-surface-muted' : ''
              }`}
            >
              {columns.map((col) => (
                <td key={col.key} className={`px-4 py-3.5 text-ink align-middle ${col.className || ''}`}>
                  {col.render ? col.render(row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
