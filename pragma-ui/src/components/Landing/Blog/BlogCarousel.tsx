import React, { useEffect, useState } from "react";
import BlogPostBox from "./BlogPostBox";
import styles from "../styles.module.scss";
import {
  CarouselProvider,
  Slider,
  Slide,
  ButtonBack,
  ButtonNext,
} from "pure-react-carousel";
import "pure-react-carousel/dist/react-carousel.es.css";
import { ArrowLeftIcon, ArrowRightIcon } from "@heroicons/react/outline";
import classNames from "classnames";

interface BlogPost {
  image: string;
  date: string;
  title: string;
  description: string;
  link: string;
}

const BlogCarousel: React.FC = () => {
  const [visibleSlides, setVisibleSlides] = useState(3);

  useEffect(() => {
    const handleResize = () => {
      // Update the number of visible slides based on screen width
      if (window.innerWidth < 400) {
        setVisibleSlides(1.1); // For smaller screens, show fewer slides
      } else if (window.innerWidth < 640) {
        setVisibleSlides(1.4); // For medium screens, show a moderate number
      } else if (window.innerWidth < 768) {
        setVisibleSlides(1.8); // For medium screens, show a moderate number
      } else if (window.innerWidth < 1024) {
        setVisibleSlides(2.1); // For medium screens, show a moderate number
      } else {
        setVisibleSlides(3.1); // For larger screens, show more slides
      }
    };

    // Listen for window resize events
    window.addEventListener("resize", handleResize);

    // Call handleResize on initial load
    handleResize();

    // Clean up the event listener when the component unmounts
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const BlogPosts: BlogPost[] = [
    {
      image: "/assets/posts/v2.webp",
      date: "October 21st, 2024",
      title: "Introducing Pragma v.2",
      description:
        "Today marks a major milestone for Pragma with the release of version 2 of our...",
      link: "https://blog.pragma.build/introducing-pragma-v-2/",
    },
    {
      image: "/assets/posts/OO.webp",
      date: "September 9th, 2024",
      title: "Announcing the Pragma Optimistic Oracle",
      description:
        "We're thrilled to announce the release of version 1 of our optimistic oracle on...",
      link: "https://blog.pragma.build/announcing-the-pragma-optimistic-oracle/",
    },
    {
      image: "/assets/posts/LiqBot.webp",
      date: "September 5th, 2024",
      title: "Announcing the Open-Source Liquidation Bot for Vesu",
      description:
        "We're thrilled to announce that we've developed a fully open-source liquidation bot...",
      link: "https://blog.pragma.build/announcing-the-open-source-liquidation-bot-for-vesu/",
    },
    {
      image: "/assets/posts/merkle.webp",
      date: "August 30th, 2024",
      title: "I have a Merkle",
      description:
        "In collaboration with DOPP, Pragma is excited to introduce our new product:...",
      link: "https://blog.pragma.build/i-have-a-merkle/",
    },
    {
      image: "/assets/posts/pragmaxvesu.webp",
      date: "August 26th, 2024",
      title: "Vesu's vault - Pragma's shield",
      description:
        "Pragma Oracle is excited to announce its integration with Vesu, a key addition to our...",
      link: "https://blog.pragma.build/vesus-vault-pragmas-shield/",
    },
    {
      image: "/assets/posts/pragmapi.webp",
      date: "February 22nd, 2024",
      title: "Pragma Empowers Starknet Sequencer with the Launch of Pragma API",
      description:
        "We're thrilled to announce a new addition to our product suite – the Pragma API, with Starknet as its first user.",
      link: "https://blog.pragma.build/pragma-empowers-starknet-sequencer-with-the-launch-of-the-api/",
    },
    {
      image: "/assets/posts/vrf.webp",
      date: "December 1st, 2023",
      title: "Introducing the Verifiable Random Function in Cairo 1",
      description:
        "We are thrilled to announce the first phase of Pragma VRF, leveraging verifiable random functions to generate onchain verifiable randomness. Pragma VRF will greatly help...",
      link: "https://blog.pragma.build/introducing-the-verifiable-random-function-vrf-in-cairo-1/",
    },
    {
      image: "/assets/posts/security.webp",
      date: "November 29th, 2023",
      title: "Exploring Pragma's Security",
      description:
        "We're thrilled to (officially) announce our bounty program on Immunefi, offering up to $50,000 for discovering vulnerabilities in our smart contracts. If you're proficient in Cairo and keen on assisting us in securing our Oracle...",
      link: "https://blog.pragma.build/exploring-pragmas-security/",
    },
    {
      image: "/assets/posts/introducing.webp",
      date: "September 7th, 2023",
      title: "(RE)Introducing Pragma on Starknet",
      description:
        "Pragma is the leading Oracle on Starknet. It provides off-chain data to all DeFi happening on Starknet. Pragma is built from the ground up to remove any trust assumptions...",
      link: "https://blog.pragma.build/re-introducing-pragma-on-starknet/",
    },
    {
      image: "/assets/posts/longliveoracles.webp",
      date: "August 21st, 2023",
      title: "Oracles are dead, Long live Oracles",
      description:
        "For as long as blockchains have been programmable, developers have attempted to bring data on-chain. Blockchains offer amazing properties, especially in terms of transparency, immutability, and openness...",
      link: "https://blog.pragma.build/oracles-are-dead-long-live-oracles/",
    },
  ];

  const sizeOfBlogPosts = BlogPosts.length;

  return (
    <div className={classNames("pb-30 overflow-visible ", styles.carouselWrap)}>
      <CarouselProvider
        naturalSlideWidth={150}
        naturalSlideHeight={200}
        visibleSlides={visibleSlides}
        totalSlides={sizeOfBlogPosts}
        step={1}
        className={styles.carouselWrapper}
      >
        <Slider className=" sm:pl-8">
          {BlogPosts.map((post, index) => (
            <Slide index={index} key={index}>
              <BlogPostBox
                image={post.image}
                date={post.date}
                title={post.title}
                description={post.description}
                link={post.link}
                key={index}
              />
            </Slide>
          ))}
        </Slider>
        <div className="relative lg:h-20 xl:h-0">
          <ButtonBack className="absolute bottom-0	left-10 hidden cursor-pointer rounded-full border border-lightGreen bg-transparent p-3 text-lightGreen transition-colors duration-300 hover:bg-lightGreen hover:text-darkGreen lg:block 2xl:bottom-28">
            <ArrowLeftIcon className="w-5" />
          </ButtonBack>
          <ButtonNext className="absolute left-24	bottom-0 hidden cursor-pointer rounded-full border border-lightGreen bg-transparent p-3 text-lightGreen transition-colors duration-300 hover:bg-lightGreen hover:text-darkGreen lg:block 2xl:bottom-28">
            <ArrowRightIcon className="w-5" />
          </ButtonNext>
        </div>
      </CarouselProvider>
    </div>
  );
};

export default BlogCarousel;
