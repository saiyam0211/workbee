import React from 'react';
import { Home, Search, FileText, Bell, User } from 'lucide-react';

const GlassFooter = ({ activeTab, setActiveTab }) => {
  const navigationItems = [
    { id: 'home', icon: Home, label: 'Home' },
    { id: 'search', icon: Search, label: 'Search' },
    { id: 'jobs', icon: FileText, label: 'Jobs' },
    { id: 'alerts', icon: Bell, label: 'Alerts', hasNotification: true },
    { id: 'profile', icon: User, label: 'Profile' }
  ];

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50">
      <div className="glass-footer-container">
        <div className="glass-footer-background"></div>
        <div className="flex items-center px-8 py-4 gap-12">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className="glass-nav-item flex flex-col items-center gap-1 group relative"
              >
                <div className="relative">
                  <Icon 
                    size={24} 
                    className={`transition-all duration-200 ${
                      isActive 
                        ? 'text-blue-400' 
                        : 'text-gray-300 group-hover:text-white'
                    }`} 
                  />
                  {item.hasNotification && (
                    <div className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                  )}
                </div>
                <span className={`text-xs font-medium transition-all duration-200 ${
                  isActive 
                    ? 'text-blue-400' 
                    : 'text-gray-300 group-hover:text-white'
                }`}>
                  {item.label}
                </span>
                {isActive && (
                  <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-1 h-1 bg-blue-400 rounded-full"></div>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default GlassFooter;