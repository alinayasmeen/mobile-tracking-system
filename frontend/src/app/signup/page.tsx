'use client';

import { useState } from 'react';
import { useAuth } from '@/lib/auth-context';
import { Mail, Lock, UserPlus, CreditCard, Building } from 'lucide-react';
import Link from 'next/link';
import Button from '@/components/Button';
import Input from '@/components/Input';
import Card from '@/components/Card';

export default function Signup() {
  const { signup } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    cnic: '',
    ntn: '',
    shop_address: '',
    role: 'citizen' as 'citizen' | 'retailer',
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<any>({});

  const validateForm = () => {
    const newErrors: any = {};

    if (formData.cnic.length !== 13 || !/^\d+$/.test(formData.cnic)) {
      newErrors.cnic = 'CNIC must be exactly 13 digits';
    }

    if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (formData.role === 'retailer' && !formData.ntn) {
      newErrors.ntn = 'NTN is required for retailer accounts';
    }

    if (formData.role === 'retailer' && !formData.shop_address.trim()) {
      newErrors.shop_address = 'Shop address is required for retailer accounts';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      await signup(formData);
    } catch (error) {
      // Error handled in context
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev: any) => ({ ...prev, [field]: '' }));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 py-12">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
        <div className="absolute bottom-20 right-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="relative w-full max-w-md animate-scale-in">
        <Card className="p-8">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-br from-success-500 to-success-700 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-success-500/30">
              <UserPlus className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold mb-2">Create Account</h1>
            <p className="text-gray-600">Join our mobile tracking system</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Role Selection */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                Account Type
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => handleChange('role', 'citizen')}
                  className={`p-4 rounded-xl border-2 transition-all ${
                    formData.role === 'citizen'
                      ? 'border-primary-500 bg-primary-50 text-primary-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <UserPlus className="w-6 h-6 mx-auto mb-2" />
                  <span className="font-semibold text-sm">Citizen</span>
                </button>
                <button
                  type="button"
                  onClick={() => handleChange('role', 'retailer')}
                  className={`p-4 rounded-xl border-2 transition-all ${
                    formData.role === 'retailer'
                      ? 'border-primary-500 bg-primary-50 text-primary-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Building className="w-6 h-6 mx-auto mb-2" />
                  <span className="font-semibold text-sm">Retailer</span>
                </button>
              </div>
            </div>

            <Input
              type="email"
              label="Email Address"
              placeholder="your@email.com"
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              icon={<Mail className="w-5 h-5" />}
              required
            />

            <Input
              type="password"
              label="Password"
              placeholder="Min. 8 characters"
              value={formData.password}
              onChange={(e) => handleChange('password', e.target.value)}
              icon={<Lock className="w-5 h-5" />}
              error={errors.password}
              required
            />

            <Input
              type="text"
              label="CNIC Number"
              placeholder="1234567890123"
              value={formData.cnic}
              onChange={(e) => handleChange('cnic', e.target.value.replace(/\D/g, '').slice(0, 13))}
              icon={<CreditCard className="w-5 h-5" />}
              error={errors.cnic}
              maxLength={13}
              required
            />

            {formData.role === 'retailer' && (
              <>
                <Input
                  type="text"
                  label="NTN Number"
                  placeholder="Business NTN"
                  value={formData.ntn}
                  onChange={(e) => handleChange('ntn', e.target.value)}
                  icon={<Building className="w-5 h-5" />}
                  error={errors.ntn}
                  required
                />
                <Input
                  type="text"
                  label="Shop Address"
                  placeholder="Enter your shop address"
                  value={formData.shop_address}
                  onChange={(e) => handleChange('shop_address', e.target.value)}
                  icon={<Building className="w-5 h-5" />}
                  error={errors.shop_address}
                  required
                />
              </>
            )}

            <Button type="submit" className="w-full" loading={loading}>
              Create Account
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link href="/login" className="text-primary-600 font-semibold hover:text-primary-700">
                Sign in
              </Link>
            </p>
          </div>

          <div className="mt-4 text-center">
            <Link href="/" className="text-sm text-gray-500 hover:text-gray-700">
              ← Back to home
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
