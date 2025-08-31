"use client";
import React, { useState } from "react";
import { cn } from "@/lib/utils";
import LoginFormDemo from "./login-form-demo";
import SignupFormDemo from "./signup-form-demo";

export default function AuthModal({ isOpen, onClose, onSuccess }) {
  const [isLogin, setIsLogin] = useState(true);

  if (!isOpen) return null;

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleFormSuccess = () => {
    onSuccess();
    onClose();
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm"
      onClick={handleBackdropClick}
    >
      <div className="relative w-full max-w-md mx-4">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute -top-4 -right-4 z-10 w-8 h-8 bg-white dark:bg-black rounded-full flex items-center justify-center shadow-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          <svg
            className="w-5 h-5 text-gray-600 dark:text-gray-300"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>

        {/* Form container */}
        <div className="relative">
          {isLogin ? <LoginFormDemo onSuccess={handleFormSuccess} /> : <SignupFormDemo onSuccess={handleFormSuccess} />}
          
          {/* Toggle between login and signup */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600 dark:text-gray-300">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
              >
                {isLogin ? "Sign up" : "Sign in"}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
