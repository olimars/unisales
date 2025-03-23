import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from '@/pages/Dashboard';
import Contacts from '@/pages/Contacts';
import Sales from '@/pages/Sales';
import Marketing from '@/pages/Marketing';
import Support from '@/pages/Support';
import Reports from '@/pages/Reports';
import Settings from '@/pages/Settings';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/contacts" element={<Contacts />} />
      <Route path="/sales" element={<Sales />} />
      <Route path="/marketing" element={<Marketing />} />
      <Route path="/support" element={<Support />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;