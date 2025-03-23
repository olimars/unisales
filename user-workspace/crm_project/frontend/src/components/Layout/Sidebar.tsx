import { NavLink } from 'react-router-dom';
import {
  Dashboard as DashboardIcon,
  People as ContactsIcon,
  ShoppingCart as SalesIcon,
  Campaign as MarketingIcon,
  Support as SupportIcon,
  Assessment as ReportsIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

const menuItems = [
  { path: '/', icon: DashboardIcon, label: 'Dashboard' },
  { path: '/contacts', icon: ContactsIcon, label: 'Contacts' },
  { path: '/sales', icon: SalesIcon, label: 'Sales' },
  { path: '/marketing', icon: MarketingIcon, label: 'Marketing' },
  { path: '/support', icon: SupportIcon, label: 'Support' },
  { path: '/reports', icon: ReportsIcon, label: 'Reports' },
  { path: '/settings', icon: SettingsIcon, label: 'Settings' },
];

const Sidebar = () => {
  return (
    <aside className="hidden lg:flex lg:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col h-0 flex-1 bg-gray-800">
          <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div className="flex items-center flex-shrink-0 px-4">
              <h1 className="text-2xl font-bold text-white">CRM System</h1>
            </div>
            <nav className="mt-8 flex-1 px-2 space-y-1">
              {menuItems.map(({ path, icon: Icon, label }) => (
                <NavLink
                  key={path}
                  to={path}
                  className={({ isActive }) =>
                    `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'bg-gray-900 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`
                  }
                >
                  <Icon className="mr-3 h-6 w-6" />
                  {label}
                </NavLink>
              ))}
            </nav>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;