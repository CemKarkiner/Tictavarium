import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

export const MainPage = (): JSX.Element => {
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/practice/${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <div className="min-h-screen w-screen bg-[#f9eded] flex items-center justify-center">
      <div className="relative w-full h-screen bg-[url(/background.svg)] bg-cover bg-center rounded-lg shadow-lg flex flex-col">

        {/* Top Navigation */}
        <div className="flex justify-center items-center px-6 pt-6 gap-6 flex-wrap">

          {/* Devices */}
          <div className="relative flex flex-col items-center">
            <img
              src="/guitar.png"
              alt="Devices Icon"
              className="w-[35px] h-[35px]"
            />
            <Button className="bg-[#fadeb2] rounded-lg hover:bg-[#f8d49e] w-[106px] h-[35px] text-black flex items-center justify-center">
              Devices
            </Button>
          </div>

          {/* Upload S&P */}
          <div className="relative flex flex-col items-center">
            <img
              src="/upload.png"
              alt="Upload S&P Icon"
              className="w-[35px] h-[35px]"
            />
            <Button className="bg-[#fadeb2] rounded-lg hover:bg-[#f8d49e] w-[106px] h-[35px] text-black flex items-center justify-center">
              Upload S&P
            </Button>
          </div>

          {/* About Us */}
          <div className="relative flex flex-col items-center">
            <img
              src="/CatWithBall.png"
              alt="About Us Icon"
              className="w-[35px] h-[35px] transform scale-x-[-1]"
            />
            <Button className="bg-[#fadeb2] rounded-lg hover:bg-[#f8d49e] w-[106px] h-[35px] text-black flex items-center justify-center">
              About Us
            </Button>
          </div>

          {/* Help */}
          <div className="relative flex flex-col items-center">
            <img
              src="/CatWithBall.png"
              alt="Help Icon"
              className="w-[35px] h-[35px]"
            />
            <Button className="bg-[#fadeb2] rounded-lg hover:bg-[#f8d49e] w-[106px] h-[35px] text-black flex items-center justify-center">
              Help
            </Button>
          </div>
        </div>

        {/* Title Section */}
        <div className="flex items-center justify-center mt-16 gap-4">
          <img
            className="w-[63px] h-[63px]"
            alt="Music note icon"
            src="/MusicNote.png"
          />
          <h1 className="font-semibold text-black text-[48px] text-center tracking-[0.16px] font-['Inter',Helvetica]">
            TicTavarium
          </h1>
          <img
            className="w-[63px] h-[63px]"
            alt="Music note icon"
            src="/MusicNote.png"
          />
        </div>

        {/* Search Input */}
        <div className="flex justify-center mt-6">
          <form onSubmit={handleSearchSubmit} className="flex justify-center">
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-[295px] h-[47px] bg-[#fadeb2] rounded-xl border border-[#f26565] px-3 font-['Inter',Helvetica] font-normal italic text-black text-[11px] placeholder:text-black/70 focus:outline-none focus:ring-2 focus:ring-[#f26565] focus:border-transparent"
              placeholder="Enter any S&P..."
            />
          </form>
        </div>

      </div>
    </div>
  );
};
