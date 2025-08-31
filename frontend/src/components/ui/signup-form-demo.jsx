"use client";
import React from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import {
  IconBrandGithub,
  IconBrandGoogle,
  IconBrandOnlyfans,
  IconExclamationCircle,
} from "@tabler/icons-react";

export default function SignupFormDemo({ onSuccess }) {
  const [isLoading, setIsLoading] = React.useState(false);
  const [passwordError, setPasswordError] = React.useState("");
  const [formData, setFormData] = React.useState({
    firstname: '',
    lastname: '',
    email: '',
    password: '',
    confirmpassword: ''
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    });
    
    // Clear password error when user types in either password field
    if (e.target.id === 'password' || e.target.id === 'confirmpassword') {
      setPasswordError("");
    }
  };

  const validatePasswords = () => {
    if (formData.password && formData.confirmpassword && formData.password !== formData.confirmpassword) {
      setPasswordError("Password doesn't match");
      return false;
    }
    setPasswordError("");
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate passwords first
    if (!validatePasswords()) {
      return;
    }
    
    // Basic validation
    if (!formData.firstname || !formData.lastname || !formData.email || !formData.password || !formData.confirmpassword) {
      alert('Please fill in all fields');
      return;
    }

    if (formData.password.length < 6) {
      alert('Password must be at least 6 characters long');
      return;
    }

    setIsLoading(true);

    // Simulate API call
    setTimeout(() => {
      console.log("Signup form submitted", formData);
      setIsLoading(false);
      if (onSuccess) {
        onSuccess();
      }
    }, 1000);
  };
  return (
    <div className="shadow-input mx-auto w-full max-w-md rounded-none bg-black p-4 md:rounded-2xl md:p-8">
      <h2 className="text-xl font-bold text-white">
        Welcome to WorkBee
      </h2>
      <p className="mt-2 max-w-sm text-sm text-gray-300">
        Login to WorkBee to access your personalized job dashboard
      </p>

      <form className="my-8" onSubmit={handleSubmit}>
        <div className="mb-4 flex flex-col space-y-2 md:flex-row md:space-y-0 md:space-x-2">
          <LabelInputContainer>
            <Label htmlFor="firstname" className="text-white">First name</Label>
            <Input 
              id="firstname" 
              placeholder="Alex" 
              type="text" 
              value={formData.firstname}
              onChange={handleInputChange}
              required
            />
          </LabelInputContainer>
          <LabelInputContainer>
            <Label htmlFor="lastname" className="text-white">Last name</Label>
            <Input 
              id="lastname" 
              placeholder="Wiliams" 
              type="text" 
              value={formData.lastname}
              onChange={handleInputChange}
              required
            />
          </LabelInputContainer>
        </div>
        <LabelInputContainer className="mb-4">
          <Label htmlFor="email" className="text-white">Email Address</Label>
          <Input 
            id="email" 
            placeholder="example@gmail.com" 
            type="email" 
            value={formData.email}
            onChange={handleInputChange}
            required
          />
        </LabelInputContainer>
        <LabelInputContainer className="mb-4">
          <Label htmlFor="password" className="text-white">Password</Label>
          <Input 
            id="password" 
            placeholder="••••••••" 
            type="password" 
            value={formData.password}
            onChange={handleInputChange}
            required
          />
        </LabelInputContainer>
        <LabelInputContainer className="mb-2">
          <Label htmlFor="confirmpassword" className="text-white">Confirm Password</Label>
          <Input
            id="confirmpassword"
            placeholder="••••••••"
            type="password"
            value={formData.confirmpassword}
            onChange={handleInputChange}
            onBlur={validatePasswords}
            required
          />
          {passwordError && (
            <div className="flex items-center space-x-2 text-red-500 text-sm mt-1">
              <IconExclamationCircle className="w-4 h-4" />
              <span>{passwordError}</span>
            </div>
          )}
        </LabelInputContainer>

        <button
          className="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-black to-neutral-600 font-medium text-white shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-zinc-800 dark:from-zinc-900 dark:to-zinc-900 dark:shadow-[0px_1px_0px_0px_#27272a_inset,0px_-1px_0px_0px_#27272a_inset] disabled:opacity-50 disabled:cursor-not-allowed"
          type="submit"
          disabled={isLoading}
        >
          {isLoading ? "Creating account..." : "Sign up"}
          <BottomGradient />
        </button>

        <div className="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-300 to-transparent dark:via-neutral-700" />

        
      </form>
    </div>
  );
}

const BottomGradient = () => {
  return (
    <>
      <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
      <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
    </>
  );
};

const LabelInputContainer = ({
  children,
  className,
}) => {
  return (
    <div className={cn("flex w-full flex-col space-y-2", className)}>
      {children}
    </div>
  );
};
