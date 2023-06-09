import axios from "axios";
import { GetStaticPaths, GetStaticProps } from "next";
import React, { useEffect, useState } from "react";
import { CityData, RegionData } from "../../../types/interfaces";
import Link from "next/link";
import { useRouter } from "next/router";
import Sidebar from "../../../components/Layout/Sidebar";
import Image from "next/image";
import Logo from "../../../components/Layout/Logo";
import Back from "../../../components/Layout/Back";
import Footer from "../../../components/Layout/Footer";

const Region: React.FC<{ regions: RegionData[] | [] }> = ({ regions }) => {
  const router = useRouter();

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
    <div className="flex min-h-screen flex-col bg-gray-200 dark:bg-slate-900">
      <div className="sticky top-0 z-10 flex justify-between  bg-gray-200 pt-2 pb-3 dark:bg-slate-900">
        <Back router={router} />
        <Logo />
        <Sidebar />
      </div>

      <div className="mb-auto flex w-full flex-wrap content-start justify-center overflow-y-auto rounded-xl ">
        {regions.length > 0 &&
          regions.map((region: RegionData) => (
            // eslint-disable-next-line @next/next/link-passhref
            <Link href={`/region/${region.id}`} key={region.id} passHref>
              <div className="card mx-4 mb-4 flex h-16 w-full cursor-pointer xs:flex-row">
                <div className="flex w-full items-center justify-center text-xl font-light text-gray-900 dark:text-gray-300">
                  {region.name}
                </div>
              </div>
            </Link>
          ))}
      </div>
      <Footer />
    </div>
  );
};

export default Region;

export const getStaticPaths: GetStaticPaths = async () => {
  const res = await axios.get(`${process.env.API_HOST}/core/city/read/`);
  const cities: CityData[] | [] = await res.data;
  const paths = cities.map((city: CityData) => ({
    params: {
      cityid: `${city.id}`,
    },
  }));
  return {
    paths,
    fallback: true,
  };
};

//TODO: sort django-filter queries, gets everything if wrong
export const getStaticProps: GetStaticProps = async (ctx) => {
  const cityid = ctx.params?.cityid;
  let regions: RegionData[] | [] = [];

  const res = await axios(
    `${process.env.API_HOST}/core/region/read/?fk_city=${cityid}`
  );
  regions = await res.data;

  try {
    regions.length;
    // console.log("==============54==================",regions);
  } catch {
    regions = [];
  }

  return {
    props: {
      regions: regions,
    },
  };
};
