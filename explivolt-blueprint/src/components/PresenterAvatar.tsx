import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { AvatarPose } from "../data/videoData";

interface PresenterAvatarProps {
  pose: AvatarPose;
  speaking?: boolean;
}

/**
 * Clean 2D illustrated SVG Presenter Avatar (Explivolt-inspired mint hoodie tech host).
 * Zero external image dependencies — works identically on every runner and supports:
 * - Natural subtle breathing bob
 * - Periodic eye blinking
 * - Speech-reactive mouth animation
 * - 7 expressive hand & eyebrow poses driven by `pose`
 */
export const PresenterAvatar: React.FC<PresenterAvatarProps> = ({
  pose,
  speaking = true,
}) => {
  const frame = useCurrentFrame();

  // Gentle breathing bob
  const bobY = Math.sin(frame * 0.1) * 4;

  // Periodic natural eye blink every ~3.2s (96 frames)
  const blinkCycle = frame % 96;
  const isBlinking = blinkCycle >= 91 && blinkCycle <= 94;

  // Mouth animation when speaking
  const mouthOpen = speaking ? (Math.sin(frame * 0.72) * 0.5 + 0.5) * 11 + 3 : 2;

  const isShocked = pose === "shocked";
  const isThinking = pose === "thinking";
  const isHappy = pose === "thumbsUp" || pose === "okSign";

  // Eyebrow lift
  const browOffsetY = isShocked ? -8 : isThinking ? -3 : isHappy ? -4 : 0;

  return (
    <div
      style={{
        position: "absolute",
        bottom: -14,
        left: "50%",
        transform: `translateX(-46%) translateY(${bobY}px)`,
        width: 540,
        height: 520,
        pointerEvents: "none",
        zIndex: 30,
      }}
    >
      <svg viewBox="0 0 420 410" width="100%" height="100%" fill="none">
        <defs>
          <linearGradient id="hoodieGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6EE7B7" />
            <stop offset="100%" stopColor="#34D399" />
          </linearGradient>
          <linearGradient id="skinGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#D99B72" />
            <stop offset="100%" stopColor="#C48259" />
          </linearGradient>
          <filter id="avatarShadow" x="-15%" y="-10%" width="130%" height="130%">
            <feDropShadow dx="0" dy="10" stdDeviation="12" floodColor="#000000" floodOpacity="0.22" />
          </filter>
        </defs>

        <g filter="url(#avatarShadow)">
          {/* === TORSO / MINT HOODIE === */}
          <path
            d="M112 292 C112 246 152 232 210 232 C268 232 308 246 308 292 L322 410 L98 410 Z"
            fill="url(#hoodieGrad)"
            stroke="#0F172A"
            strokeWidth="4.5"
            strokeLinejoin="round"
          />
          {/* Inner white crew tee */}
          <path
            d="M174 236 Q210 278 246 236 L236 292 Q210 306 184 292 Z"
            fill="#F8FAFC"
            stroke="#0F172A"
            strokeWidth="3.5"
          />
          {/* Hoodie zipper & collar folds */}
          <line x1="210" y1="296" x2="210" y2="410" stroke="#0F172A" strokeWidth="3.5" />
          <path d="M168 236 C170 264 184 282 192 296" stroke="#0F172A" strokeWidth="3.5" fill="none" />
          <path d="M252 236 C250 264 236 282 228 296" stroke="#0F172A" strokeWidth="3.5" fill="none" />
          {/* Drawstrings */}
          <line x1="188" y1="294" x2="184" y2="348" stroke="#F8FAFC" strokeWidth="4" strokeLinecap="round" />
          <line x1="232" y1="294" x2="236" y2="348" stroke="#F8FAFC" strokeWidth="4" strokeLinecap="round" />

          {/* === NECK === */}
          <rect
            x="186"
            y="196"
            width="48"
            height="48"
            rx="16"
            fill="#BA7A52"
            stroke="#0F172A"
            strokeWidth="4"
          />

          {/* === EARS === */}
          <ellipse cx="141" cy="146" rx="13" ry="19" fill="url(#skinGrad)" stroke="#0F172A" strokeWidth="4" />
          <ellipse cx="279" cy="146" rx="13" ry="19" fill="url(#skinGrad)" stroke="#0F172A" strokeWidth="4" />

          {/* === HEAD === */}
          <path
            d="M148 118 C148 76 174 56 210 56 C246 56 272 76 272 118 C272 174 248 214 210 214 C172 214 148 174 148 118 Z"
            fill="url(#skinGrad)"
            stroke="#0F172A"
            strokeWidth="4.5"
          />

          {/* === STYLISH DARK HAIR === */}
          <path
            d="M144 124 C138 82 162 42 212 42 C258 42 284 74 276 124 C272 102 256 84 232 82 C216 90 192 92 174 84 C158 92 149 108 144 124 Z"
            fill="#1E1B24"
            stroke="#0F172A"
            strokeWidth="4"
            strokeLinejoin="round"
          />
          {/* Hair highlight tuft */}
          <path
            d="M180 56 Q210 46 244 60"
            stroke="#3F3B4D"
            strokeWidth="4.5"
            strokeLinecap="round"
            fill="none"
          />

          {/* === EYEBROWS === */}
          <path
            d={`M168 ${116 + browOffsetY} Q182 ${109 + browOffsetY} 196 ${115 + browOffsetY}`}
            stroke="#1E1B24"
            strokeWidth="5.5"
            strokeLinecap="round"
            fill="none"
          />
          <path
            d={`M224 ${115 + browOffsetY} Q238 ${109 + browOffsetY} 252 ${116 + browOffsetY}`}
            stroke="#1E1B24"
            strokeWidth="5.5"
            strokeLinecap="round"
            fill="none"
          />

          {/* === EYES === */}
          {isBlinking ? (
            <>
              <path d="M170 138 Q182 144 194 138" stroke="#0F172A" strokeWidth="4.5" strokeLinecap="round" />
              <path d="M226 138 Q238 144 250 138" stroke="#0F172A" strokeWidth="4.5" strokeLinecap="round" />
            </>
          ) : (
            <>
              <ellipse cx="182" cy="138" rx="12" ry={isShocked ? 15 : 11} fill="#FFFFFF" stroke="#0F172A" strokeWidth="3.5" />
              <circle cx="183" cy="138" r={isShocked ? 6 : 6.5} fill="#1E1B24" />
              <circle cx="185" cy="135" r="2.2" fill="#FFFFFF" />

              <ellipse cx="238" cy="138" rx="12" ry={isShocked ? 15 : 11} fill="#FFFFFF" stroke="#0F172A" strokeWidth="3.5" />
              <circle cx="237" cy="138" r={isShocked ? 6 : 6.5} fill="#1E1B24" />
              <circle cx="239" cy="135" r="2.2" fill="#FFFFFF" />
            </>
          )}

          {/* === NOSE === */}
          <path d="M210 144 L206 160 Q210 163 215 160" stroke="#9A5B37" strokeWidth="3.2" strokeLinecap="round" fill="none" />

          {/* === MOUTH === */}
          {isShocked ? (
            <ellipse cx="210" cy="184" rx="12" ry="11" fill="#7F1D1D" stroke="#0F172A" strokeWidth="3.5" />
          ) : isHappy ? (
            <path
              d={`M190 176 Q210 ${192 + mouthOpen * 0.5} 230 176 Z`}
              fill="#FFFFFF"
              stroke="#0F172A"
              strokeWidth="3.5"
              strokeLinejoin="round"
            />
          ) : (
            <path
              d={`M193 179 Q210 ${181 + mouthOpen} 227 179 Q210 ${184 + mouthOpen * 1.15} 193 179 Z`}
              fill="#7F1D1D"
              stroke="#0F172A"
              strokeWidth="3.5"
              strokeLinejoin="round"
            />
          )}

          {/* === POSE-SPECIFIC HANDS === */}
          {pose === "pointUp" && (
            <g transform={`translate(0, ${Math.sin(frame * 0.2) * 3})`}>
              {/* Right hand pointing up */}
              <path
                d="M310 296 L334 222 C337 210 350 212 348 224 L336 276 L354 274 C362 274 364 286 356 292 L352 318 C348 334 320 338 310 322 Z"
                fill="url(#skinGrad)"
                stroke="#0F172A"
                strokeWidth="4"
                strokeLinejoin="round"
              />
            </g>
          )}

          {pose === "thumbsUp" && (
            <g transform={`translate(0, ${Math.sin(frame * 0.22) * 3})`}>
              {/* Left thumbs up */}
              <path
                d="M66 298 L76 254 C79 242 92 244 92 256 L92 276 L112 276 C122 276 124 316 112 322 L76 322 C64 322 62 310 66 298 Z"
                fill="url(#skinGrad)"
                stroke="#0F172A"
                strokeWidth="4"
                strokeLinejoin="round"
              />
              {/* Right thumbs up */}
              <path
                d="M354 298 L344 254 C341 242 328 244 328 256 L328 276 L308 276 C298 276 296 316 308 322 L344 322 C356 322 358 310 354 298 Z"
                fill="url(#skinGrad)"
                stroke="#0F172A"
                strokeWidth="4"
                strokeLinejoin="round"
              />
            </g>
          )}

          {pose === "thinking" && (
            <g>
              {/* Hand resting under chin */}
              <path
                d="M174 226 C188 210 226 212 232 224 C236 234 224 244 206 244 L178 244 Z"
                fill="url(#skinGrad)"
                stroke="#0F172A"
                strokeWidth="4"
                strokeLinejoin="round"
              />
            </g>
          )}

          {pose === "shocked" && (
            <g transform={`translate(0, ${interpolate(Math.sin(frame * 0.25), [-1, 1], [-4, 4])})`}>
              {/* Both hands raised open */}
              <rect x="66" y="246" width="44" height="58" rx="18" fill="url(#skinGrad)" stroke="#0F172A" strokeWidth="4" />
              <rect x="310" y="246" width="44" height="58" rx="18" fill="url(#skinGrad)" stroke="#0F172A" strokeWidth="4" />
            </g>
          )}

          {pose === "okSign" && (
            <g transform={`translate(0, ${Math.sin(frame * 0.2) * 3})`}>
              <circle cx="334" cy="274" r="24" fill="url(#skinGrad)" stroke="#0F172A" strokeWidth="4" />
              <circle cx="334" cy="274" r="9" fill="#0F172A" opacity="0.16" />
              <line x1="344" y1="252" x2="356" y2="226" stroke="#0F172A" strokeWidth="5" strokeLinecap="round" />
              <line x1="332" y1="250" x2="338" y2="222" stroke="#0F172A" strokeWidth="5" strokeLinecap="round" />
            </g>
          )}

          {pose === "explain" && (
            <g transform={`translate(0, ${Math.sin(frame * 0.16) * 3})`}>
              {/* Open explaining palms */}
              <path
                d="M72 302 C72 280 96 276 112 286 L116 320 C102 332 76 326 72 302 Z"
                fill="url(#skinGrad)"
                stroke="#0F172A"
                strokeWidth="4"
              />
              <path
                d="M348 302 C348 280 324 276 308 286 L304 320 C318 332 344 326 348 302 Z"
                fill="url(#skinGrad)"
                stroke="#0F172A"
                strokeWidth="4"
              />
            </g>
          )}
        </g>
      </svg>
    </div>
  );
};
