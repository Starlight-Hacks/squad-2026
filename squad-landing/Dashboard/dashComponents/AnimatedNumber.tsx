"use-client"
import { useState, useEffect } from "react";

interface AnimatedProp{
    value: string;
    prefix?: string;
    suffix?: string
} 

export const AnimatedNumber = ({ value, prefix = "", suffix = "" }: AnimatedProp) => {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = parseInt(value, 10);
    if (start === end) return;
    
    let totalDuration = 1000; 
    let incrementTime = (totalDuration / end) * 50; 
    
    let timer = setInterval(() => {
      start += Math.ceil(end / 20);
      if (start >= end) {
        clearInterval(timer);
        setDisplayValue(end);
      } else {
        setDisplayValue(start);
      }
    }, incrementTime);
    
    return () => clearInterval(timer);
  }, [value]);

  return <span>{prefix}{displayValue.toLocaleString()}{suffix}</span>;
};