import os, re, sys, time, signal, yt_dlp, subprocess, unicodedata, itertools
from urllib.parse import urlparse, parse_qs

NEON = {
    "blue": '\033[38;5;45m',
    "pink": '\033[38;5;198m',
    "green": '\033[38;5;82m',
    "purple": '\033[38;5;135m',
    "orange": '\033[38;5;208m',
    "reset": '\033[0m'
}

def banner():
    print(f"""{NEON["pink"]}
 /$$   /$$ /$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$
| $$$ | $$|_  $$_/ /$$__  $$ /$$__  $$ /$$__  $$
| $$$$| $$  | $$  | $$  \\__/| $$  \\__/| $$  \\ $$
| $$ $$ $$  | $$  | $$ /$$$$| $$ /$$$$| $$$$$$$$
| $$  $$$$  | $$  | $$|_  $$| $$|_  $$| $$__  $$
| $$\\  $$$  | $$  | $$  \\ $$| $$  \\ $$| $$  | $$
| $$ \\  $$ /$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$
|__/  \\__/|______/ \\______/  \\______/ |__/  |__/
    {NEON["blue"]}FIXED_HELL_EDITION_REFINED{NEON["reset"]}
""")

class YtDlpHyperdrive:
    def __init__(self):
        self.succeeded = []
        self.skipped = []
        self.failed = []
        self.non_youtube = []
        self.emergency = False
        signal.signal(signal.SIGINT, self._on_ctrl_c)

    def _on_ctrl_c(self, sig, frame):
        print(f"\n{NEON['pink']}✖ Emergency stop triggered.{NEON['reset']}")
        self.emergency = True

    def safe_filename(self, name):
        # Remove non-ASCII and replace illegal chars
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
        return re.sub(r'[\\/*?:"<>|]', "_", name)

    def _format_time(self, sec):
        h, m = divmod(int(sec), 3600)
        m, s = divmod(m, 60)
        return f"{h:02}:{m:02}:{s:02}"

    def extract_links_and_timestamps(self, file_path):
        url_pat = re.compile(r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=[\w\-]+(?:[^\s]*)?|youtu\.be/[\w\-]+(?:[^\s]*)?))")
        ts_range_pat = re.compile(r"(\d{1,2}[:.]\d{2}(?::\d{2})?)\s*[-–]\s*(\d{1,2}[:.]\d{2}(?::\d{2})?)")
        ts_single_pat = re.compile(r"(\d{1,2}[:.]\d{2}(?::\d{2})?)")
        links = []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = list(f)
            for i, line in enumerate(lines):
                url_match = url_pat.search(line)
                if url_match:
                    url = url_match.group(1)
                    ts_start, ts_end = None, None

                    # 1. Try to find timestamp range on the same line (before OR after the URL)
                    pre_url, post_url = line.split(url, 1)
                    ts_range_match = ts_range_pat.search(pre_url)
                    if ts_range_match:
                        ts_start, ts_end = ts_range_match.group(1), ts_range_match.group(2)
                    else:
                        ts_range_match = ts_range_pat.search(post_url)
                        if ts_range_match:
                            ts_start, ts_end = ts_range_match.group(1), ts_range_match.group(2)

                    # 2. If not found, look ahead for timestamp range in next 2 lines
                    if not ts_start:
                        for next_line in itertools.islice(lines, i+1, i+3):
                            ts_range_match = ts_range_pat.search(next_line)
                            if ts_range_match:
                                ts_start, ts_end = ts_range_match.group(1), ts_range_match.group(2)
                                break

                    # 3. If still not found, look for a single timestamp in next 2 lines
                    if not ts_start:
                        for next_line in itertools.islice(lines, i+1, i+3):
                            ts_single_match = ts_single_pat.search(next_line)
                            if ts_single_match:
                                ts_start = ts_single_match.group(1)
                                ts_end = None
                                break

                    links.append((url, ts_start, ts_end))
        return links
    
    def _yt_time_to_seconds(self, t):
        # Handles formats like '1m23s', '83', '90s'
        if isinstance(t, int):
            return t
        if not t:
            return 0
        if t.isdigit():
            return int(t)
        match = re.match(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', t)
        if match:
            h, m, s = match.groups(default='0')
            return int(h) * 3600 + int(m) * 60 + int(s)
        # fallback: handle 00:00 or 00.00
        parts = list(map(int, t.replace('.', ':').split(':')))
        if len(parts) == 2:
            return parts[0]*60 + parts[1]
        elif len(parts) == 3:
            return parts[0]*3600 + parts[1]*60 + parts[2]
        return 0

    def get_info(self, vid):
        url = f"https://www.youtube.com/watch?v={vid}"
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
            return (
                self.safe_filename(info.get('title', 'Unknown')),
                int(float(info.get('duration', 0))),
                info.get("height", "N/A"),
                info.get("filesize") or info.get("filesize_approx") or 0
            )
        except Exception as e:
            print(f"{NEON['pink']}✗ Failed to get metadata: {e}{NEON['reset']}")
            return "Unknown", 0, "N/A", 0

    def download_clip(self, vid, ts_start, ts_end, folder):
        title, dur, quality, fsize = self.get_info(vid)
        if dur <= 0:
            self.failed.append(title)
            print(f"{NEON['pink']}✗ Invalid duration. Skipping.{NEON['reset']}")
            return

        # Only use the first timestamp and add 1:30 (90 seconds)
        if ts_start:
            start = self._timestamp_to_seconds(ts_start)
            end = min(start + 90, dur)
            if start >= end:
                print(f"{NEON['pink']}✗ Invalid timestamp range. Skipping.{NEON['reset']}")
                self.failed.append(title)
                return
        else:
            start = max(0, dur // 2 - 60)
            end = min(dur, start + 120)
            print(f"{NEON['blue']}⚠ No timestamp. Defaulting to 2-min middle clip.{NEON['reset']}")

        safe_title = self.safe_filename(title)
        label = f"{self._format_time(start)}-{self._format_time(end)}"
        safe_label = self.safe_filename(label).replace(":", "_")
        fname = f"{safe_title} [{safe_label}].mp4"
        outp = os.path.join(folder, fname)
        temp_outp = outp + ".part"

        if os.path.exists(outp):
            print(f"{NEON['blue']}⤴ Already exists: {fname}{NEON['reset']}")
            self.skipped.append(fname)
            return

        print(f"{NEON['green']}↓ DL:{NEON['reset']} {fname}")
        print(f"{NEON['purple']}→ Quality: {quality}p | Est. Size: {round((fsize * (end - start) / dur) / 1e6, 1)} MB{NEON['reset']}")

        video_url = f"https://www.youtube.com/watch?v={vid}"
        output_path = outp

        args = [
            "yt-dlp",
            "--no-warnings",
            "--quiet",
            "--abort-on-unavailable-fragment",
            "--retries", "3",
            "--fragment-retries", "2",
            "--no-playlist",
            "--external-downloader", "ffmpeg",
            "--external-downloader-args", f"ffmpeg_i:-ss {start} -to {end}",
            "-f", "bv[height<=1080][ext=mp4][vcodec^=avc1]",
            "-o", output_path,
            video_url
        ]

        if start != 0 or end != dur:
            args += ["--download-sections", f"*{start}-{end}"]

        for attempt in range(5):
            if self.emergency:
                print(f"{NEON['pink']}✖ Emergency stop: cleaning up...{NEON['reset']}")
                if os.path.exists(temp_outp):
                    try:
                        os.remove(temp_outp)
                        print(f"{NEON['pink']}✖ Temp file removed: {temp_outp}{NEON['reset']}")
                    except Exception as e:
                        print(f"{NEON['pink']}✖ Failed to remove temp file: {e}{NEON['reset']}")
                return
            success = self.run_yt_dlp_download(args)
            if self.emergency:
                print(f"{NEON['pink']}✖ Emergency stop: cleaning up...{NEON['reset']}")
                if os.path.exists(temp_outp):
                    try:
                        os.remove(temp_outp)
                        print(f"{NEON['pink']}✖ Temp file removed: {temp_outp}{NEON['reset']}")
                    except Exception as e:
                        print(f"{NEON['pink']}✖ Failed to remove temp file: {e}{NEON['reset']}")
                return
            if success:
                print(f"{NEON['green']}✓ Done: {fname}{NEON['reset']}")
                self.succeeded.append(fname)
                return
            else:
                print(f"{NEON['pink']}✗ Failed (attempt {attempt+1}/5){NEON['reset']}")
                if os.path.exists(temp_outp):
                    try:
                        os.remove(temp_outp)
                    except Exception:
                        pass
                time.sleep(2)
        print(f"{NEON['pink']}✗ Max retries reached. Skipping: {fname}{NEON['reset']}")
        self.failed.append(fname)

    def _report(self):
        print(f"\n{NEON['purple']}=== FINAL REPORT ==={NEON['reset']}")
        print(f"{NEON['green']}✔ Downloaded: {len(self.succeeded)}{NEON['reset']}")
        print(f"{NEON['blue']}⤴ Skipped   : {len(self.skipped)}{NEON['reset']}")
        print(f"{NEON['pink']}✗ Failed    : {len(self.failed)}{NEON['reset']}")
        print(f"{NEON['pink']}? Non-YT     : {len(self.non_youtube)}{NEON['reset']}\n")

    def run(self, filepath):
        if not os.path.isfile(filepath):
            print(f"{NEON['pink']}✖ File not found: {filepath}{NEON['reset']}")
            sys.exit(1)

        session = os.path.splitext(os.path.basename(filepath))[0]
        folder = os.path.join("downloads", session)
        os.makedirs(folder, exist_ok=True)

        links = self.extract_links_and_timestamps(filepath)
        print(f"{NEON['purple']}Found {len(links)} YT links.{NEON['reset']}")

        for url, ts_start, ts_end in links:
            vid = self.extract_yt_id(url)
            if not vid:
                self.non_youtube.append(url)
                continue
            self.download_clip(vid, ts_start, ts_end, folder)
            if self.emergency:
                break

        self._report()

    def _timestamp_to_seconds(self, ts):
        if not ts:
            return 0
        ts = ts.replace('.', ':')
        parts = list(map(int, ts.split(':')))
        if len(parts) == 3:
            return parts[0]*3600 + parts[1]*60 + parts[2]
        elif len(parts) == 2:
            return parts[0]*60 + parts[1]
        elif len(parts) == 1:
            return int(parts[0])
        return 0
    
    def run_yt_dlp_download(self, args):
        try:
            # Ensure output directory exists
            if "-o" in args:
                os.makedirs(os.path.dirname(args[args.index("-o") + 1]), exist_ok=True)
            print(f"{NEON['blue']}[DEBUG] Running: {' '.join(args)}{NEON['reset']}")
            result = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(f"{NEON['pink']}[ERROR] yt_dlp failed with exit code {result.returncode}.{NEON['reset']}")
                print(f"{NEON['orange']}[stderr]:\n{result.stderr.strip()}{NEON['reset']}")
                print(f"{NEON['orange']}[yt_dlp stderr dump]:\n{result.stderr}{NEON['reset']}")
                return False
            return True
        except Exception as e:
            print(f"{NEON['pink']}[EXCEPTION] {e}{NEON['reset']}")
            return False

    def extract_yt_id(self, url):
        """
        Extracts the YouTube video ID from a full YouTube URL or youtu.be shortlink.
        Returns None if it can't extract a valid 11-character ID.
        """
        try:
            parsed = urlparse(url)
            # Standard YouTube URL
            if "youtube.com" in parsed.netloc:
                qs = parse_qs(parsed.query)
                vid = qs.get('v', [None])[0]
                if vid and len(vid) == 11:
                    return vid
            # Short youtu.be URL
            elif "youtu.be" in parsed.netloc:
                vid = parsed.path.lstrip('/')
                if vid and len(vid) == 11:
                    return vid
        except Exception as e:
            print(f"{NEON['pink']}[extract_yt_id ERROR] {e}{NEON['reset']}")
        return None