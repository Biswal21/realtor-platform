import axios from "axios";
import type { GetStaticProps, NextPage } from "next";
import { CityData } from "../types/interfaces";
import Link from "next/link";
import Image from "next/image";
import Sidebar from "../components/Layout/Sidebar";
import { useEffect, useState } from "react";
import Logo from "../components/Layout/Logo";
import Footer from "../components/Layout/Footer";
// import { useRouter } from "next/router";

const Home: React.FC<{ cities: CityData[] | []; Link: NextPage }> = ({
  cities,
}) => {
  const [moreHeight, setHeight] = useState<Boolean>(false);
  useEffect(() => {
    const checkHeight = () => {
      if (window.innerWidth > 768 && window.innerWidth < 1024) {
        if (window.innerHeight > 1000) setHeight(true);
        else setHeight(false);
      }
    };

    window.addEventListener("resize", checkHeight);
  }, []);

  return (
    <div className="flex min-h-screen flex-col bg-gray-200 dark:bg-slate-900 ">
      <div className="sticky top-0 z-10 bg-gray-200 pb-2 pt-2 dark:bg-slate-900">
        <Sidebar />
        <Logo />
      </div>

      <div className="mb-auto mt-8 flex w-full flex-wrap content-start justify-center overflow-y-auto rounded-xl">
        {cities.length > 0 &&
          cities.map((city: CityData) => (
            // eslint-disable-next-line @next/next/link-passhref
            <Link href={`/city/${city.id}`} key={city.id} passHref>
              <div
                className={`card 
                              mx-4 mb-4
                              flex
                              h-24
                              w-full cursor-pointer
                              xs:flex-row`}
              >
                <div className="relative w-3/5 xs:w-full md:w-6/12 ">
                  <Image
                    src={
                      city.city_image !== null
                        ? city.city_image
                        : "/placeholder.png"
                    }
                    alt={city.name}
                    layout="fill"
                    objectFit="cover"
                  />
                </div>
                <div className="flex w-2/5 items-end pb-4 pl-4 text-xl font-light text-gray-900 dark:text-gray-300 xs:w-full sm:text-lg md:w-1/2 md:pl-4 md:text-xl">
                  {city.name}
                </div>
              </div>
            </Link>
          ))}
      </div>
      <Footer />
    </div>
  );
};

export default Home;

export const getStaticProps: GetStaticProps = async () => {
  console.log(`${process.env.API_HOST}/core/city/read/`);
  const res = await axios.get(`${process.env.API_HOST}/core/city/read/`);
  // if (res.status === 200) {
  const cities: CityData[] | [] = await res.data;
  return {
    props: {
      cities: cities,
    },
  };
};
