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

const NavigationItem = ({ item, isActive, onClick }) => {
  const Icon = item.icon;
  
  return (
    <button
      onClick={() => onClick(item.id)}
      className={`
        relative flex flex-col items-center justify-center transition-all duration-500 ease-out
        ${isActive ? 'px-6 py-4' : 'px-4 py-3'}
        hover:scale-105 active:scale-95
        group
      `}
    >
      {/* Active State Background with Enhanced Glass Effect */}
      <div 
        className={`
          absolute inset-0 rounded-full transition-all duration-500 ease-out
          ${isActive 
            ? 'bg-gradient-to-br from-purple-500/20 via-blue-500/15 to-purple-600/20 border-2 border-purple-400/60 shadow-lg shadow-purple-500/25' 
            : 'bg-transparent border-2 border-transparent group-hover:border-white/20 group-hover:bg-white/5'
          }
        `}
        style={{
          backdropFilter: isActive ? 'blur(10px)' : 'blur(0px)',
        }}
      />
      
      {/* Glow Effect for Active State */}
      {isActive && (
        <div 
          className="absolute inset-0 rounded-full bg-gradient-to-br from-purple-400/30 to-blue-500/30 blur-md -z-10"
          style={{ transform: 'scale(1.1)' }}
        />
      )}
      
      {/* Icon Container */}
      <div className="relative z-10 mb-2">
        <div className={`
          p-2 rounded-xl transition-all duration-300
          ${isActive 
            ? 'bg-gradient-to-br from-purple-500/30 to-blue-500/30 shadow-inner' 
            : 'group-hover:bg-white/10'
          }
        `}>
          <Icon 
            width={24} 
            height={24}
            className={`
              transition-all duration-300
              ${isActive 
                ? 'text-purple-300 drop-shadow-lg' 
                : 'text-white/80 group-hover:text-white'
              }
            `}
            style={{
              filter: isActive ? 'drop-shadow(0 0 8px rgba(157, 144, 225, 0.5))' : 'none'
            }}
          />
        </div>
      </div>
      
      {/* Label */}
      <span 
        className={`
          text-xs font-medium transition-all duration-300 text-center
          ${isActive 
            ? 'text-purple-300 opacity-100 transform translate-y-0' 
            : 'text-white/60 opacity-0 transform translate-y-2 group-hover:opacity-80 group-hover:translate-y-0'
          }
        `}
        style={{
          fontFamily: 'SF Pro, -apple-system, system-ui, BlinkMacSystemFont, sans-serif',
          textShadow: isActive ? '0 0 10px rgba(157, 144, 225, 0.5)' : 'none'
        }}
      >
        {item.label}
      </span>
      
      {/* Active Indicator Dot */}
      {isActive && (
        <div 
          className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-purple-400 rounded-full"
          style={{
            boxShadow: '0 0 8px rgba(157, 144, 225, 0.8)'
          }}
        />
      )}
    </button>
  );
};

const BeautifulFooterNav = ({ activeItem = 'home' }) => {
  const [activeId, setActiveId] = useState(activeItem);
  const [hoveredId, setHoveredId] = useState(null);

  const handleItemClick = (id) => {
    setActiveId(id);
  };

  return (
    <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50">
      {/* Main Navigation Container */}
      <div 
        className="relative flex items-center gap-2 px-4 py-3 rounded-full backdrop-blur-xl border border-white/10 shadow-2xl"
        style={{
          background: 'linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(20, 20, 30, 0.9) 50%, rgba(0, 0, 0, 0.8) 100%)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.05)'
        }}
        onMouseLeave={() => setHoveredId(null)}
      >
        {/* Background Glow */}
        <div 
          className="absolute inset-0 rounded-full opacity-50"
          style={{
            background: 'radial-gradient(ellipse at center, rgba(157, 144, 225, 0.1) 0%, transparent 70%)',
          }}
        />
        
        {navigationItems.map((item, index) => (
          <div
            key={item.id}
            onMouseEnter={() => setHoveredId(item.id)}
          >
            <NavigationItem
              item={item}
              isActive={activeId === item.id}
              onClick={handleItemClick}
            />
          </div>
        ))}
      </div>
      
      {/* Floating Label for Hovered Item */}
      {hoveredId && hoveredId !== activeId && (
        <div 
          className="absolute -top-12 left-1/2 transform -translate-x-1/2 px-3 py-1 bg-black/80 backdrop-blur-sm rounded-lg border border-white/20 shadow-lg"
          style={{
            animation: 'fadeInUp 0.2s ease-out'
          }}
        >
          <span className="text-white text-sm font-medium">
            {navigationItems.find(item => item.id === hoveredId)?.label}
          </span>
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-black/80" />
        </div>
      )}
    </div>
  );
};

export default BeautifulFooterNav;