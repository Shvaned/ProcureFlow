"use client";

import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { create } from "zustand";

interface User {
  id: string;
  email: string;
  name: string;
  roles: string[];
  permissions: string[];
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setTokens: (access: string, refresh: string) => void;
}

function loadAuth(): Partial<AuthState> {
  if (typeof window === "undefined") return {};
  try {
    const raw = localStorage.getItem("auth-storage");
    if (raw) {
      const parsed = JSON.parse(raw);
      const s = parsed?.state;
      if (s?.accessToken) return { user: s.user, accessToken: s.accessToken, refreshToken: s.refreshToken, isAuthenticated: true };
    }
  } catch { return {}; }
  return {};
}

function saveAuth(state: { user: User | null; accessToken: string | null; refreshToken: string | null }) {
  if (typeof window === "undefined") return;
  localStorage.setItem("auth-storage", JSON.stringify({
    state: { user: state.user, accessToken: state.accessToken, refreshToken: state.refreshToken },
  }));
}

function clearAuth() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("auth-storage");
}

export const useAuthStore = create<AuthState>((set) => ({
  ...loadAuth(),
  isLoading: false,
  login: async (email: string, password: string) => {
    set({ isLoading: true });
    try {
      const response = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) throw new Error("Login failed");
      const data = await response.json();
      const newState = {
        user: data.data.user,
        accessToken: data.data.access_token,
        refreshToken: data.data.refresh_token,
        isAuthenticated: true,
        isLoading: false,
      };
      set(newState);
      saveAuth(newState);
    } catch {
      set({ isLoading: false });
      throw new Error("Login failed");
    }
  },
  logout: () => {
    clearAuth();
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    });
  },
  setTokens: (access: string, refresh: string) => {
    set({ accessToken: access, refreshToken: refresh });
  },
}));

export function useAuth() {
  return useAuthStore();
}
