#!/bin/bash

# WorkBee Android Production Build Script
echo "🏗️  Building WorkBee Android App for Production"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "capacitor.config.json" ]; then
    echo "❌ Error: Please run this script from the frontend directory"
    exit 1
fi

# Sync Capacitor
echo "📱 Syncing Capacitor..."
npx cap sync android

# Build APK
echo "🔨 Building APK..."
cd android
./gradlew assembleRelease

echo "✅ Build complete!"
echo ""
echo "📱 APK location:"
echo "   android/app/build/outputs/apk/release/app-release.apk"
echo ""
echo "📋 Next steps:"
echo "1. Install the APK on your device:"
echo "   adb install android/app/build/outputs/apk/release/app-release.apk"
echo ""
echo "2. Or open Android Studio and build from there:"
echo "   npx cap open android"
