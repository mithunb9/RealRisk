"use client";
import { useState } from "react";
import Score from "./components/score";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Loader2, MapPin, Send } from "lucide-react";
import { TooltipProvider } from "@/components/ui/tooltip";
import Extras from "./components/extras";
import Head from "next/head";

const addressFormSchema = z.object({
  streetAddress: z.string().min(1, "Street address is required"),
  city: z.string().min(1, "City is required"),
  state: z.string().length(2, "Please use 2-letter state code"),
  zipCode: z.string().length(5, "ZIP code must be 5 digits"),
  county: z.string().min(1, "County is required"),
});

const coordsFormSchema = z.object({
  latitude: z.string().regex(/^-?\d*\.?\d*$/, "Must be a valid latitude"),
  longitude: z.string().regex(/^-?\d*\.?\d*$/, "Must be a valid longitude"),
});

const apnFormSchema = z.object({
  apn: z.string().min(1, "APN is required"),
});

export default function Home() {
  const [response, setResponse] = useState<{ message?: string } | null>(null);
  const [conversationHistory, setConversationHistory] = useState<Array<{role: 'user' | 'assistant', content: string}>>([]); 
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  const addressForm = useForm<z.infer<typeof addressFormSchema>>({
    resolver: zodResolver(addressFormSchema),
    defaultValues: {
      streetAddress: "2102 Hummingbird St",
      city: "Princeton",
      state: "TX",
      zipCode: "75407",
      county: "Collin",
    },
  });

  const coordsForm = useForm<z.infer<typeof coordsFormSchema>>({
    resolver: zodResolver(coordsFormSchema),
    defaultValues: {
      latitude: "32.997826",
      longitude: "-96.760584",
    },
  });

  const apnForm = useForm<z.infer<typeof apnFormSchema>>({
    resolver: zodResolver(apnFormSchema),
    defaultValues: {
      apn: "",
    },
  });

  async function onAddressSubmit(values: z.infer<typeof addressFormSchema>) {
    setIsLoading(true);
    const fullAddress = `${values.streetAddress} ${values.city}, ${values.state} ${values.zipCode}`;
    try {
      const res = await fetch(`http://localhost:6969/?location=${encodeURIComponent(fullAddress)}&county=${encodeURIComponent(values.county)}`);
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      if (data.error) {
        console.error('Server error:', data.message);
        return;
      }
      setResponse(data);
      if (data.ai_summary) {
        setConversationHistory([{ role: 'assistant', content: data.ai_summary }]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setIsLoading(false);
    }
  }

  async function onCoordsSubmit(values: z.infer<typeof coordsFormSchema>) {
    setIsLoading(true);
    try {
      const res = await fetch(`http://localhost:6969/?lat=${values.latitude}&lon=${values.longitude}`);
      const data = await res.json();
      setResponse(data);
      if (data.ai_summary) {
        setConversationHistory([{ role: 'assistant', content: data.ai_summary }]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setIsLoading(false);
    }
  }

  async function onAPNSubmit(values: z.infer<typeof apnFormSchema>) {
    setIsLoading(true);
    try {
      const res = await fetch(`http://localhost:6969/?apn=${encodeURIComponent(values.apn)}`);
      const data = await res.json();
      setResponse(data);
      if (data.ai_summary) {
        setConversationHistory([{ role: 'assistant', content: data.ai_summary }]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setIsLoading(false);
    }
  }

  async function sendMessage() {
    if (!message.trim()) return;
    
    try {
      setMessage("");

      setConversationHistory(prevHistory => [
        ...prevHistory,
        { role: "user", content: message },
      ]);

      const res = await fetch('http://localhost:6969/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: message,
          history: conversationHistory
        })
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();

      setConversationHistory(prevHistory => [
        ...prevHistory,
        { role: "assistant", content: data.message }
      ]);

      setResponse(prevResponse => ({
        ...prevResponse,
        ai_summary: data.message
      }));
    } catch (err) {
      console.error('Error sending message:', err);
    }
  }

  return (
    <TooltipProvider>
      <Head>
        <title>RealRisk</title>
      </Head>
      <div className="min-h-screen flex flex-col items-center justify-center p-8">
        {!response ? (
          <div className="flex gap-8 w-full max-w-6xl">
            <div className="flex-1 opacity-50">
              <h2 className="text-xl font-bold mb-4">Search by APN</h2>
              <Form {...apnForm}>
                <form onSubmit={apnForm.handleSubmit(onAPNSubmit)} className="space-y-6">
                  <FormField
                    control={apnForm.control}
                    name="apn"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Assessor's Parcel Number (APN)</FormLabel>
                        <FormControl>
                          <Input disabled placeholder="Enter APN" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <Button disabled type="submit" className="w-full">
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Getting Risk Score...
                      </>
                    ) : (
                      "Get Risk Score"
                    )}
                  </Button>
                </form>
              </Form>
            </div>

            <div className="flex-1">
              <h2 className="text-xl font-bold mb-4">Search by Address</h2>
              <Form {...addressForm}>
                <form onSubmit={addressForm.handleSubmit(onAddressSubmit)} className="space-y-6">
                  <FormField
                    control={addressForm.control}
                    name="streetAddress"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Street Address</FormLabel>
                        <FormControl>
                          <Input placeholder="123 Main St" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={addressForm.control}
                    name="city"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>City</FormLabel>
                        <FormControl>
                          <Input placeholder="City" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="flex gap-4">
                    <FormField
                      control={addressForm.control}
                      name="state"
                      render={({ field }) => (
                        <FormItem className="flex-1">
                          <FormLabel>State</FormLabel>
                          <FormControl>
                            <Input placeholder="TX" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={addressForm.control}
                      name="zipCode"
                      render={({ field }) => (
                        <FormItem className="flex-1">
                          <FormLabel>ZIP Code</FormLabel>
                          <FormControl>
                            <Input placeholder="12345" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>

                  <FormField
                    control={addressForm.control}
                    name="county"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>County</FormLabel>
                        <FormControl>
                          <Input placeholder="County" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <Button disabled={isLoading} type="submit" className="w-full">
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Getting Risk Score...
                      </>
                    ) : (
                      "Get Risk Score"
                    )}
                  </Button>
                </form>
              </Form>
            </div>

            <div className="flex-1">
              <h2 className="text-xl font-bold mb-4">Search by Coordinates</h2>
              <Form {...coordsForm}>
                <form onSubmit={coordsForm.handleSubmit(onCoordsSubmit)} className="space-y-6">
                  <FormField
                    control={coordsForm.control}
                    name="latitude"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Latitude</FormLabel>
                        <FormControl>
                          <Input placeholder="33.1800" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={coordsForm.control}
                    name="longitude"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Longitude</FormLabel>
                        <FormControl>
                          <Input placeholder="-96.4977" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <Button disabled={isLoading} type="submit" className="w-full mt-[318px]">
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Getting Risk Score...
                      </>
                    ) : (
                      "Get Risk Score"
                    )}
                  </Button>
                </form>
              </Form>
            </div>
          </div>
        ) : (
          <div>
            <div className="grid grid-cols-2 gap-8">
              <div className="flex flex-col gap-4">
                <div className="flex items-center gap-2">
                  <MapPin className="h-6 w-6" />
                  <h1 className="text-2xl font-bold">
                    {(response as any).location?.location || "Location Not Found"}
                  </h1>
                </div>
                <div className="text-sm text-gray-500">
                  Latitude: {(response as any).location?.latitude || "N/A"}
                  {" | "}
                  Longitude: {(response as any).location?.longitude || "N/A"}
                </div>
                <iframe 
                  src={`https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d14273.829742374324!2d${(response as any).location?.longitude}!3d${(response as any).location?.latitude}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e1!3m2!1sen!2sus!4v1731194741378!5m2!1sen!2sus`} 
                  width="600"
                  height="400"
                  style={{border:0}}
                  allowFullScreen={true}
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  className="rounded-lg"
                />
              </div>
              <div className="flex flex-col h-[500px]">
                <div className="flex-1 p-6 border border-gray rounded-lg overflow-y-auto mb-4">
                  <h2 className="text-xl font-bold mb-4">Analysis</h2>
                  {conversationHistory.map((msg, index) => (
                    <div key={index} className={`mb-4 ${msg.role === 'assistant' ? 'bg-gray-200 p-4 rounded-lg' : 'text-gray-700'}`}>
                      <strong>{msg.role === 'assistant' ? 'RiskAI: ' : 'You: '}</strong>
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  ))}
                </div>
                <div className="flex gap-2">
                  <Input 
                    placeholder="Ask a question about this analysis..." 
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  />
                  <Button onClick={sendMessage}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
            <div className="mt-8 p-6 bg-gray-100 rounded-lg text-black grid grid-cols-5 gap-6">
              <Score 
                score={(response as any).demographic_risk?.risk_score || 0}
                title="Demographic"
                description="Population and socioeconomic factors"
                components={(response as any).demographic_risk?.components}
                showDetails={true}
                tooltips={(response as any).demographic_risk?.tooltip}
              />
              <Score 
                score={(response as any).competitor_risk?.risk_score || 0}
                title="Competition"
                description="Local market competition analysis"
                components={(response as any).competitor_risk?.components}
                showDetails={true}
                tooltips={(response as any).competitor_risk?.tooltip}
              />
              <Score 
                score={(response as any).environment_risk?.risk_score || 0}
                title="Environmental"
                description="Weather and natural disaster risks"
                components={(response as any).environment_risk?.components}
                showDetails={true}
                tooltips={(response as any).environment_risk?.tooltip}
              />
              <Score 
                score={(response as any).regulatory_risk?.risk_score || 0}
                title="Regulatory"
                description="Building codes, ordinances, and zoning laws"
                components={(response as any).regulatory_risk?.components}
                showDetails={true}
                tooltips={(response as any).regulatory_risk?.tooltip}
                response={(response as any).regulatory_risk?.response}
              />
              <Score 
                score={(response as any).crime_risk?.risk_score || 0}
                title="Crime"
                description="Local crime statistics and safety"
                components={(response as any).crime_risk?.components}
                showDetails={true}
                tooltips={(response as any).crime_risk?.tooltip}
              />
            </div>
            {(response as any).extras && (
              <Extras extras={(response as any).extras} />
            )}
          </div>
        )}
      </div>
    </TooltipProvider>
  );
}