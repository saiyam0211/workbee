import React, { useState } from 'react';
import HomeIcon from '../icons/HomeIcon';
import DocumentsIcon from '../icons/DocumentsIcon';
import HeartIcon from '../icons/HeartIcon';
import BellIcon from '../icons/BellIcon';
import UserIcon from '../icons/UserIcon';

const navigationItems = [
  { id: 'home', icon: HomeIcon, label: 'Home' },
  { id: 'documents', icon: DocumentsIcon, label: 'Documents' },
  { id: 'favorites', icon: HeartIcon, label: 'Favorites' },
  { id: 'notifications', icon: BellIcon, label: 'Notifications' },
  { id: 'profile', icon: UserIcon, label: 'Profile' }
];

const FigmaFooterNav = ({ activeItem = 'home' }) => {
  const [activeId, setActiveId] = useState(activeItem);

  const handleItemClick = (id) => {
    setActiveId(id);
  };

  return (
    <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50">
      {/* Main Navigation Container */}
      <div 
        className="relative flex items-center gap-1 px-6 py-4 rounded-full"
        style={{
          backgroundColor: 'rgba(0, 0, 0, 0.20)',
          backdropFilter: 'blur(20px)',
          borderRadius: '296px'
        }}
      >
        {navigationItems.map((item, index) => {
          const Icon = item.icon;
          const isActive = activeId === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => handleItemClick(item.id)}
              className={`
                relative flex flex-col items-center justify-center transition-all duration-300 ease-out
                ${isActive ? 'px-4 py-2' : 'p-3'}
              `}
            >
              {/* Active State Background with Glass Effect */}
              {isActive && (
                <div 
                  className="absolute inset-0 rounded-full"
                  style={{
                    border: '1.5px solid #9d90e1',
                    borderRadius: '1000px'
                  }}
                />
              )}
              
              {/* Icon */}
              <div className="relative z-10 mb-1">
                <Icon 
                  width={isActive ? 39 : 35} 
                  height={isActive ? 43 : 35}
                  color={isActive ? '#9d90e1' : '#ffffff'}
                  style={{
                    border: isActive ? '1.5px solid #9d90e1' : '1.5px solid #ffffff',
                    borderRadius: '8px',
                    padding: '2px'
                  }}
                />
              </div>
              
              {/* Label and Underline for Active State */}
              {isActive && (
                <div className="relative z-10 flex flex-col items-center">
                  <span 
                    className="text-center leading-tight mb-1"
                    style={{
                      fontFamily: 'SF Pro, -apple-system, system-ui, BlinkMacSystemFont, sans-serif',
                      fontSize: '32px',
                      fontWeight: '400',
                      color: '#9d90e1'
                    }}
                  >
                    {item.label}
                  </span>
                  {/* Underline */}
                  <div 
                    className="w-full h-0.5 rounded-full"
                    style={{
                      backgroundColor: '#9d90e1',
                      width: '77px',
                      height: '3px'
                    }}
                  />
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default FigmaFooterNav;