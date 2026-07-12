import { Routes, Route, Navigate } from 'react-router-dom';
import AuthLayout from '../layouts/AuthLayout.jsx';
import MainLayout from '../layouts/MainLayout.jsx';
import ProtectedRoute from './ProtectedRoute.jsx';

import Login from '../pages/auth/Login.jsx';
import Dashboard from '../pages/dashboard/Dashboard.jsx';

// Screens below are scaffolded incrementally, one at a time, into
// pages/<domain>/<Screen>.jsx following the same pattern as Dashboard.
// Uncomment + wire each route below as it's built:
//
// import Employees from '../pages/organization/Employees.jsx';
// import Departments from '../pages/organization/Departments.jsx';
// import AssetCategories from '../pages/organization/AssetCategories.jsx';
// import Assets from '../pages/assets/Assets.jsx';
// import AssetDetails from '../pages/assets/AssetDetails.jsx';
// import Allocation from '../pages/allocation/Allocation.jsx';
// import Booking from '../pages/booking/Booking.jsx';
// import Maintenance from '../pages/maintenance/Maintenance.jsx';
// import Audits from '../pages/audits/Audits.jsx';
// import Reports from '../pages/reports/Reports.jsx';
// import Notifications from '../pages/notifications/Notifications.jsx';

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />

          {/* <Route path="/organization" element={<Employees />} /> */}
          {/* <Route path="/assets" element={<Assets />} /> */}
          {/* <Route path="/assets/:id" element={<AssetDetails />} /> */}
          {/* <Route path="/allocation" element={<Allocation />} /> */}
          {/* <Route path="/booking" element={<Booking />} /> */}
          {/* <Route path="/maintenance" element={<Maintenance />} /> */}
          {/* <Route path="/audits" element={<Audits />} /> */}
          {/* <Route path="/reports" element={<Reports />} /> */}
          {/* <Route path="/notifications" element={<Notifications />} /> */}
        </Route>
      </Route>

      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
