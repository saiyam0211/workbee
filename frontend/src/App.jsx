import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Landing from '@/pages/Landing'
import Dashboard from '@/pages/Dashboard'
import FavCompanies from '@/pages/fav-companies'
import Notifications from '@/pages/Notifications'
import SearchPage from '@/pages/SearchPage'

export default function App() {
  return (
    <Router basename="/">
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/fav-companies" element={<FavCompanies />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/search" element={<SearchPage />} />
        {/* Catch-all route for 404 handling */}
        <Route path="*" element={<Landing />} />
      </Routes>
    </Router>
  )
}


