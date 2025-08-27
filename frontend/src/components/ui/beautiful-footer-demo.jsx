import React, { useState } from 'react';
import BeautifulFooterNav from './beautiful-footer-nav';

const BeautifulFooterDemo = () => {
  const [activeItem, setActiveItem] = useState('home');

  const features = [
    {
      title: 'Glass Morphism',
      description: 'Advanced backdrop blur with gradient overlays',
      icon: '✨'
    },
    {
      title: 'Smooth Animations',
      description: '500ms transitions with easing curves',
      icon: '🎭'
    },
    {
      title: 'Interactive States',
      description: 'Hover effects and active state indicators',
      icon: '🎯'
    },
    {
      title: 'Purple Glow',
      description: 'Elegant purple accent with shadow effects',
      icon: '💜'
    },
    {
      title: 'Floating Tooltips',
      description: 'Context-aware labels on hover',
      icon: '💬'
    },
    {
      title: 'Responsive Design',
      description: 'Scales beautifully on all devices',
      icon: '📱'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-gray-900 text-white overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-600/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
      </div>
      
      {/* Content */}
      <div className="relative z-10 p-8">
        {/* Header */}
        <div className="text-center mb-16 pt-12">
          <div className="inline-block p-4 rounded-2xl bg-gradient-to-br from-purple-500/20 to-blue-500/20 backdrop-blur-sm border border-purple-400/30 mb-6">
            <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-300 via-blue-300 to-purple-400 bg-clip-text text-transparent">
              Beautiful Footer
            </h1>
          </div>
          <p className="text-gray-300 text-xl max-w-3xl mx-auto leading-relaxed">
            A stunning navigation component with glass morphism effects, smooth animations, and elegant purple accents
          </p>
        </div>

        {/* Features Grid */}
        <div className="max-w-6xl mx-auto mb-20">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div 
                key={index}
                className="group p-6 rounded-2xl bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm border border-gray-700/50 hover:border-purple-400/30 transition-all duration-500 hover:transform hover:scale-105"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-purple-300 mb-2 group-hover:text-purple-200 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-gray-400 group-hover:text-gray-300 transition-colors">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Interactive Demo Section */}
        <div className="max-w-4xl mx-auto mb-20">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-purple-300 mb-4">Interactive Demo</h2>
            <p className="text-gray-400">Click on different navigation items to see the beautiful transitions</p>
          </div>
          
          <div className="grid md:grid-cols-5 gap-4 mb-8">
            {['home', 'documents', 'favorites', 'notifications', 'profile'].map((item) => (
              <button
                key={item}
                onClick={() => setActiveItem(item)}
                className={`
                  p-4 rounded-xl border transition-all duration-300 text-center capitalize
                  ${activeItem === item 
                    ? 'bg-purple-500/20 border-purple-400/50 text-purple-300 shadow-lg shadow-purple-500/25' 
                    : 'bg-gray-800/30 border-gray-600/30 text-gray-400 hover:bg-gray-700/40 hover:border-gray-500/50'
                  }
                `}
              >
                <div className="font-medium">{item}</div>
                {activeItem === item && (
                  <div className="text-xs text-purple-400 mt-1">Active</div>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Design Specifications */}
        <div className="max-w-5xl mx-auto mb-24">
          <div className="bg-gradient-to-br from-gray-800/30 to-gray-900/30 backdrop-blur-sm rounded-3xl border border-gray-700/50 p-8">
            <h3 className="text-2xl font-bold text-purple-300 mb-6 text-center">Design Specifications</h3>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500/30 to-blue-500/30 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl">🎨</span>
                </div>
                <h4 className="font-semibold text-white mb-2">Colors</h4>
                <ul className="text-sm text-gray-400 space-y-1">
                  <li>Purple: #9d90e1</li>
                  <li>Background: rgba(0,0,0,0.8)</li>
                  <li>Glass: backdrop-blur-xl</li>
                </ul>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500/30 to-blue-500/30 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl">📐</span>
                </div>
                <h4 className="font-semibold text-white mb-2">Dimensions</h4>
                <ul className="text-sm text-gray-400 space-y-1">
                  <li>Icons: 24×24px</li>
                  <li>Padding: 16px</li>
                  <li>Border radius: 9999px</li>
                </ul>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500/30 to-blue-500/30 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl">⚡</span>
                </div>
                <h4 className="font-semibold text-white mb-2">Animations</h4>
                <ul className="text-sm text-gray-400 space-y-1">
                  <li>Duration: 500ms</li>
                  <li>Easing: ease-out</li>
                  <li>Hover: scale(1.05)</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Beautiful Footer Navigation */}
      <BeautifulFooterNav activeItem={activeItem} />
    </div>
  );
};

export default BeautifulFooterDemo;