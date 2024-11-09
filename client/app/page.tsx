"use client";
import { useState } from "react";
import { Score } from "./components/score";
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

const formSchema = z.object({
  streetAddress: z.string().min(1, "Street address is required"),
  city: z.string().min(1, "City is required"),
  state: z.string().length(2, "Please use 2-letter state code"),
  zipCode: z.string().length(5, "ZIP code must be 5 digits"),
  county: z.string().min(1, "County is required"),
});

export default function Home() {
  const [response, setResponse] = useState<{ message?: string } | null>(null);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      streetAddress: "2102 Hummingbird St",
      city: "Princeton",
      state: "TX",
      zipCode: "75407",
      county: "Collin",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    const fullAddress = `${values.streetAddress} ${values.city}, ${values.state} ${values.zipCode}`;
    try {
      const res = await fetch(`http://localhost:6969/?location=${encodeURIComponent(fullAddress)}`);
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6 w-full max-w-md">
          <FormField
            control={form.control}
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
            control={form.control}
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
              control={form.control}
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
              control={form.control}
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
            control={form.control}
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

          <Button type="submit" className="w-full">Get Risk Score</Button>
        </form>
      </Form>

      {response && (
        <div className="mt-8 p-4 bg-gray-100 rounded-lg text-black">
          <Score score={(response as any).risk_score || 0} />
        </div>
      )}
    </div>
  );
}
