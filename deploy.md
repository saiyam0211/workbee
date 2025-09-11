# Vercel Deployment Fix

## Problem
The app was showing 404 errors when accessing routes directly (like `/dashboard`, `/search`, etc.) because Vercel didn't know how to handle client-side routing for the React SPA.

## Solution
Created `vercel.json` configuration file to handle SPA routing properly.

## Files Added/Modified

### 1. `vercel.json` (Root directory)
```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/dist",
  "devCommand": "cd frontend && npm run dev",
  "installCommand": "cd frontend && npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 2. `frontend/public/_redirects` (Backup)
```
/*    /index.html   200
```

### 3. `frontend/src/App.jsx` (Updated)
- Added catch-all route for 404 handling
- Added explicit basename

## How It Works
- The `rewrites` configuration tells Vercel to serve `index.html` for all routes
- This allows React Router to handle client-side routing
- The catch-all route in App.jsx provides a fallback for unknown routes

## Deployment Steps
1. Commit and push these changes
2. Redeploy on Vercel
3. All routes should now work correctly

## Testing
After deployment, test these URLs:
- `/` (Landing page)
- `/dashboard` (Dashboard)
- `/search` (Search page)
- `/fav-companies` (Favorites)
- `/notifications` (Notifications)
- Any invalid route should redirect to landing page
