# Resolve: karaoke captions and freeze/SBAM

This is the reusable ARPHÈ workflow for vertical social captions and the freeze/SBAM beat. It is never a per-video command or preset.

## Caption treatment

- Keep the entire short phrase visible in white, uppercase `Satoshi Bold`.
- Use one compact burgundy card behind only the currently spoken word; the card moves word by word.
- Keep spacing compact and readable. Do not display isolated words and do not use a fixed banner behind the whole phrase.
- Correct transcript wording in the plan data before rendering; do not hard-code editorial corrections in the bridge.

## Freeze and SBAM

- Build the freeze only after the timeline is established at 1080×1920.
- The frozen frame must fill the vertical canvas. A landscape freeze inside a vertical timeline is invalid because it creates black borders and a reduced image.
- Use 15 frames at 30 fps (0.5 seconds), mute the original audio for the freeze, and place the SBAM transient at its first frame on a separate audio track.

## Required review

1. Capture two frames from different active words of one phrase to verify that the phrase remains complete and the card moves.
2. Capture a frame in a transcript gap to ensure no caption remains.
3. Capture the freeze frame and confirm full-screen 9:16 coverage before saving, rendering, or uploading.
