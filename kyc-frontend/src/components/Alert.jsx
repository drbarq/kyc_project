import React from "react";
import { AlertCircle, CheckCircle } from "lucide-react";

export const Alert = ({ children, variant = "error" }) => {
  const isError = variant === "error";

  return (
    <div
      className={`p-4 rounded-lg flex items-start space-x-3 ${
        isError ? "bg-red-50 text-red-700" : "bg-green-50 text-green-700"
      }`}
    >
      {isError ? (
        <AlertCircle className="h-5 w-5 flex-shrink-0" />
      ) : (
        <CheckCircle className="h-5 w-5 flex-shrink-0" />
      )}
      <div className="flex-1">{children}</div>
    </div>
  );
};
