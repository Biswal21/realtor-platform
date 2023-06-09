import React, { useEffect } from "react";
import PropTypes from "prop-types";

export const YoutubeEmbed = React.forwardRef((props: any, ref: any) => {
  useEffect(() => {
    if (!window.YT) {
      const tag = document.createElement("script");
      tag.src = "https://www.youtube.com/iframe_api";
      window.onYouTubeIframeAPIReady = loadVideo;
      const firstScriptTag = document.getElementsByTagName("script")[0];
      firstScriptTag.parentNode?.insertBefore(tag, firstScriptTag);
    } else loadVideo();
  }, []);

  const loadVideo = () => {
    const player = new window.YT.Player("player", {
      videoId: getIdFromUrl(props.url),
      height: "100%",
      width: "100%",
      playerVars: {
        autoplay: 0,
      },
      events: {
        // onReady: onPlayerReady,
        onStateChange: onPlayerStateChange,
      },
    });
  };

  // const onPlayerReady = (event: any) => {
  //   console.log("onPlayerReady");
  //   event.target.playVideo();
  // };

  const onPlayerStateChange = (event: any) => {
    console.log(event.target, event.data);
    if (event.data === 1) {
      ref.current.classList.add("playing-mode");
      ref.current.classList.remove("buffering-mode");
      ref.current.classList.remove("paused-mode");      
    } else if (event.data === 3) {
      ref.current.classList.add("buffering-mode");
      ref.current.classList.remove("playing-mode");
      ref.current.classList.remove("paused-mode");
    } else if (event.data === 2) {
      ref.current.classList.add("paused-mode");
      ref.current.classList.remove("playing-mode");
      ref.current.classList.remove("buffering-mode");
    } else {
      ref.current.classList.remove("playing-mode");
      ref.current.classList.remove("buffering-mode");
      ref.current.classList.remove("paused-mode");
    }

  };
  // UNSTARTED-MODE
  // PLAYING-MODE
  // PAUSED-MODE
  return (
    <div className="video-responsive h-full w-full">
      <div id="player" ref={ref}>
      </div>
    </div>
  );
});

YoutubeEmbed.displayName = "YoutubeEmbed";

const getIdFromUrl = (url: any) => {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url?.match(regExp);
  return match && match[2].length === 11 ? match[2] : null;
};
