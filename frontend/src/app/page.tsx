'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { Smartphone, Shield, Users, TrendingUp } from 'lucide-react';
import Link from 'next/link';
import Button from '@/components/Button';

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      if (user.role === 'admin') {
        router.push('/admin');
      } else if (user.role === 'retailer') {
        router.push('/retailer');
      } else {
        router.push('/citizen');
      }
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-72 h-72 bg-primary-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
          <div className="absolute top-40 right-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
          <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>
        </div>

        {/* Content */}
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-semibold mb-8 animate-slide-down">
              <Shield className="w-4 h-4" />
              <span>Secure & Reliable Mobile Tracking</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-slide-up">
              Protect Your{' '}
              <span className="gradient-text">Mobile Devices</span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
              A comprehensive system to prevent mobile phone theft and track stolen devices through a collaborative ecosystem of citizens, retailers, and law enforcement.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <Link href="/signup">
                <Button size="lg" className="w-full sm:w-auto">
                  Get Started
                </Button>
              </Link>
              <Link href="/login">
                <Button variant="outline" size="lg" className="w-full sm:w-auto">
                  Sign In
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Why Choose Our System?</h2>
          <p className="text-gray-600 text-lg">Built with cutting-edge technology for maximum security</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {[
            {
              icon: <Smartphone className="w-8 h-8" />,
              title: 'Device Registration',
              description: 'Register your mobile devices with IMEI and track ownership history',
              color: 'primary',
            },
            {
              icon: <Shield className="w-8 h-8" />,
              title: 'Theft Prevention',
              description: 'Report lost or snatched phones and get instant alerts',
              color: 'success',
            },
            {
              icon: <Users className="w-8 h-8" />,
              title: 'Retailer Network',
              description: 'Retailers verify devices before purchase to prevent stolen goods',
              color: 'warning',
            },
            {
              icon: <TrendingUp className="w-8 h-8" />,
              title: 'Smart Matching',
              description: 'Automated IMEI matching to identify stolen devices',
              color: 'danger',
            },
          ].map((feature, index) => (
            <div
              key={index}
              className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 group animate-scale-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className={`w-16 h-16 bg-${feature.color}-100 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform text-${feature.color}-600`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8 text-center text-white">
            {[
              { number: '10,000+', label: 'Registered Devices' },
              { number: '500+', label: 'Verified Retailers' },
              { number: '95%', label: 'Recovery Rate' },
            ].map((stat, index) => (
              <div key={index} className="animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="text-5xl font-bold mb-2">{stat.number}</div>
                <div className="text-primary-100 text-lg">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        <h2 className="text-4xl font-bold mb-6">Ready to Secure Your Device?</h2>
        <p className="text-xl text-gray-600 mb-8">
          Join thousands of users protecting their mobile devices today
        </p>
        <Link href="/signup">
          <Button size="lg">
            Create Free Account
          </Button>
        </Link>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-4">Mobile Tracking System</h3>
            <p className="text-gray-400 mb-4">
              Protecting your devices, one registration at a time.
            </p>
            <p className="text-gray-500 text-sm">
              © 2024 Mobile Tracking System. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
