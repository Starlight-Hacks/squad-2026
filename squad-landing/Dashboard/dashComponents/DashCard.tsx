import { ReactNode } from "react";

interface DashProps{
    children: ReactNode
    className?: string;
    noPadding?: boolean
}

export const DashCard = ({ children, className = "", noPadding = false }: DashProps) => (
  <div className={`bg-white border border-gray-200 rounded-xl shadow-sm ${noPadding ? '' : 'p-6'} ${className}`}>
    {children}
  </div>
);