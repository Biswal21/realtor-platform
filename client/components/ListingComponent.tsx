// import Link from "next/link";
import React from "react";
import { ListingData, ListingImage, PropertyUSP } from "../types/interfaces";
import Slider from "./Slider";
import Link from "next/link";

const ListingComponent: React.FC<{
  listing: ListingData;
}> = ({ listing }) => {
  let images: any = [];
  let videos: any = [];
  listing?.listing_image
    ? (images = listing?.listing_image.map((image: ListingImage) => {
        return image.name;
      }))
    : (images = []);
  listing?.listing_video
    ? (videos = listing?.listing_video.map((video: ListingImage) => {
        return video.name;
      }))
    : (videos = []);

  return (
    <>
      <div className="card mx-4 mt-4">
        <Slider images={images} videos={videos} autonext={false} />
      </div>
      <div className="card mx-4 mt-4">
        <div className="px-5 py-5">
          <div className="border-b-2 border-slate-200 pb-3">
            <div className="text-2xl font-bold text-gray-900 dark:text-white">
              {listing.name}
            </div>
            {listing.dealer_approved === true ? (
              <div className="flex content-center items-center justify-end text-lg text-red-700">
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
                <span>Approved</span>
              </div>
            ) : null}
            <div className="flex justify-between">
              <div>
                <div className="py-3 text-sm font-medium text-slate-400 underline decoration-slate-400">
                  {listing.fk_region !== undefined
                    ? `${listing.fk_region?.name}, `
                    : null}
                  {listing.fk_region?.city}
                </div>
              </div>
              <div className="flex content-center items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
                <div className="font-medium text-gray-900">
                  {listing.fk_builder !== undefined ? (
                    <Link
                      href={{
                        pathname: `/region/${listing?.fk_region?.id}`,
                        query: { builder: listing?.fk_builder?.name },
                      }}
                      passHref={true}
                    >
                      {listing.fk_builder?.name}
                    </Link>
                  ) : (
                    "Builder information not available"
                  )}
                </div>
              </div>
            </div>
          </div>
          <div className="py-7">
            <div className="text-xl font-semibold">Property USP</div>
            <div className="py-4">
              {listing?.property_usp?.length > 0 && (
                <ul className="list-none">
                  {listing?.property_usp.map((amenity: PropertyUSP) => (
                    <li key={amenity.id} className="flex items-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="h-6 w-6 text-lg font-medium"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M16.5 3.75V16.5L12 14.25 7.5 16.5V3.75m9 0H18A2.25 2.25 0 0120.25 6v12A2.25 2.25 0 0118 20.25H6A2.25 2.25 0 013.75 18V6A2.25 2.25 0 016 3.75h1.5m9 0h-9"
                        />
                      </svg>
                      <div className="pl-2">{amenity.name}</div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ListingComponent;
