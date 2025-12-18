# Error Handling Usage Guide

This guide explains how to use the animated error feedback system in your React components.

## 🎨 Features

### 1. Shake Animation
- Elements shake left-right when errors occur
- Keyframe: `x: [0, -8, 8, -8, 8, 0]`
- Duration: 0.4s with easeInOut

### 2. Glow Feedback
- Soft orange glow (#fca65a) around invalid inputs
- Border changes to error color
- Shadow: `0_0_10px_#fca65a40`

### 3. Error Messages
- Fade in with slide-up animation
- Subtle opacity and y-axis transition
- Duration: 0.3s

## 📦 Components Available

### ErrorToast
Displays floating error messages at the top of the screen.

**Usage:**
```tsx
import ErrorToast from "@/components/ErrorToast";

const [showError, setShowError] = useState(false);
const [errorMessage, setErrorMessage] = useState("");

<ErrorToast 
  message={errorMessage}
  isVisible={showError}
  onClose={() => setShowError(false)}
/>
```

### SuccessToast
Displays floating success messages at the top of the screen.

**Usage:**
```tsx
import SuccessToast from "@/components/SuccessToast";

const [showSuccess, setShowSuccess] = useState(false);

<SuccessToast 
  message="Action completed successfully!"
  isVisible={showSuccess}
  onClose={() => setShowSuccess(false)}
/>
```

## 🔧 Form Input Error Handling

### Complete Example

```tsx
import { useState } from "react";
import { motion } from "framer-motion";
import { Input } from "@/components/ui/input";

const MyForm = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [fieldError, setFieldError] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    setFieldError(false);

    // Validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setFieldError(true);
      setError("Please enter a valid email address.");
      return;
    }

    // Submit form...
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Error Message Banner */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="mb-4 p-3 rounded-xl bg-[#fca65a]/10 border border-[#fca65a]/30"
        >
          <p className="text-[#fca65a] text-sm flex items-center gap-2">
            <span>⚠️</span>
            <span>{error}</span>
          </p>
        </motion.div>
      )}

      {/* Input Field with Shake Animation */}
      <motion.div
        animate={fieldError ? { x: [0, -4, 4, -4, 4, 0] } : {}}
        transition={{ duration: 0.3 }}
      >
        <Input
          type="email"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
            setFieldError(false);
            setError("");
          }}
          className={`transition-all ${
            fieldError
              ? "border-[#fca65a] shadow-[0_0_10px_#fca65a40] focus:border-[#fca65a] focus:ring-2 focus:ring-[#fca65a]/30"
              : "border-primary/20 focus:border-primary focus:ring-2 focus:ring-primary/30"
          }`}
        />
      </motion.div>
    </form>
  );
};
```

## 🎨 Color Palette

All error colors are consistent with the pastel theme:

- **Error Color**: `#fca65a` (soft orange)
- **Error Background**: `#fca65a` with 10% opacity
- **Error Border**: `#fca65a` with 30% opacity
- **Error Glow**: `#fca65a` with 25% opacity (40 in hex)
- **Primary Accent**: `#FDB87D`
- **Text**: `#3B3B3B`

## 💡 Best Practices

1. **Clear errors on input change**: Reset error states when users start typing
2. **Use subtle animations**: Keep shake distance small (4-8px)
3. **Auto-dismiss toasts**: Consider auto-hiding success toasts after 3-5s
4. **Validation timing**: Validate on submit, not on blur (less annoying)
5. **Specific error messages**: Be clear about what's wrong and how to fix it

## 🚀 Integration with Existing Components

The error handling is already integrated into:
- ✅ Login page (`/login`)
- ✅ Signup page (`/signup`)

To add to other pages:
1. Import the toast components
2. Add state for error/success messages
3. Use motion.div with shake animation for form fields
4. Add conditional styling for error states
