"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import { apiClient } from "@/services/api-client";

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.get<any>(`/api/v1/products/${id}`)
      .then((r) => setProduct(r.data))
      .catch(() => setProduct(null))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="p-6 text-muted-foreground">Loading...</div>;
  if (!product) return <div className="p-6 text-destructive">Product not found</div>;

  return (
    <div className="space-y-6">
      <Link href="/products"><Button variant="ghost"><ArrowLeft className="mr-2 h-4 w-4" /> Back</Button></Link>
      <div>
        <h1 className="text-2xl font-bold">{product.name}</h1>
        <p className="text-muted-foreground">SKU: {product.sku}</p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <Card><CardContent className="py-4"><p className="text-sm text-muted-foreground">Cost Price</p><p className="text-xl font-bold">₹{product.cost_price?.toLocaleString()}</p></CardContent></Card>
        <Card><CardContent className="py-4"><p className="text-sm text-muted-foreground">Selling Price</p><p className="text-xl font-bold">₹{product.selling_price?.toLocaleString()}</p></CardContent></Card>
        <Card><CardContent className="py-4"><p className="text-sm text-muted-foreground">Status</p><p className="text-xl font-bold">{product.is_active ? "Active" : "Inactive"}</p></CardContent></Card>
      </div>
    </div>
  );
}
