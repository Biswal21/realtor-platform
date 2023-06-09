import axios from "axios";
import { GetServerSideProps } from "next";
import React, { useEffect, useState } from "react";
import ListingComponent from "../../components/ListingComponent";
import { CouponData, ListingData } from "../../types/interfaces";
import ErrorPage from "next/error";
import axiosInstance from "../../services/axiosauth";
import { useRouter } from "next/router";
import Sidebar from "../../components/Layout/Sidebar";
import { toast } from "react-toastify";
import Back from "../../components/Layout/Back";
import Logo from "../../components/Layout/Logo";
// import Image from "next/image";

const Listingid: React.FC<{ listing: ListingData; err: string }> = ({
  listing,
  err,
}) => {
  const [isLoggedin, setLogin] = useState<Boolean>(false);

  // const [coupon, setCoupon] = useState<CouponData>({
  //   id: 0,
  //   name: "",
  //   fk_user: 0,
  //   fk_listing: 0,
  //   fk_payment_request: null,
  //   is_paid: listing.premium_amount
  //     ? listing.premium_amount === undefined ||
  //       listing.premium_amount === null ||
  //       listing.premium_amount === 0
  //       ? false
  //       : true
  //     : false,
  //   is_premium: false,
  //   modified_at: null,
  //   created_at: null,
  // });
  const [coupon, setCoupon] = useState<CouponData | null>(null);
  const router = useRouter();

  useEffect(() => {
    axiosInstance
      .get("/core/user_coupons/read/")
      .then((res) => {
        res.data.map((item: CouponData) => {
          if (!coupon && item.fk_listing === listing.id) {
            setCoupon(item);
          }
        });
        setLogin(true);
      })
      .catch((err) => {
        // console.log(err);
      });
  }, [listing.id, coupon, isLoggedin]);

  const handleGenerate = (id: any) => {
    if (process.browser && localStorage.access_token) {
      axiosInstance
        .post("/core/coupon/create/", { fk_listing: id })
        .then((response) => {
          setCoupon(response.data);
        })
        .catch((err) => {
          console.log(err);
          // if(err.response.data.message)
          // {
          //   toast.error(err.response.data.message);
          // }
          if (
            err.message === "Invalid token specified" ||
            (err.response && err.response.status === 401)
          ) {
            setLogin(false);
            router.push("/login/");
          }
          if (err.response) {
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
            if (err.response.status === 409) {
              setLogin(true);
            }
          }
        });
    } else {
      setLogin(false);
      router.push("/login/");
    }
  };

  const handlePremium = (id: any) => {
    axiosInstance
      .post("/core/payment_request/payment/", { listing_id: id })
      .then((response) => {
        setCoupon(response.data);
        router.push(response.data.payment_url);
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
  };

  return (
    <>
      {err !== "" ? (
        <ErrorPage statusCode={404} />
      ) : (
        <>
          <div className="flex min-h-screen flex-col bg-gray-200 dark:bg-slate-900">
            <div className="sticky top-0 z-10 flex justify-between  bg-gray-200 pt-2 dark:bg-slate-900">
              <Back router={router} />
              <Logo />
              <Sidebar />
            </div>
            <ListingComponent listing={listing} />
            <div className="absolute bottom-0 z-10 w-screen rounded-t-xl bg-gray-200 dark:bg-slate-900">
              {!coupon ? (
                <div className="flex h-full w-full justify-center  bg-slate-200">
                  {/* <div className="bottom-4 w-full justify-center border border-red-700 px-3 pt-3 text-center align-bottom"> */}
                  {/* <button
                      className="button-2 mx-1 bg-gradient-to-r from-yellow-400 via-yellow-400 to-yellow-500 text-black shadow-lg "
                      onClick={() => handlePremium(listing.id)}
                    >
                      Generate Premium Coupon
                    </button> */}
                  <button
                    className="button mx-2 w-full"
                    onClick={() => handleGenerate(listing.id)}
                  >
                    Generate Coupon
                  </button>
                  {/* </div> */}
                </div>
              ) : (
                <>
                  <div className="inline-block h-full w-full bg-slate-200 align-bottom">
                    <div className="sticky bottom-4 z-10 flex w-full flex-wrap justify-evenly px-3 pt-3 text-center align-bottom">
                      {coupon && !coupon.is_paid && (
                        <>
                          <div className="mt-4 w-full">
                            <div className="mb-4 text-xl font-light">
                              YOUR COUPON CODE
                            </div>
                            <div className="mx-1 mb-2 w-full rounded-xl bg-white p-4 font-medium text-black shadow-lg">
                              {coupon.name} 🔖
                            </div>
                            {/* <button
                              className="mx-1 mt-2 w-full rounded-xl bg-gradient-to-r from-yellow-400 via-yellow-400 to-yellow-500 p-4 text-black shadow-lg"
                              onClick={() => handlePremium(listing.id)}
                            >
                              Upgrade to Premium
                            </button> */}
                          </div>
                        </>
                      )}
                      {coupon && coupon.is_paid && (
                        <div className="mt-4 w-full">
                          {/* <div className="mb-4 text-xl font-light">
                            YOUR COUPON CODE
                          </div> */}
                          {/* <div className="mx-1 w-full rounded-xl bg-gradient-to-r from-yellow-400 via-yellow-400 to-yellow-500 p-4 text-black shadow-lg">
                            {coupon.name}
                          </div> */}
                        </div>
                      )}
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default Listingid;

//TODO: sort django-filter queries, gets everything if wrong
export const getServerSideProps: GetServerSideProps = async (ctx) => {
  const { listingid } = ctx.query;
  try {
    const res = await axios.get(
      `${process.env.API_HOST}/core/listing/${listingid}/read/`
    );
    const listing: ListingData = await res.data;
    return {
      props: {
        listing: listing,
        err: "",
      },
    };
  } catch (err: any) {
    const listing: {} = {};
    if (err === undefined || err === null || err.response?.data === undefined)
      err = "";
    else err = err.response.data;
    return {
      props: {
        listing: listing,

        err: err,
      },
    };
  }
};
