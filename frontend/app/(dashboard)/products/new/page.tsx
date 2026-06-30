"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Sparkles, Hash } from "lucide-react";

const CATEGORIES = ["Composite", "Gloves", "Handpiece", "Impression Material", "Endodontics", "Restorative", "Cement", "Bonding Agent", "Etchant", "Bur", "Implant", "Orthodontics", "Instrument", "Mirror", "Scaler", "PPE", "Needle", "Syringe", "Suture", "General"];
const BRANDS = ["3M", "GC", "Dentsply Sirona", "NSK", "Woodpecker", "Mani", "Ivoclar", "Kerr", "Septodont", "Zhermack", "DPI", "Coltene", "Ultradent", "Bisco", "Kuraray", "Shofu", "Voco", "DMG"];
const SHADES = ["", "A1", "A2", "A3", "A3.5", "A4", "B1", "B2", "B3", "C1", "C2", "D2", "Incisal", "Bleach", "Transparent"];
const SIZES = ["", "S", "M", "L", "XL", "XXL"];
const LENGTHS = ["", "21", "25", "28", "31"];

export default function NewProductPage() {
  const router = useRouter();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [category, setCategory] = useState("");
  const [brand, setBrand] = useState("");
  const [variant, setVariant] = useState("");
  const [previewSku, setPreviewSku] = useState("");
  const [skuGenerating, setSkuGenerating] = useState(false);

  useEffect(() => {
    if (!category || !brand) { setPreviewSku(""); return; }
    setSkuGenerating(true);
    const t = setTimeout(async () => {
      try {
        const r = await apiClient.post<{ data: { sku: string } }>("/api/v1/sku/preview", { category_name: category, brand_name: brand, variant: variant || undefined });
        setPreviewSku(r.data?.sku || "");
      } catch {}
      setSkuGenerating(false);
    }, 300);
    return () => clearTimeout(t);
  }, [category, brand, variant]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); setSaving(true); setError("");
    if (!category || !brand) { setError("Please select a Category and Brand"); setSaving(false); return; }
    const form = new FormData(e.currentTarget);
    const name = ((form.get("name") as string) || "").trim();
    if (!name) { setError("Product name is required"); setSaving(false); return; }
    const manualSku = ((form.get("sku") as string) || "").trim();
    const body = {
      sku: manualSku || previewSku,
      name,
      category_name: category, brand_name: brand,
      cost_price: parseFloat(form.get("cost_price") as string) || 0,
      selling_price: parseFloat(form.get("selling_price") as string) || 0,
      gst_rate: parseFloat(form.get("gst_rate") as string) || 18,
      is_active: true,
    };
    try {
      await apiClient.post("/api/v1/products", body);
      router.push("/products");
    } catch (err: any) { setError(err.message); }
    setSaving(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="rounded-lg bg-primary/10 p-2"><Hash className="h-5 w-5 text-primary" /></div>
        <div><h1 className="text-2xl font-bold">New Product</h1><p className="text-muted-foreground">Smart SKU generation with live preview</p></div>
      </div>
      <Card className="max-w-2xl"><CardContent className="py-6">
        {error && <div className="mb-4 rounded-md bg-destructive/10 p-3 text-sm text-destructive">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <div><label className="text-sm font-medium">Category *</label><select className="w-full rounded-md border px-3 py-2 text-sm" value={category} onChange={e => setCategory(e.target.value)}><option value="">Select...</option>{CATEGORIES.map(c => <option key={c}>{c}</option>)}</select></div>
            <div><label className="text-sm font-medium">Brand *</label><select className="w-full rounded-md border px-3 py-2 text-sm" value={brand} onChange={e => setBrand(e.target.value)}><option value="">Select...</option>{BRANDS.map(b => <option key={b}>{b}</option>)}</select></div>
            <div><label className="text-sm font-medium">Variant</label><select className="w-full rounded-md border px-3 py-2 text-sm" value={variant} onChange={e => setVariant(e.target.value)}>
              <option value="">None</option><optgroup label="Shades">{SHADES.filter(s => s).map(s => <option key={s}>{s}</option>)}</optgroup><optgroup label="Sizes">{SIZES.filter(s => s).map(s => <option key={s}>{s}</option>)}</optgroup><optgroup label="Lengths">{LENGTHS.filter(s => s).map(s => <option key={s}>{s}</option>)}</optgroup>
            </select></div>
          </div>

          {previewSku && (
            <div className="rounded-lg border-2 border-primary/30 bg-primary/5 p-4">
              <div className="flex items-center gap-2 mb-1"><Sparkles className="h-4 w-4 text-primary" /><span className="text-xs font-medium text-primary uppercase">Auto-Generated SKU</span>{skuGenerating && <span className="text-xs text-muted-foreground animate-pulse">Updating...</span>}</div>
              <p className="text-2xl font-mono font-bold tracking-wider">{previewSku}</p>
              <p className="text-xs text-muted-foreground mt-1">Category: {category} · Brand: {brand} {variant ? `· Variant: ${variant}` : ""}</p>
            </div>
          )}

          <div><label className="text-sm font-medium">SKU</label><input name="sku" className="w-full rounded-md border px-3 py-2 text-sm font-mono" placeholder={previewSku || "Auto-generated or enter manually"} /><p className="text-xs text-muted-foreground mt-1">Leave blank to use auto-generated SKU. Admins may override.</p></div>

          <div><label className="text-sm font-medium">Product Name *</label><input name="name" required className="w-full rounded-md border px-3 py-2 text-sm" placeholder="e.g., Filtek Z350 XT Composite A2" /></div>

          <div className="grid grid-cols-3 gap-4">
            <div><label className="text-sm font-medium">Cost Price (₹)</label><input name="cost_price" type="number" step="0.01" className="w-full rounded-md border px-3 py-2 text-sm" /></div>
            <div><label className="text-sm font-medium">Selling Price (₹)</label><input name="selling_price" type="number" step="0.01" className="w-full rounded-md border px-3 py-2 text-sm" /></div>
            <div><label className="text-sm font-medium">GST (%)</label><input name="gst_rate" type="number" defaultValue={18} className="w-full rounded-md border px-3 py-2 text-sm" /></div>
          </div>

          <Button type="submit" disabled={saving}>{saving ? "Creating..." : "Create Product"}</Button>
        </form>
      </CardContent></Card>
    </div>
  );
}
