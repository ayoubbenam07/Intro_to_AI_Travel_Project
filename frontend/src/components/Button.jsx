/**
 * Button component with design-system variants.
 *
 * Variants : primary | secondary | inverted | outlined
 * Sizes    : sm | md (default) | lg
 *
 * Usage:
 *   <Button variant="primary">Click me</Button>
 *   <Button variant="outlined" size="lg" onClick={fn}>Submit</Button>
 */

export default function Button({
  children,
  variant = "primary",
  size = "md",
  className = "",
  disabled = false,
  type = "button",
  ...rest
}) {
  const sizeClass = size === "sm" ? "btn-sm" : size === "lg" ? "btn-lg" : "";

  return (
    <button
      type={type}
      disabled={disabled}
      className={`btn btn-${variant} ${sizeClass} ${className}`.trim()}
      {...rest}
    >
      {children}
    </button>
  );
}
