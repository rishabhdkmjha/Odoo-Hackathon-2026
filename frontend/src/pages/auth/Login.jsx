import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { Eye, EyeOff, LogIn } from 'lucide-react';
import useAuth from '../../hooks/useAuth.js';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [serverError, setServerError] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({ defaultValues: { email: '', password: '' } });

  const onSubmit = async (formValues) => {
    setServerError('');
    try {
      await login(formValues);
      navigate('/dashboard');
    } catch (err) {
      setServerError(
        err?.response?.data?.message || 'Invalid email or password. Please try again.'
      );
    }
  };

  return (
    <div>
      <h2 className="font-display text-2xl font-semibold text-ink mb-1">Welcome back</h2>
      <p className="text-sm text-ink-muted mb-8">Log in to your AssetFlow workspace.</p>

      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
        <div>
          <label htmlFor="email" className="label">
            Work email
          </label>
          <input
            id="email"
            type="email"
            autoComplete="email"
            placeholder="you@company.com"
            className="input"
            {...register('email', {
              required: 'Email is required',
              pattern: { value: /^\S+@\S+\.\S+$/, message: 'Enter a valid email address' },
            })}
          />
          {errors.email && (
            <p className="text-xs text-status-lost mt-1.5">{errors.email.message}</p>
          )}
        </div>

        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label htmlFor="password" className="label mb-0">
              Password
            </label>
            <Link to="/forgot-password" className="text-xs font-medium text-brand-500 hover:text-brand-600">
              Forgot password?
            </Link>
          </div>
          <div className="relative">
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              placeholder="••••••••"
              className="input pr-10"
              {...register('password', { required: 'Password is required' })}
            />
            <button
              type="button"
              onClick={() => setShowPassword((v) => !v)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-soft hover:text-ink-muted"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          </div>
          {errors.password && (
            <p className="text-xs text-status-lost mt-1.5">{errors.password.message}</p>
          )}
        </div>

        {serverError && (
          <div className="rounded-md bg-red-50 border border-red-100 px-3 py-2.5 text-sm text-status-lost">
            {serverError}
          </div>
        )}

        <button type="submit" disabled={isSubmitting} className="btn-primary w-full mt-2">
          {isSubmitting ? 'Signing in...' : (
            <>
              <LogIn size={16} /> Log In
            </>
          )}
        </button>
      </form>

      <p className="text-sm text-ink-muted text-center mt-6">
        New to AssetFlow?{' '}
        <Link to="/signup" className="font-medium text-brand-500 hover:text-brand-600">
          Create an Employee account
        </Link>
      </p>
      <p className="text-xs text-ink-soft text-center mt-2">
        Roles like Department Head and Asset Manager are assigned by an Administrator
        after signup — not chosen here.
      </p>
    </div>
  );
}
