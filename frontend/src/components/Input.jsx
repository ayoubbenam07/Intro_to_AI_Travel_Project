import { forwardRef } from "react";

/**
 * Input component — white background, design-system tokens.
 *
 * Props:
 *   label       – optional label above the input
 *   helperText  – optional helper / error text below
 *   icon        – optional ReactNode rendered as a left icon
 *   size        – "sm" | "md" (default) | "lg"
 *   error       – boolean, applies error styling
 *   className   – extra classes on the outer wrapper
 *   inputClassName – extra classes on the <input> itself
 *   ...rest     – forwarded to the native <input>
 *
 * Usage:
 *   <Input label="Email" placeholder="you@example.com" />
 *   <Input icon={<SearchIcon />} placeholder="Search" />
 *   <Input error helperText="This field is required" />
 */
const Input = forwardRef(function Input(
  {
    label,
    helperText,
    icon,
    size = "md",
    error = false,
    className = "",
    inputClassName = "",
    id,
    ...rest
  },
  ref
) {
  const sizeClass = size === "sm" ? "input-sm" : size === "lg" ? "input-lg" : "";

  const inputEl = (
    <input
      ref={ref}
      id={id}
      className={`input ${sizeClass} ${inputClassName}`.trim()}
      {...rest}
    />
  );

  return (
    <div className={`${error ? "input-error" : ""} ${className}`.trim()}>
      {label && (
        <label htmlFor={id} className="input-label">
          {label}
        </label>
      )}

      {icon ? (
        <div className="input-wrapper">
          {inputEl}
          <span className="input-icon">{icon}</span>
        </div>
      ) : (
        inputEl
      )}

      {helperText && <p className="input-helper">{helperText}</p>}
    </div>
  );
});

export default Input;
