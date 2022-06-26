import React, { useState } from "react";
import { AssetKeyT } from "../../hooks/oracle";

/**
 * Returns name of the logo's image.
 * @param {AssetKeyT} assetKey string containing the coin abbreviation delimited by a '/'
 * @return {string} returns string that matches corresponding file name in /assets/logos
 */
function getLogo(assetKey: AssetKeyT): string {
  const indexOfSlash = assetKey.indexOf("/");
  return indexOfSlash > 0
    ? assetKey.slice(0, indexOfSlash).toLowerCase()
    : "fallback";
}

interface AssetLogoProps {
  assetKey: AssetKeyT;
  className: string;
}

const AssetLogo: React.FC<AssetLogoProps> = ({ assetKey, className }) => {
  // The error state here is needed to prevent an infinite loop if 'fallback.svg' doesn't exist.
  // This stops the browser from sending GET requests.
  const [isError, setIsError] = useState(false);
  const logoString = getLogo(assetKey);
  return (
    <img
      src={
        isError
          ? "/assets/currencies/fallback.svg"
          : `/assets/currencies/${logoString}.svg`
      }
      alt={`${logoString} logo`}
      className={className}
      onError={() => setIsError(true)}
    />
  );
};

export default AssetLogo;
