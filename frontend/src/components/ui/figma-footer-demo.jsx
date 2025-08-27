import React, { useState } from 'react';
import FigmaFooterNav from './figma-footer-nav';

const FigmaFooterDemo = () => {
  const [activeItem, setActiveItem] = useState('home');

  const navigationItems = [
    { id: 'home', label: 'Home', description: 'Main dashboard and overview' },
    { id: 'documents', label: 'Documents', description: 'File management and documents' },
    { id: 'favorites', label: 'Favorites', description: 'Saved and favorite items' },
    { id: 'notifications', label: 'Notifications', description: 'Alerts and messages' },
    { id: 'profile', label: 'Profile', description: 'User account and settings' }
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-950 to-black" />
      
      {/* Content */}
      <div className="relative z-10 p-8">
        {/* Header */}
        <div className="text-center mb-12 pt-8">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-400 via-blue-400 to-purple-300 bg-clip-text text-transparent">
            Figma Footer Navigation
          </h1>
          <p className="text-gray-400 text-xl max-w-2xl mx-auto">
            Glass morphism design with backdrop blur, purple accent colors, and smooth transitions
          </p>
        </div>

        {/* Design Specifications */}
        <div className="max-w-6xl mx-auto mb-16">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Glass Effect */}
            <div className="bg-gray-900/30 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-full mb-4 flex items-center justify-center">
                <div className="w-6 h-6 bg-purple-400 rounded-full opacity-60" />
              </div>
              <h3 className="text-lg font-semibold text-purple-300 mb-2">Glass Morphism</h3>
              <p className="text-gray-400 text-sm">
                20% black background with backdrop blur effect and rounded corners
              </p>
            </div>

            {/* Active States */}
            <div className="bg-gray-900/30 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
              <div className="w-12 h-12 border-2 border-purple-400 rounded-full mb-4 flex items-center justify-center">
                <div className="w-4 h-4 bg-purple-400 rounded-full" />
              </div>
              <h3 className="text-lg font-semibold text-purple-300 mb-2">Active States</h3>
              <p className="text-gray-400 text-sm">
                Purple border (#9d90e1) with label and underline for active items
              </p>
            </div>

            {/* Typography */}
            <div className="bg-gray-900/30 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
              <div className="w-12 h-12 bg-gray-800 rounded-full mb-4 flex items-center justify-center">
                <span className="text-purple-400 font-bold text-lg">Aa</span>
              </div>
              <h3 className="text-lg font-semibold text-purple-300 mb-2">SF Pro Font</h3>
              <p className="text-gray-400 text-sm">
                32px SF Pro font for active labels with proper spacing
              </p>
            </div>
          </div>
        </div>

        {/* Navigation Items Grid */}
        <div className="max-w-4xl mx-auto mb-20">
          <h2 className="text-2xl font-semibold text-center mb-8 text-purple-300">
            Navigation Items
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {navigationItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveItem(item.id)}
                className={`
                  p-4 rounded-xl border transition-all duration-300 text-left
                  ${activeItem === item.id 
                    ? 'bg-purple-500/10 border-purple-400/30 text-purple-300' 
                    : 'bg-gray-900/20 border-gray-700/30 text-gray-400 hover:bg-gray-800/30'
                  }
                `}
              >
                <h3 className="font-medium mb-1">{item.label}</h3>
                <p className="text-sm opacity-80">{item.description}</p>
                {activeItem === item.id && (
                  <div className="mt-2 text-xs text-purple-400 font-medium">
                    Currently Active
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Design Details */}
        <div className="max-w-3xl mx-auto text-center mb-20">
          <div className="bg-gray-900/20 backdrop-blur-sm rounded-2xl border border-gray-700/30 p-8">
            <h3 className="text-xl font-semibold text-purple-300 mb-4">Design Details</h3>
            <div className="grid md:grid-cols-2 gap-6 text-left">
              <div>
                <h4 className="font-medium text-white mb-2">Colors</h4>
                <ul className="text-sm text-gray-400 space-y-1">
                  <li>• Active: #9d90e1 (Purple)</li>
                  <li>• Inactive: #ffffff (White)</li>
                  <li>• Background: rgba(0,0,0,0.20)</li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-white mb-2">Dimensions</h4>
                <ul className="text-sm text-gray-400 space-y-1">
                  <li>• Border radius: 296px</li>
                  <li>• Icon size: 39×43px (active)</li>
                  <li>• Font size: 32px</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Figma Footer Navigation */}
      <FigmaFooterNav activeItem={activeItem} />
    </div>
  );
};

export default FigmaFooterDemo;