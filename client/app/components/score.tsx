"use client"

import { cn } from "@/lib/utils"

interface ScoreProps {
  score: number 
  className?: string
}

export function Score({ score, className }: ScoreProps) {
  const normalizedScore = Math.min(Math.max(score, 0), 100)
  
  const getScoreColor = (score: number) => {
    if (score <= 20) return "text-green-500"
    if (score <= 40) return "text-emerald-500"
    if (score <= 60) return "text-yellow-500"
    if (score <= 80) return "text-orange-500"
    return "text-red-500"
  }

  return (
    <div className={cn("text-center text-4xl font-bold tracking-tighter", getScoreColor(normalizedScore))}>
      {normalizedScore}
    </div>
  )
}
