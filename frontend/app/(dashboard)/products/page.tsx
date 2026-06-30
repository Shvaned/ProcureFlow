"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus, Search } from "lucide-react";
import { apiClient } from "@/services/api-client";

interface ApiProduct { id: string; sku: string; name: string; cost_price: number; selling_price: number; is_active: boolean; brand?: { name: string } | null; category?: { name: string } | null; }

export default function ProductsPage() {
  const [search, setSearch] = useState("");
  const [products, setProducts] = useState<ApiProduct[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.get<{ data: { items: ApiProduct[] } }>("/api/v1/products", { page: "1", page_size: "50" })
      .then((r) => setProducts(r.data?.items || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Products</h1>
          <p className="text-muted-foreground">Manage your product catalog</p>
        </div>
        <Link href="/products/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" /> Add Product
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                className="w-full rounded-md border pl-10 pr-4 py-2 text-sm"
                placeholder="Search by SKU, name, brand, category..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {products.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <p className="text-lg font-semibold">No products yet</p>
              <p className="mt-1 text-sm text-muted-foreground">
                Create your first product to get started.
              </p>
              <Link href="/products/new" className="mt-4">
                <Button>Create Product</Button>
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left">
                    <th className="py-3 font-medium">SKU</th>
                    <th className="py-3 font-medium">Name</th>
                    <th className="py-3 font-medium">Brand</th>
                    <th className="py-3 font-medium">Category</th>
                    <th className="py-3 font-medium text-right">Cost</th>
                    <th className="py-3 font-medium text-right">Selling</th>
                    <th className="py-3 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map((p) => (
                    <tr key={p.id} className="border-b hover:bg-muted/50">
                      <td className="py-3 font-mono text-xs">{p.sku}</td>
                      <td className="py-3">
                        <Link href={`/products/${p.id}`} className="text-primary hover:underline">
                          {p.name}
                        </Link>
                      </td>
                      <td className="py-3 text-muted-foreground">{p.brand?.name || "--"}</td>
                      <td className="py-3 text-muted-foreground">{p.category?.name || "--"}</td>
                      <td className="py-3 text-right">₹{p.cost_price?.toLocaleString()}</td>
                      <td className="py-3 text-right">₹{p.selling_price?.toLocaleString()}</td>
                      <td className="py-3">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
                          p.is_active ? "bg-success/10 text-success" : "bg-muted text-muted-foreground"
                        }`}>
                          {p.is_active ? "Active" : "Inactive"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
