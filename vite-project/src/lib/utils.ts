import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
export const cn1 = (...classes: (string | boolean | undefined)[]) => {
  return classes.filter(Boolean).join(" ");
};

export const placeholderImage = (text = "Image") =>
  `https://placehold.co/600x400/1a1a1a/ffffff?text=${text}`;

