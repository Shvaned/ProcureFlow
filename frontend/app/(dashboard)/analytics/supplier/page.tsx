"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Truck, Star, Download } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface SupData {
  total_suppliers: number;
  average_rating: number;
  top_suppliers: { name: string; rating: number }[];
}

export default function SupplierAnalytics() {
  const [data, setData] = useState<SupData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .get<{ data: SupData }>("/api/v1/analytics/supplier")
      .then((r) => {
        setData(r.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className="py-16 text-center text-muted-foreground">Loading supplier analytics...</div>
    );

  const chartData =
    data?.top_suppliers?.map((s) => ({
      name: s.name?.slice(0, 15) || "Unknown",
      rating: s.rating || 0,
    })) || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Supplier Performance</h1>
          <p className="text-muted-foreground">Scorecards, ratings, delivery accuracy</p>
        </div>
        <Button variant="outline" size="sm">
          <Download className="mr-2 h-4 w-4" /> Export
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Total Suppliers</p>
            <p className="text-2xl font-bold">{data?.total_suppliers || 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Average Rating</p>
            <p className="text-2xl font-bold flex items-center gap-1">
              <Star className="h-5 w-5 fill-orange-400 text-orange-400" />
              {data?.average_rating?.toFixed(1) || "0.0"}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Top Supplier</p>
            <p className="text-2xl font-bold">
              {data?.top_suppliers?.[0]?.name?.slice(0, 15) || "--"}
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Top Suppliers by Rating</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={chartData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 5]} style={{ fontSize: 12 }} />
              <YAxis type="category" dataKey="name" width={140} style={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="rating" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
