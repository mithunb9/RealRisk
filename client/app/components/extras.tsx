import {
  Card,
  CardContent,
} from "@/components/ui/card"

import { MapPin, Users, Landmark, Map, Navigation, Trees} from 'lucide-react'

interface ExtrasProps {
  extras: {
    [key: string]: string
  }
}

export default function Extras({ extras }: ExtrasProps) {
  const mainOrder = [
    'Population',
    'Land Area', 
    'Green Space',
    'Points of Interest',
    'New Points of Interest'
  ];

  const getIcon = (key: string) => {
    switch(key) {
      case 'Population': return <Users className="w-5 h-5" />;
      case 'Land Area': return <Map className="w-5 h-5" />;
      case 'Green Space': return <Trees className="w-5 h-5" />;
      case 'Points of Interest': return <Landmark className="w-5 h-5" />;
      case 'New Points of Interest': return <Navigation className="w-5 h-5" />;
      default: return <MapPin className="w-5 h-5" />;
    }
  };

  const locationInfo = ['City', 'County', 'State'].reduce((acc, key) => {
    if (key in extras) {
      acc[key] = extras[key];
    }
    return acc;
  }, {} as {[key: string]: string});

  const otherInfo = mainOrder
    .filter(key => key in extras && !['County', 'State'].includes(key))
    .reduce((acc, key) => ({
      ...acc,
      [key]: extras[key]
    }), {});

  return (
    <Card className="w-full mt-6">
      <CardContent>
        <div className="space-y-6">
          <div className="space-y-2">
            <h2 className="text-2xl font-bold flex items-center gap-2 pt-6">
              <MapPin className="w-6 h-6" />
              {Object.entries(locationInfo).map(([key, value], index) => (
                <span key={key}>
                  {value}
                  {index < Object.entries(locationInfo).length - 1 ? ", " : ""}
                </span>
              ))}
            </h2>
          </div>

          <div className="flex flex-col gap-4">
            {Object.entries(otherInfo).map(([key, value]) => (
              <div key={key} className="flex items-center gap-2">
                {getIcon(key)}
                <span className="font-medium">{key}:</span>
                <span>{key === 'Points of Interest' || key === 'New Points of Interest' 
                  ? String(value).split(',').map(item => item.trim()).join(', ')
                  : String(value)}</span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}