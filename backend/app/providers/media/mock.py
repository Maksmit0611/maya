import asyncio
from pathlib import Path
from typing import Any
from uuid import UUID


class MockMediaProvider:
    name = "mock-media"

    def __init__(self, result_dir: str = "./results"):
        self._result_dir = Path(result_dir)

    async def generate(self, job: Any) -> dict[str, Any]:
        self._result_dir.mkdir(parents=True, exist_ok=True)
        output = self._result_dir / f"{UUID(str(job.id))}.mp4"
        ffmpeg = (
            await asyncio.create_subprocess_exec(
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                "color=c=0xE9E2D5:s=1280x720:d=3",
                "-vf",
                "drawtext=text='MAYA AI concept preview':fontcolor=0x343A35:fontsize=32:"
                "x=(w-text_w)/2:y=(h-text_h)/2",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                "-y",
                str(output),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            if _has_ffmpeg()
            else None
        )
        if ffmpeg is not None:
            await ffmpeg.communicate()
        return {
            "kind": "placeholder_video" if output.exists() else "placeholder_metadata",
            "label": "AI visualisation concept — not construction-ready",
            "local_path": str(output) if output.exists() else None,
            "mime_type": "video/mp4" if output.exists() else None,
            "duration_seconds": 3,
            "ffmpeg_available": output.exists(),
        }


def _has_ffmpeg() -> bool:
    from shutil import which

    return which("ffmpeg") is not None
