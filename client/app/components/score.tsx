"use client"

import * as React from "react"
import { TrendingUp } from "lucide-react"
import { Label, Pie, PieChart, Cell } from "recharts"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
} from "@/components/ui/chart"

interface ScoreProps {
  score: number
  title: string
  description: string
  components?: Record<string, number>
  showDetails?: boolean
  tooltips?: Record<string, string>
}

const getRiskColor = (score: number) => {
  if (score > 80) return '#BD1E1E'
  if (score > 50) return '#F59E0B'
  return '#4DA167'
}

export default function Score({ score, title, description, components, showDetails, tooltips }: ScoreProps) {
  const data = React.useMemo(() => [{
    name: "Risk Score",
    value: score,
    fill: getRiskColor(score)
  }], [score])

  const config: ChartConfig = {
    score: {
      label: "Risk Score"
    }
  }

  return (
    <Card className="flex flex-col">
      <CardHeader className="items-center pb-0">
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer
          config={config}
          className="mx-auto aspect-square max-h-[250px]"
        >
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={60}
              outerRadius={80}
              startAngle={180}
              endAngle={0}
              strokeWidth={2}
              stroke="white"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
              <Label
                content={({ viewBox }) => {
                  if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                    return (
                      <text
                        x={viewBox.cx}
                        y={viewBox.cy}
                        textAnchor="middle"
                        dominantBaseline="middle"
                      >
                        <tspan
                          x={viewBox.cx}
                          y={viewBox.cy}
                          className="fill-foreground text-3xl font-bold"
                          style={{ fill: getRiskColor(score) }}
                        >
                          {score}
                        </tspan>
                        <tspan
                          x={viewBox.cx}
                          y={(viewBox.cy || 0) + 24}
                          className="fill-muted-foreground text-sm"
                        >
                          Risk Score
                        </tspan>
                      </text>
                    )
                  }
                }}
              />
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm">
        <div className="flex items-center gap-2 font-medium leading-none">
          Risk Assessment <TrendingUp className="h-4 w-4" />
        </div>
        {showDetails && components && (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="text-left w-1/2">Component</TableHead>
                <TableHead className="text-left w-1/2">Value</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Object.entries(components).map(([key, value]) => (
                <TableRow key={key}>
                  <TableCell className="font-medium">
                    {tooltips?.[key] ? (
                      <Tooltip>
                        <TooltipTrigger className="cursor-help text-left">
                          {key.replace(/_/g, ' ')}
                        </TooltipTrigger>
                        <TooltipContent>
                          {tooltips[key]}
                        </TooltipContent>
                      </Tooltip>
                    ) : (
                      key.replace(/_/g, ' ')
                    )}
                  </TableCell>
                  <TableCell className="text-left">
                    {String(value)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardFooter>
    </Card>
  )
}
