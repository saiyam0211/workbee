import React, { useState } from 'react';
import ModernFooterNav from './modern-footer-nav';

const FooterNavDemo = () => {
  const [currentVariant, setCurrentVariant] = useState('strategy');

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
          Modern Footer Navigation
        </h1>
        <p className="text-gray-400 text-lg">
          Dark themed navigation with active states and smooth transitions
        </p>
      </div>

      {/* Variant Selector */}
      <div className="flex justify-center mb-16">
        <div className="bg-gray-900/50 backdrop-blur-sm rounded-full p-1 border border-gray-700/50">
          <button
            onClick={() => setCurrentVariant('strategy')}
            className={`px-6 py-3 rounded-full transition-all duration-300 ${
              currentVariant === 'strategy'
                ? 'bg-purple-500/20 text-purple-300 border border-purple-400/30'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            Strategy Variant
          </button>
          <button
            onClick={() => setCurrentVariant('home')}
            className={`px-6 py-3 rounded-full transition-all duration-300 ${
              currentVariant === 'home'
                ? 'bg-purple-500/20 text-purple-300 border border-purple-400/30'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            Home Variant
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="max-w-4xl mx-auto">
        <div className="bg-gray-900/30 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-8 mb-8">
          <h2 className="text-2xl font-semibold mb-4 text-center">
            {currentVariant === 'strategy' ? 'Strategy Navigation' : 'Home Navigation'}
          </h2>
          <p className="text-gray-400 text-center mb-8">
            {currentVariant === 'strategy' 
              ? 'Navigation focused on business strategy with Strategy item highlighted'
              : 'Navigation focused on home dashboard with Home item highlighted'
            }
          </p>
          
          {/* Feature List */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-purple-300">Features</h3>
              <ul className="space-y-2 text-gray-400">
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                  Dark themed design
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                  Rounded corners with backdrop blur
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                  Purple/blue gradient active states
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                  Smooth hover transitions
                </li>
              </ul>
            </div>
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-purple-300">Navigation Items</h3>
              <ul className="space-y-2 text-gray-400">
                {currentVariant === 'strategy' ? (
                  <>
                    <li>🏠 Home</li>
                    <li className="text-purple-300 font-medium">💼 Strategy (Active)</li>
                    <li>📅 Calendar</li>
                    <li>🛡️ Security</li>
                    <li>⚙️ Settings</li>
                  </>
                ) : (
                  <>
                    <li className="text-purple-300 font-medium">🏠 Home (Active)</li>
                    <li>📄 Documents</li>
                    <li>❤️ Favorites</li>
                    <li>🔔 Notifications</li>
                    <li>👤 Profile</li>
                  </>
                )}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Navigation */}
      <ModernFooterNav 
        variant={currentVariant} 
        activeItem={currentVariant === 'strategy' ? 'strategy' : 'home'} 
      />
    </div>
  );
};

export default FooterNavDemo;