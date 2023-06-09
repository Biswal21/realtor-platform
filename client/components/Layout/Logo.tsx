import React from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/router";

const Logo = () => {
  return (
    <div className="absolute  left-1/2  mt-12 flex -translate-x-1/2 -translate-y-1/2 transform items-end">
      <Link href={`/`} passHref>
        <Image
          src="/shelterkart_final_logo.svg"
          alt="Shelterkart"
          objectFit="cover"
          width={200}
          height={50}
        />
      </Link>
    </div>
  );
};

export default Logo;
