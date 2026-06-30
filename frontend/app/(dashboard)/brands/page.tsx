"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export default function BrandsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Brands</h1>
          <p className="text-muted-foreground">Manage product brands</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" /> Add Brand
        </Button>
      </div>
      <Card>
        <CardContent className="py-16">
          <div className="flex flex-col items-center justify-center text-center">
            <p className="text-lg font-semibold">No brands yet</p>
            <p className="mt-1 text-sm text-muted-foreground">
              Create brands to associate with your products.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
