#!/bin/bash

# WorkBee Vercel Deployment Script
echo "🚀 Deploying WorkBee to Vercel"
echo "==============================="

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Build the frontend
echo "📦 Building frontend..."
cd frontend
npm run build
cd ..

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
npx vercel --prod

echo "✅ Deployment complete!"
echo ""
echo "🔗 Your app should be available at:"
echo "   https://workbee.vercel.app"
echo "   https://workbee.vercel.app/dashboard"
echo "   https://workbee.vercel.app/redirect"
echo ""
echo "📱 Android app will load from:"
echo "   https://workbee.vercel.app/redirect (with auto-redirect to dashboard)"
