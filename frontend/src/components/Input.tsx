'use client';

import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

export default function Input({
  label,
  error,
  icon,
  className = '',
  ...props
}: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        {icon && (
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
            {icon}
          </div>
        )}
        <input
          className={`
            w-full px-4 py-3 rounded-xl border-2 transition-all duration-200
            ${icon ? 'pl-12' : ''}
            ${error
              ? 'border-danger-500 focus:border-danger-600 focus:ring-4 focus:ring-danger-100'
              : 'border-gray-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-100'
            }
            outline-none
            ${className}
          `}
          {...props}
        />
      </div>
      {error && (
        <p className="mt-2 text-sm text-danger-600 animate-slide-down">
          {error}
        </p>
      )}
    </div>
  );
}
