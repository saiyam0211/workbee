# WorkBee Android App Setup

This document explains how to build and run the WorkBee Android app using Capacitor.

## 🚀 Quick Start

1. **Run the setup script:**
   ```bash
   ./run-android.sh
   ```

2. **Or manually:**
   ```bash
   # Sync Capacitor
   npx cap sync android
   
   # Open Android Studio
   npx cap open android
   ```

## 📱 App Configuration

The app is configured to:
- **URL**: Loads `https://workbee.vercel.app/dashboard` directly
- **Icon**: Uses `android/app/src/appicon.png` as the app icon
- **Splash Screen**: Shows the same icon as splash screen
- **Theme**: Dark theme matching the web app

## 🔧 Android Studio Setup

1. **Open the project** in Android Studio (should open automatically)
2. **Wait for Gradle sync** to complete
3. **Connect your device** or start an emulator
4. **Click Run** (green play button) to build and install the app

## 📋 Requirements

- Android Studio (latest version)
- Android SDK (API level 21 or higher)
- Physical Android device or emulator
- Node.js 18+ (for Capacitor CLI)

## 🎯 Features

- **Dashboard Only**: The app loads directly to the dashboard
- **Native Feel**: Uses Capacitor for native Android features
- **Custom Icon**: Your appicon.png is used throughout
- **Splash Screen**: Shows your icon during app launch
- **Responsive**: Optimized for mobile devices

## 🐛 Troubleshooting

### App won't load
- Check your internet connection
- Verify `workbee.vercel.app/dashboard` is accessible
- Check Android Studio logs for errors

### Build errors
- Clean and rebuild the project in Android Studio
- Run `npx cap sync android` again
- Check that all dependencies are installed

### Icon not showing
- Verify `appicon.png` exists in `android/app/src/`
- Run `npx cap sync android` to update assets
- Clean and rebuild the project

## 📁 Project Structure

```
frontend/
├── android/                 # Android project
│   └── app/
│       └── src/
│           ├── appicon.png  # Your app icon
│           └── main/
│               └── res/     # Android resources
├── capacitor.config.json    # Capacitor configuration
└── run-android.sh          # Quick start script
```

## 🔄 Updating the App

To update the app with new changes:

1. **Update the web app** on Vercel
2. **Sync Capacitor:**
   ```bash
   npx cap sync android
   ```
3. **Rebuild in Android Studio**

The app will automatically load the latest version from `workbee.vercel.app/dashboard`.
