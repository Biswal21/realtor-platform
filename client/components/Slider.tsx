import React, { useEffect, useRef } from "react";
import Image from "next/image";
import { YoutubeEmbed } from "./YoutubeEmbed";

const Slider: React.FC<{
  images: string[];
  videos: string[];
  autonext: boolean;
}> = ({ images, videos, autonext }) => {
  const [currentIndex, setCurrentIndex] = React.useState(0);
  let count = 0;

  const slideRef = useRef<any>();
  const ytRef = useRef<any>();
  // const nextRef = useRef<any>();
  // const prevRef = useRef<any>();

  const handleOnPrevClick = () => {
    count =
      (currentIndex + (images.length + videos.length) - 1) %
      (images.length + videos.length);
    setCurrentIndex(count);
    slideRef.current.classList.add("left-anim");
  };

  const handleOnNextClick = () => {
    count = (currentIndex + 1) % (images.length + videos.length);
    setCurrentIndex(count);
    console.log(count);
    console.log(slideRef.current, count);
    slideRef.current.classList.add("right-anim");
  };

  const removeAnimation = () => {
    slideRef.current.classList.remove("right-anim");
    slideRef.current.classList.remove("left-anim");
  };

  var touchstartX = 0;
  var touchstartY = 0;
  var touchendX = 0;
  var touchendY = 0;

  const handleStartTouch = (e: any) => {
    touchstartX = e.changedTouches[0].screenX;
    touchstartY = e.changedTouches[0].screenY;
  };

  const handleEndTouch = (e: any) => {
    touchendX = e.changedTouches[0].screenX;
    touchendY = e.changedTouches[0].screenY;
    if (touchendX < touchstartX) {
      handleOnNextClick();
    } else if (touchendX > touchstartX) {
      handleOnPrevClick();
    }
  };

  useEffect(() => {
    //startSlider();

    const handleAutoNext = () => {
      const ytDiv = ytRef.current?.classList;
      if (ytDiv != undefined) {
        if (
          ytDiv != undefined &&
          !(
            ytDiv.contains("playing-mode") ||
            ytDiv.contains("paused-mode") ||
            ytDiv.contains("buffering-mode")
          )
        ) {
          handleOnNextClick();
        }
      } else {
        handleOnNextClick();
      }
    };
    if (autonext) {
      const slide = setTimeout(() => handleAutoNext(), 5000);
      return () => {
        clearTimeout(slide);
      };
    }

    if (slideRef && slideRef.current) {
      slideRef.current.addEventListener("animationend", removeAnimation);
    }
  }, [handleOnNextClick]);
  return (
    <div>
      <div
        className="relative w-full select-none"
        ref={slideRef}
        onTouchStart={handleStartTouch}
        onTouchEnd={handleEndTouch}
      >
        <div className="relative aspect-video">
          {currentIndex < images.length ? (
            <Image
              src={images[currentIndex]}
              alt="property listing"
              layout="fill"
            />
          ) : videos.length ? (
            <YoutubeEmbed
              url={videos[currentIndex - images.length]}
              ref={ytRef}
            />
          ) : (
            <div className="relative flex aspect-video items-center justify-center bg-slate-500">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-20 w-20"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
          )}
        </div>
        <div className="absolute top-1/2 flex w-full -translate-y-1/2 transform items-center justify-between px-3">
          <button
            type="button"
            className="group absolute top-0 left-0 z-30 flex h-full cursor-pointer items-center justify-center px-4 focus:outline-none"
            onClick={handleOnPrevClick}
          >
            <span className="inline-flex h-16 w-16 items-center justify-start rounded-full group-focus:outline-none">
              <svg
                className="h-8 w-8 text-white focus:outline-none dark:text-gray-800"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M15 19l-7-7 7-7"
                ></path>
              </svg>
              <span className="hidden">Previous</span>
            </span>
          </button>
          <button
            type="button"
            className="group absolute top-0 right-0 flex h-full cursor-pointer items-center justify-center px-4 focus:outline-none"
            onClick={handleOnNextClick}
          >
            <span className="inline-flex h-16 w-16 items-center justify-end rounded-full group-focus:outline-none">
              <svg
                className="h-8 w-8 text-white focus:outline-none dark:text-gray-800"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 5l7 7-7 7"
                ></path>
              </svg>
              <span className="hidden">Next</span>
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Slider;
