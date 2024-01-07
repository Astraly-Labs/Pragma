import React from "react";
import Link from "next/link";
import { Popover } from "@headlessui/react";
import {
  ChatIcon,
  CodeIcon,
  CursorClickIcon,
  HomeIcon,
  MenuIcon,
  PuzzleIcon,
  ViewListIcon,
  XIcon,
  SpeakerphoneIcon,
} from "@heroicons/react/outline";
import NavPopover from "./NavPopover";
import SearchBar from "./SearchBar";
import StyledTransition from "../common/StyledTransition";
import {
  buildExplorerUrlForAddress,
  networkId,
} from "../../services/wallet.service";
import { getOracleProxyAddress } from "../../services/address.service";
import styles from "./styles.module.scss";
import { ButtonLink } from "../common/Button";
import classNames from "classnames";

interface Resource {
  name: string;
  description: string;
  href: string;
  icon: (props: React.SVGProps<SVGSVGElement>) => JSX.Element;
}

// List of resources displayed directly in the nav
const resources: Resource[] = [
  {
    name: "Ecosystem",
    description: "Start using our data by reading our docs.",
    href: "https://docs.pragmaoracle.com/",
    icon: CodeIcon,
  },
  {
    name: "Docs",
    description: "Learn about what makes Pragma special.",
    href: "/features",
    icon: PuzzleIcon,
  },
  {
    name: "Resources",
    description: "Meet our data publishers.",
    href: "/publishers",
    icon: SpeakerphoneIcon,
  },
  {
    name: "Community",
    description: "Take a look at who is already using Pragma.",
    href: "/protocols",
    icon: ViewListIcon,
  },
];

// List of resources displayed in the more tab
const additional = [
  // {
  //   name: "About Us",
  //   description: "Get to know the team behind Pragma.",
  //   href: "/about",
  //   icon: UserGroupIcon,
  // },
  {
    name: "View on Block Explorer",
    description: "Take a closer look at our Starknet contract.",
    href: `${buildExplorerUrlForAddress(
      getOracleProxyAddress(networkId())
    )}#readContract`,
    icon: CursorClickIcon,
  },
];

// Calls to action at the bottom of the more tab.
const callsToAction = [
  {
    name: "Request Asset",
    href: "mailto:support@pragma.build?body=Hi%Pragma%20Team,%0AWe%20would%20like%20to%20request%20the%20following%20assets:",
    icon: ChatIcon,
  },
];

// Mobile only
const mobileResources = [
  {
    name: "Home",
    href: "/",
    icon: HomeIcon,
  },
];

const NavHeader = () => (
  <Popover className={"absolute w-full p-8"}>
    <Popover className={styles.container}>
      <div className="flex items-center justify-between md:justify-start md:space-x-10 lg:space-x-0">
        <div className="flex justify-start lg:w-0 lg:flex-1">
          <Link href="/">
            <div>
              <span className="sr-only">Pragma</span>
              <img
                className="h-8 w-auto"
                src="/pragma-og-img.png"
                alt="Pragma"
              />
            </div>
          </Link>
        </div>
        <div className="-my-2 -mr-2 md:hidden">
          {/* To open mobile menu */}
          <Popover.Button className="hover:bg-dark focus:ring-primary inline-flex items-center justify-center rounded-md p-2 text-white hover:text-slate-600 focus:outline-none focus:ring-2 focus:ring-inset">
            <span className="sr-only">Open menu</span>
            <MenuIcon className="h-6 w-6" aria-hidden="true" />
          </Popover.Button>
        </div>
        <Popover.Group as="nav" className="hidden space-x-10 md:flex">
          {resources.map((resource) => (
            <a
              href={resource.href}
              key={resource.name}
              className="text-base font-medium text-lightGreen hover:text-white"
            >
              {resource.name}
            </a>
          ))}
          {/* <NavPopover
          buttonName="More"
          content={additional}
          callsToAction={callsToAction}
        /> */}
        </Popover.Group>
        <div className="hidden items-center justify-end md:flex md:flex-1 lg:w-0">
          <ButtonLink center={false} variant="solid" color="mint" href="/">
            Start building
          </ButtonLink>
        </div>
      </div>

      {/* Mobile Version */}
      <StyledTransition
        enterFrom="scale-95"
        enterTo="scale-100"
        leaveFrom="scale-100"
        leaveTo="scale-95"
      >
        <Popover.Panel
          focus
          className={classNames(
            styles.mobilePop,
            "absolute inset-x-0 top-0 z-10 origin-top-right transform p-2 transition md:hidden"
          )}
        >
          <div className="divide-grey bg-dark divide-y-2 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
            <div className="px-5 pt-5 pb-6">
              <div className="flex items-center justify-between">
                <div>
                  <img
                    className="h-8 w-auto"
                    src="pragma-og-img.png"
                    alt="Pragma"
                  />
                </div>
                <div className="-mr-2">
                  <Popover.Button className="hover:bg-dark hover:text-grey focus:ring-primary inline-flex items-center justify-center rounded-md bg-black p-2 text-white focus:outline-none focus:ring-2 focus:ring-inset">
                    <span className="sr-only">Close menu</span>
                    <XIcon className="h-6 w-6" aria-hidden="true" />
                  </Popover.Button>
                </div>
              </div>
              <div className="mt-6">
                <nav className="grid gap-y-8">
                  {[...mobileResources, ...resources].map((resource) => (
                    <a
                      key={resource.name}
                      href={resource.href}
                      className="-m-3 flex items-center rounded-md p-3 hover:bg-black"
                    >
                      <resource.icon
                        className="text-primary h-6 w-6 flex-shrink-0"
                        aria-hidden="true"
                      />
                      <span className="text-grey ml-3 text-base font-medium">
                        {resource.name}
                      </span>
                    </a>
                  ))}
                </nav>
              </div>
            </div>
            <div className="space-y-2 py-6 px-5">
              <div className="grid grid-cols-2 gap-y-4 gap-x-8">
                {additional.map((item) => (
                  <a
                    key={item.name}
                    href={item.href}
                    className="text-grey text-base font-medium hover:text-white"
                  >
                    {item.name}
                  </a>
                ))}
              </div>
              <div className="flex flex-col items-center">
                <SearchBar />
                <p className="text-grey mt-6 text-center text-base font-medium">
                  Need help?{" "}
                  <a href="#" className="text-primary hover:text-secondary">
                    Contact us
                  </a>
                </p>
              </div>
            </div>
          </div>
        </Popover.Panel>
      </StyledTransition>
    </Popover>
  </Popover>
);

export default NavHeader;
