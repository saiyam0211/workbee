import React from 'react';
import { Default, Customized } from '../components/ui/modern-mobile-menu-demo';

const ModernMenuDemo = () => {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold text-foreground">Modern Mobile Menu</h1>
          <p className="text-muted-foreground text-lg">
            Interactive mobile navigation component with smooth animations and customizable styling
          </p>
        </div>

        {/* Default Example */}
        <div className="space-y-6">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-foreground mb-2">Default Menu</h2>
            <p className="text-muted-foreground">Using default items and styling</p>
          </div>
          <div className="flex justify-center">
            <div className="bg-card border border-border rounded-lg p-8 shadow-lg">
              <Default />
            </div>
          </div>
        </div>

        {/* Customized Example */}
        <div className="space-y-6">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-foreground mb-2">Customized Menu</h2>
            <p className="text-muted-foreground">With custom accent color and Lucide icons</p>
          </div>
          <div className="flex justify-center">
            <div className="bg-card border border-border rounded-lg p-8 shadow-lg">
              <Customized />
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mt-12">
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-2">Smooth Animations</h3>
            <p className="text-muted-foreground">Icon bounce effects and smooth transitions</p>
          </div>
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-2">Responsive Design</h3>
            <p className="text-muted-foreground">Adapts to different screen sizes and orientations</p>
          </div>
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="text-lg font-semibold text-foreground mb-2">Customizable</h3>
            <p className="text-muted-foreground">Easy to customize colors, icons, and labels</p>
          </div>
        </div>

        {/* Usage Instructions */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Usage</h3>
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-foreground mb-2">Basic Usage:</h4>
              <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
{`import { InteractiveMenu } from './components/ui/modern-mobile-menu';

<InteractiveMenu />`}
              </pre>
            </div>
            <div>
              <h4 className="font-medium text-foreground mb-2">With Custom Items:</h4>
              <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
{`import { InteractiveMenu } from './components/ui/modern-mobile-menu';
import { Home, Search, User } from 'lucide-react';

const customItems = [
  { label: 'home', icon: Home },
  { label: 'search', icon: Search },
  { label: 'profile', icon: User }
];

<InteractiveMenu items={customItems} accentColor="hsl(var(--primary))" />`}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModernMenuDemo;
