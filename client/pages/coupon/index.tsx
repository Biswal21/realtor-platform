import Link from "next/link";
import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";
import Sidebar from "../../components/Layout/Sidebar";
import axiosInstance from "../../services/axiosauth";
import { CouponData } from "../../types/interfaces";
import Image from "next/image";
import Back from "../../components/Layout/Back";
import Logo from "../../components/Layout/Logo";

const Coupon = () => {
  const [coupons, setCoupons] = useState<CouponData[] | []>([]);

  const [login, setLogin] = useState<Boolean>(false);

  const router = useRouter();

  function formatDate(dateString: string): string {
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = {
      month: "long",
      day: "numeric",
      year: "numeric",
    };
    return date.toLocaleDateString("en-US", options);
  }

  useEffect(() => {
    axiosInstance
      .get("/core/user_coupons/read/")
      .then((res) => {
        // console.log("is logged in", res.data);
        setCoupons(res.data);
        setLogin(true);
      })
      .catch((err) => {
        if (
          err.message === "Invalid token specified" ||
          (err.response && err.response.status === 401)
        ) {
          setLogin(false);
          router.push("/login/");
        }
        if (err.response) {
          // console.log(err.response.data?.token_error);
          if (
            (err.response.data?.refresh &&
              err.response.data?.refresh[0] ===
                "This field may not be null.") ||
            (err.response.data?.token_error &&
              err.response.data?.token_error === "Token is blacklisted")
          ) {
            setLogin(false);
            router.push("/login/");
          }
        }
      });
  }, [router]);

  return (
    <>
      <div className="flex min-h-screen flex-col bg-gray-200 dark:bg-slate-900">
        <div className="sticky top-0 z-10 flex justify-between  bg-gray-200 pt-2 pb-3 dark:bg-slate-900">
          <Back router={router} />
          <Logo />
          <Sidebar />
        </div>
        <div className="mb-2 flex w-full flex-wrap content-start justify-center overflow-y-auto rounded-xl pt-4">
          <div className="mt-2 mb-4 text-xl font-light">MY COUPONS</div>

          <div className="h-fit w-full">
            <ul className="flex w-full flex-row flex-wrap overflow-y-auto">
              {coupons.map((coupon) => {
                if (coupon.is_paid)
                  return (
                    <div className="shine-box card mx-4 mb-4 flex w-full bg-gradient-to-r from-yellow-500 via-yellow-400 to-yellow-400 px-4 py-4">
                      <Link
                        href={`/listing/${coupon.fk_listing}`}
                        passHref={true}
                      >
                        <li style={{ cursor: "pointer" }} key={coupon.id}>
                          {coupon.name}
                        </li>
                      </Link>
                    </div>
                  );
              })}
            </ul>
            <ul className="flex w-full flex-row flex-wrap overflow-y-auto">
              {coupons.map((coupon) => {
                if (!coupon.is_paid) {
                  return (
                    <div className="card mx-4 mb-4 flex w-full px-3 py-2">
                      <div className="w-full">
                        {/* <div className="flex items-center justify-between"> */}
                        <Link
                          href={`/listing/${coupon.fk_listing}`}
                          passHref={true}
                        >
                          <a className="flex items-center justify-between">
                            <h4 className="text-xl font-semibold">
                              {coupon.listing_data.name}
                            </h4>
                            <div className="py-3 text-sm font-medium text-slate-400 underline decoration-slate-400">
                              {coupon.listing_data.region !== undefined
                                ? `${coupon.listing_data.region}, `
                                : null}
                              {coupon.listing_data.city}
                            </div>
                          </a>
                        </Link>
                        {/* </div> */}
                        <hr className="my-2 border-gray-300" />
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-sm text-slate-400 decoration-slate-400">
                              Valid till
                            </p>
                            <p className="text-sm font-semibold text-blue-500">
                              {formatDate(coupon.expiration_date)}
                            </p>
                          </div>
                          <div className="flex items-center space-x-1">
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              fill="none"
                              viewBox="0 0 24 24"
                              strokeWidth={1.5}
                              stroke="currentColor"
                              className="h-6 w-6 text-slate-400"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 010 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 010-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375z"
                              />
                            </svg>

                            <p className="font-semibold text-slate-700">
                              {coupon.name}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                }
              })}
            </ul>
          </div>
        </div>
      </div>
      {/* <div className="ticket">
  <div className="ticket__content">
    <p className="ticket__text">Pure CSS Ticket</p>
  </div>
</div> */}
      {/* <div id="raffle-red" className="entry raffle">
        <div className="no-scale">
          <div className="text-4xl font-medium text-[#333] flex justify-center items-center">LOL</div>
        </div>
  </div> */}
    </>
  );
};

export default Coupon;
