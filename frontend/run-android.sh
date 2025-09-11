#!/bin/bash

# WorkBee Android App Runner Script
echo "🚀 WorkBee Android App Setup"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "capacitor.config.json" ]; then
    echo "❌ Error: Please run this script from the frontend directory"
    exit 1
fi

# Sync Capacitor
echo "📱 Syncing Capacitor..."
npx cap sync android

# Open Android Studio
echo "🔧 Opening Android Studio..."
npx cap open android

echo "✅ Android Studio should now be open with your WorkBee project!"
echo ""
echo "📋 Next steps:"
echo "1. Wait for Android Studio to load the project"
echo "2. Connect your Android device or start an emulator"
echo "3. Click the 'Run' button (green play icon) in Android Studio"
echo "4. The app will load workbee.vercel.app/dashboard directly"
echo ""
echo "🎯 The app is configured to:"
echo "   - Use your appicon.png as the app icon and splash screen"
echo "   - Load workbee.vercel.app/dashboard directly"
echo "   - Show only the dashboard (no other pages)"
