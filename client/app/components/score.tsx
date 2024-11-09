"use client"

import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"

interface ScoreProps {
  score: number 
  className?: string
}

export function Score({ score, className }: ScoreProps) {
  const normalizedScore = Math.min(Math.max(score, 0), 100)

  return (
    <div className={cn("relative w-32 h-32", className)}>
      {/*  progress background */}
      <div className="absolute inset-0">
        <Progress
          value={normalizedScore}
          className="h-full w-full rounded-full [&>div]:rounded-full"
        />
      </div>
      
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center">
          <span className="text-2xl font-bold">{normalizedScore}</span>
          <span className="text-sm block text-muted-foreground">Risk Score</span>
        </div>
      </div>
    </div>
  )
}
