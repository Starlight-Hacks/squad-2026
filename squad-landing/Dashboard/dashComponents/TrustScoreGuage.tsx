"use-client"
import {useState, useEffect} from "react"

interface TrustScoreProp{
  score: number
}

export const TrustScoreGauge = ({ score }: TrustScoreProp) => {
  const [currentScore, setCurrentScore] = useState(0);
  
  useEffect(() => {
    setTimeout(() => setCurrentScore(score), 100);
  }, [score]);

  const circumference = 2 * Math.PI * 40;
  const strokeDashoffset = circumference - (currentScore / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center w-32 h-32">
      <svg className="w-full h-full transform -rotate-90">
        <circle cx="64" cy="64" r="40" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-gray-100" />
        <circle 
          cx="64" cy="64" r="40" stroke="currentColor" strokeWidth="8" fill="transparent" 
          className="text-blue-600 transition-all duration-1000 ease-out"
          style={{ strokeDasharray: circumference, strokeDashoffset }}
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center mt-1">
        <span className="text-3xl font-bold text-gray-900 tracking-tight">{currentScore}</span>
        <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-widest">Score</span>
      </div>
    </div>
  );
};