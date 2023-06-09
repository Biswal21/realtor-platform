import "../styles/globals.css";
import type { AppProps } from "next/app";
import { ThemeProvider } from "next-themes";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Footer from "../components/Layout/Footer";

function MyApp({ Component, pageProps }: AppProps) {
  // TODO: remove inline styles
  return (
    <ThemeProvider enableSystem={true} attribute="class">
      <ToastContainer
        position="top-center"
        autoClose={5000}
        hideProgressBar
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        closeButton={false}
      />
      <Component {...pageProps} />
    </ThemeProvider>
  );
}

export default MyApp;
