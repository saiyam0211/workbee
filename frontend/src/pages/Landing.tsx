import React, { useEffect } from 'react'
import { Demo } from '@/pages/demo'

export default function Landing() {
  useEffect(() => {
    document.body.classList.add('dark')
  }, [])

  return (
    <main className="min-h-dvh bg-background text-foreground">
      <Demo />
    </main>
  )
}

