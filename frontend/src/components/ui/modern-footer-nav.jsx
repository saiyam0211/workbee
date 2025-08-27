import React, { useState } from 'react';
import { House, Briefcase, CalendarDays, ShieldCheck, Settings, FileText, Heart, Bell, User } from 'lucide-react';

// Navigation items for the first design (Strategy focused)
const strategyNavItems = [
  { id: 'home', icon: House, label: 'Home' },
  { id: 'strategy', icon: Briefcase, label: 'Strategy' },
  { id: 'calendar', icon: CalendarDays, label: 'Calendar' },
  { id: 'security', icon: ShieldCheck, label: 'Security' },
  { id: 'settings', icon: Settings, label: 'Settings' }
];

// Navigation items for the second design (Home focused)
const homeNavItems = [
  { id: 'home', icon: House, label: 'Home' },
  { id: 'documents', icon: FileText, label: 'Documents' },
  { id: 'favorites', icon: Heart, label: 'Favorites' },
  { id: 'notifications', icon: Bell, label: 'Notifications' },
  { id: 'profile', icon: User, label: 'Profile' }
];

const ModernFooterNav = ({ variant = 'strategy', activeItem = null }) => {
  const navItems = variant === 'strategy' ? strategyNavItems : homeNavItems;
  const defaultActive = variant === 'strategy' ? 'strategy' : 'home';
  const [activeId, setActiveId] = useState(activeItem || defaultActive);

  const handleItemClick = (id) => {
    setActiveId(id);
  };

  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50">
      <nav className="bg-gray-900/95 backdrop-blur-sm border border-gray-700/50 rounded-full px-6 py-3 shadow-2xl">
        <div className="flex items-center justify-center gap-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeId === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => handleItemClick(item.id)}
                className={`
                  relative flex flex-col items-center justify-center p-3 rounded-2xl transition-all duration-300 ease-out
                  ${isActive 
                    ? 'bg-gradient-to-br from-purple-500/20 to-blue-500/20 border border-purple-400/30' 
                    : 'hover:bg-gray-800/50'
                  }
                  min-w-[60px] min-h-[60px]
                `}
              >
                {/* Active state background glow */}
                {isActive && (
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-blue-500/10 rounded-2xl blur-sm" />
                )}
                
                {/* Icon */}
                <div className="relative z-10">
                  <Icon 
                    size={24} 
                    className={`
                      transition-all duration-300
                      ${isActive 
                        ? 'text-purple-400 drop-shadow-lg' 
                        : 'text-gray-400 hover:text-gray-300'
                      }
                    `}
                  />
                </div>
                
                {/* Label */}
                {isActive && (
                  <span className="relative z-10 text-xs font-medium text-purple-300 mt-1 opacity-90">
                    {item.label}
                  </span>
                )}
                
                {/* Active indicator border */}
                {isActive && (
                  <div className="absolute inset-0 rounded-2xl border-2 border-purple-400/40 shadow-lg shadow-purple-500/20" />
                )}
              </button>
            );
          })}
        </div>
      </nav>
    </div>
  );
};

export default ModernFooterNav;