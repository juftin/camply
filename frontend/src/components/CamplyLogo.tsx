interface CamplyLogoProps {
  className?: string;
  width?: number;
  height?: number;
  variant?: "svg" | "png";
}

export function CamplyLogo({
  className = "",
  width = 32,
  height = 32,
  variant = "svg",
}: CamplyLogoProps) {
  if (variant === "png") {
    return (
      <img
        src="/camply-logo.png"
        alt="camply logo"
        width={width}
        height={height}
        className={className}
      />
    );
  }

  return (
    <img
      src="/camply-logo.svg"
      alt="camply logo"
      width={width}
      height={height}
      className={className}
    />
  );
}
