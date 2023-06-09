import Fuse from "fuse.js";
import React, { useEffect } from "react";
import { FilterListingData, ListingData } from "../types/interfaces";

const SearchBar: React.FC<{
  search: string;
  setSearch: React.Dispatch<React.SetStateAction<string>>;
  listings: ListingData[] | [];
  setFilteredListings: React.Dispatch<
    React.SetStateAction<[] | FilterListingData[]>
  >;
}> = ({ search, setSearch, listings, setFilteredListings }) => {
  const options = {
    keys: ["name", "fk_builder.name", "fk_region.name"],
  };
  const fuse = new Fuse(listings, options);
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setFilteredListings(fuse.search(`${search}`));
  };
  return (
    <>
      <input
        type="text"
        placeholder="Search"
        name="search"
        value={search}
        onChange={handleSearch}
        className="mx-4 mt-4 rounded-lg px-4 py-2 shadow-md placeholder:font-light"
      />
    </>
  );
};

export default SearchBar;
