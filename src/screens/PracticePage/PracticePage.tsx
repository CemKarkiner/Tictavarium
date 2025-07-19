import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

interface Note {
  note: string;
  duration: string;
}

interface MeasureData {
  part: string;
  measure: string;
  notes: Note[];
}

export const PracticePage = (): JSX.Element => {
  const { songName: urlSongName } = useParams<{ songName: string }>();
  const navigate = useNavigate();

  const [bpm, setBpm] = useState(120);
  const [bpmInput, setBpmInput] = useState(bpm.toString());
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentBeat, setCurrentBeat] = useState(1);
  const [currentMeasure, setCurrentMeasure] = useState(1);

  const [songName] = useState(urlSongName ? decodeURIComponent(urlSongName) : "Song Name");
  const [artist] = useState("From");

  const [musicData, setMusicData] = useState<MeasureData[]>([]);
  const [tabData, setTabData] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string>("");

  const intervalRef = useRef<number | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const measureIncrementedRef = useRef(false);

  // ✅ Fetch Notes and Tab from Backend
  const API_BASE = "http://localhost:8000";

  useEffect(() => {
    const fetchNotesAndTab = async () => {
      try {
        const notesRes = await fetch(`${API_BASE}/api/notes?song=${encodeURIComponent(songName)}`);
        if (!notesRes.ok) throw new Error(`Failed to fetch notes: ${notesRes.status}`);
        const notesJson = await notesRes.json();
        setMusicData(notesJson);

        const tabRes = await fetch(`${API_BASE}/api/tab?song=${encodeURIComponent(songName)}`);
        if (!tabRes.ok) throw new Error(`Failed to fetch tab: ${tabRes.status}`);
        const tabJson = await tabRes.json();
        setTabData(tabJson.tab || "No tablature available.");
      } catch (err: any) {
        console.error(err);
        setErrorMsg(err.message || "Something went wrong while fetching data.");
      }
    };

    fetchNotesAndTab();
  }, [songName]);


  // ✅ Create Metronome Beep
  const createBeep = (frequency: number, duration: number) => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }

    const ctx = audioContextRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);

    oscillator.frequency.value = frequency;
    oscillator.type = "sine";

    gainNode.gain.setValueAtTime(0.3, ctx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration);

    oscillator.start(ctx.currentTime);
    oscillator.stop(ctx.currentTime + duration);
  };

  const startMetronome = () => {
    if (!isPlaying) setIsPlaying(true);
  };

  const stopMetronome = () => {
    setIsPlaying(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setCurrentBeat(1);
    measureIncrementedRef.current = false;
  };

  const resetPractice = () => {
    stopMetronome();
    setCurrentMeasure(1);
    setCurrentBeat(1);
    measureIncrementedRef.current = false;
  };

  const handleBackToHome = () => {
    stopMetronome();
    navigate("/");
  };

  const handleBpmChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBpmInput(e.target.value);
  };

  const applyBpmChange = () => {
    const value = parseInt(bpmInput);
    if (isNaN(value) || bpmInput.trim() === "") {
      setBpm(120);
      setBpmInput("120");
    } else {
      const newBpm = Math.max(20, value);
      setBpm(newBpm);
      setBpmInput(newBpm.toString());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      applyBpmChange();
      (e.target as HTMLInputElement).blur();
    }
  };

  // ✅ Metronome Interval
  useEffect(() => {
    if (isPlaying) {
      if (intervalRef.current) clearInterval(intervalRef.current);

      const interval = 60000 / bpm;
      intervalRef.current = window.setInterval(() => {
        setCurrentBeat((prevBeat) => {
          const nextBeat = prevBeat >= 4 ? 1 : prevBeat + 1;
          const frequency = nextBeat === 1 ? 1200 : 800;
          createBeep(frequency, 0.1);

          if (nextBeat === 1 && prevBeat === 4 && !measureIncrementedRef.current) {
            setCurrentMeasure((prevMeasure) => prevMeasure + 1);
            measureIncrementedRef.current = true;
          }
          if (nextBeat !== 1) {
            measureIncrementedRef.current = false;
          }
          return nextBeat;
        });
      }, interval);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isPlaying, bpm]);

  return (
    <div className="min-h-screen w-screen bg-gradient-to-br from-[#f9eded] to-[#faf0e6] p-4">
      <div className="max-w-7xl mx-auto">
        {/* Error Alert */}
        {errorMsg && (
          <div className="bg-red-100 text-red-800 p-4 mb-4 rounded-lg">
            ⚠ {errorMsg}
          </div>
        )}

        {/* Header */}
        <div className="flex items-center justify-center mb-8">
          <Button
            onClick={handleBackToHome}
            className="absolute left-4 top-4 bg-[#fadeb2] hover:bg-[#f8d49e] text-black px-4 py-2 rounded-lg font-medium"
          >
            ← Back to Home
          </Button>

          <img className="w-12 h-12 mr-4" alt="Music note icon" src="/MusicNote.png" />
          <h1 className="font-bold text-black text-4xl text-center tracking-wide font-['Inter',Helvetica]">
            TicTavarium
          </h1>
          <img className="w-12 h-12 ml-4" alt="Music note icon" src="/MusicNote.png" />
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20">
              <div className="flex flex-col items-center mb-6">
                <img src="/metronome.png" alt="Metronome" className="w-20 h-20 mb-4" />
                <div className="text-center">
                  <div className="text-3xl font-bold text-gray-800 mb-1">{bpm}</div>
                  <div className="text-sm text-gray-600 font-medium">BPM</div>
                </div>
              </div>

              {/* BPM Input */}
              <div className="space-y-4 mb-6">
                <Input
                  type="number"
                  value={bpmInput}
                  onChange={handleBpmChange}
                  onBlur={applyBpmChange}
                  onKeyDown={handleKeyPress}
                  className="text-center font-bold text-lg bg-white/50 border-2 border-[#f26565]/30 rounded-lg w-full"
                  placeholder="Enter BPM"
                />
              </div>

              {/* Beat Indicator */}
              <div className="flex justify-center space-x-2 mb-6">
                {[1, 2, 3, 4].map((beat) => (
                  <div
                    key={beat}
                    className={`w-4 h-4 rounded-full border-2 transition-all duration-150 ${
                      currentBeat === beat
                        ? "bg-red-500 border-red-500 scale-125"
                        : "bg-white border-gray-300"
                    }`}
                  />
                ))}
              </div>

              {/* Control Buttons */}
              <div className="space-y-3">
                <Button
                  onClick={isPlaying ? stopMetronome : startMetronome}
                  className={`w-full py-3 rounded-xl font-bold text-lg transition-all duration-200 ${
                    isPlaying
                      ? "bg-red-500 hover:bg-red-600 text-white"
                      : "bg-green-500 hover:bg-green-600 text-white"
                  }`}
                >
                  {isPlaying ? "Stop" : "Start"}
                </Button>

                <Button
                  onClick={resetPractice}
                  className="w-full py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-xl font-medium"
                >
                  Reset
                </Button>
              </div>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-3">
            {/* Song Info */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 mb-6 shadow-lg border border-white/20">
              <div className="flex items-center justify-between mb-4">
                <div className="flex-1">
                  <div className="text-2xl font-bold bg-[#fadeb2]/50 border-2 border-[#f26565]/30 rounded-lg mb-2 px-3 py-1 select-none">
                    {songName}
                  </div>
                  <div className="text-lg bg-[#fadeb2]/30 border border-[#f26565]/20 rounded-lg px-3 py-1 select-none">
                    {artist}
                  </div>
                </div>

                <div className="ml-6 text-right">
                  <div className="text-sm text-gray-600">Current Measure</div>
                  <div className="text-3xl font-bold text-gray-800">{currentMeasure}</div>
                </div>
              </div>
            </div>

            {/* Tab Display */}
            <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20">
              <h2 className="text-xl font-bold mb-4">Tablature:</h2>
              <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm font-mono">
                {tabData || "Loading tablature..."}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
