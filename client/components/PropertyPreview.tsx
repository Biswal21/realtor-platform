import Link from "next/link";
import Image from "next/image";
import React from "react";
import { ListingData } from "../types/interfaces";

const PropertyPreview: React.FC<{
  item: ListingData;
  key: number | null | undefined;
}> = ({ item, key }) => {
  return (
    <Link href={`/listing/${item.id}/`} key={key} passHref>
      <div className="card mx-4 mb-4 flex w-full cursor-pointer flex-wrap">
        <div className="relative h-48 w-full overflow-hidden ">
          {item?.display_image !== null ? (
            <Image
              src={item.display_image}
              alt={item.name}
              layout="fill"
              objectFit="cover"
            />
          ) : (
            <Image
              src="/placeholder.webp"
              alt={item.name}
              layout="fill"
              objectFit="cover"
            />
          )}
        </div>
        <div className="mt-2 mb-6 ml-4 flex h-10 w-full justify-between  text-lg text-gray-900 dark:text-gray-300">
          <div>
            <div className="text-sm font-light">{item?.fk_builder?.name}</div>
            <div className="font-semibold ">{item?.name}</div>
          </div>
          {item?.dealer_approved === true ? (
            <div className="mr-2 flex items-center justify-end text-lg text-red-700">
              <span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="p h-6 w-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </span>
            </div>
          ) : null}
        </div>
      </div>
    </Link>
  );
};

export default PropertyPreview;
