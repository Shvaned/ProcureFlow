"use client";
import { Card, CardContent } from "@/components/ui/card";
import { ShoppingCart } from "lucide-react";

export default function ProcurementAIPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">AI Procurement Copilot</h1>
        <p className="text-muted-foreground">Reorder recommendations, supplier comparison, what-if analysis</p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {["Reorder Engine", "Supplier Comparison", "What-If Analysis"].map((label) => (
          <Card key={label}>
            <CardContent className="py-6">
              <ShoppingCart className="mb-2 h-5 w-5 text-primary" />
              <h3 className="font-semibold">{label}</h3>
              <p className="text-sm text-muted-foreground">AI recommends; you decide</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
