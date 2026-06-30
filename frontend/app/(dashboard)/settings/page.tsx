"use client";
import { Card, CardContent } from "@/components/ui/card";
import { Settings } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-muted-foreground">System configuration and preferences</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {[
          { title: "General", desc: "Application name, version, environment" },
          { title: "Security", desc: "JWT configuration, password policy, rate limits" },
          { title: "AI Configuration", desc: "OpenRouter API key, default model, fallback model" },
          { title: "Database", desc: "Neon PostgreSQL connection, pooling, migrations" },
        ].map(({ title, desc }) => (
          <Card key={title}>
            <CardContent className="py-6">
              <Settings className="mb-2 h-5 w-5 text-muted-foreground" />
              <h3 className="font-semibold">{title}</h3>
              <p className="text-sm text-muted-foreground">{desc}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
