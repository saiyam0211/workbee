import React from 'react';
import { Home, Search, FileText, Bell, User, Heart } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const GlassFooter = ({ activeTab, setActiveTab, onJobSelect }) => {
  const navigate = useNavigate();
  
  const navigationItems = [
    { id: 'home', icon: Home, label: 'Home' },
    { id: 'search', icon: Search, label: 'Search' },
    { id: 'saved', icon: Heart, label: 'Favourites' },
    // { id: 'profile', icon: User, label: 'Profile' }
  ];

  return (
    <div id="bottom-navigation" className="fixed bottom-10  inset-x-0 md:inset-x-auto md:left-1/2 md:-translate-x-1/2 md:bottom-6 z-50 px-3 md:px-0 pb-[max(env(safe-area-inset-bottom),0.5rem)] sm:pb-6">
      <div className="glass-footer-container mx-auto md:mx-0 max-w-md">
        <div className="glass-footer-background"></div>
        <div className="grid grid-cols-3 items-center px-4 sm:px-8 py-2 sm:py-4 gap-6 sm:gap-12">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            
            return (
              <button
                key={item.id}
                id={`nav-${item.id}`}
                onClick={() => {
                  setActiveTab(item.id);
                  if (item.id === 'home') {
                    navigate('/dashboard');
                  }
                  if (item.id === 'saved') navigate('/fav-companies');
                  if (item.id === 'search') navigate('/search');
                  // if (item.id === 'profile') navigate('/profile');
                }}
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