import axios from "axios";
import { GetStaticPaths, GetStaticProps } from "next";
import React, { useEffect } from "react";
import { FilterListingData, RegionData } from "../../../types/interfaces";
import { ListingData } from "../../../types/interfaces";
import { NextRouter, useRouter } from "next/router";

import Sidebar from "../../../components/Layout/Sidebar";
import Back from "../../../components/Layout/Back";
import Logo from "../../../components/Layout/Logo";
import Footer from "../../../components/Layout/Footer";
import PropertyPreview from "../../../components/PropertyPreview";
import SearchBar from "../../../components/SearchBar";
import Fuse from "fuse.js";

const Listings: React.FC<{
  listings: ListingData[] | [];
}> = ({ listings }) => {
  const [search, setSearch] = React.useState<string>("");

  const [filtered_listings, setFilteredListings] = React.useState<
    FilterListingData[] | []
  >([]);
  const router: NextRouter = useRouter();
  const { regionid, builder } = router.query;
  const options = {
    keys: ["name", "fk_builder.name", "fk_region.name"],
  };
  const fuse = new Fuse(listings, options);
  useEffect(() => {
    if (builder) {
      setSearch(builder as string);
      setFilteredListings(fuse.search(`${search}`));
    }
  }, [search]);

  return (
    <div className="flex min-h-screen flex-col bg-gray-200 dark:bg-slate-900 ">
      <div className="sticky top-0 z-10 flex flex-col bg-gray-200 pb-3 dark:bg-slate-900">
        <div className="mt-2 flex justify-between">
          <Back router={router} />
          <Logo />
          <Sidebar />
        </div>
        <SearchBar
          search={search}
          setSearch={setSearch}
          listings={listings}
          setFilteredListings={setFilteredListings}
        />
      </div>
      <div className="mb-auto flex w-full flex-wrap content-start justify-center overflow-y-auto rounded-xl ">
        {search === "" ? (
          Array.isArray(listings) ? (
            listings.map((item: ListingData) => {
              if (item.fk_region?.id == regionid)
                return <PropertyPreview item={item} key={item.id} />;
            })
          ) : (
            <h1>No Listings in this region</h1>
          )
        ) : filtered_listings.length > 0 ? (
          filtered_listings.map(({ item }: FilterListingData) => {
            if (item.fk_region?.id == regionid)
              return <PropertyPreview item={item} key={item?.id} />;
          })
        ) : (
          // eslint-disable-next-line react/no-unescaped-entities
          <h1>No results found for '{search}'</h1>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default Listings;

export const getStaticPaths: GetStaticPaths = async () => {
  const res = await axios.get(`${process.env.API_HOST}/core/region/read/`);
  const regions: RegionData[] | [] = await res.data;
  const paths = regions.map((region: RegionData) => ({
    params: {
      regionid: `${region.id}`,
    },
  }));
  return {
    paths,
    fallback: false,
  };
};

//TODO: sort django-filter queries, gets everything if wrong
export const getStaticProps: GetStaticProps = async (ctx) => {
  const regionid = ctx.params?.regionid;
  let listings: ListingData[] | [] = [];

  const res = await axios(
    `${process.env.API_HOST}/core/listing/read/?fk_region=${regionid}`
  );

  listings = await res.data;

  return {
    props: {
      listings: listings,
    },
  };
};
