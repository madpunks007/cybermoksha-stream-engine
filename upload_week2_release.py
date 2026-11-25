import os
import sys
import json
import urllib.request
import urllib.error

WEEK2_DIR = r"C:\Users\Lenovo\.gemini\antigravity\scratch\cybermoksha_week2"
REPO = "madpunks007/cybermoksha-stream-engine"
TAG = "v2.0"

FILES_TO_UPLOAD = [
    os.path.join(WEEK2_DIR, "Master_Week2_Full7Days_70Min.mp4"),
    os.path.join(WEEK2_DIR, "Day1_Mon_NeonTokyo", "Master_W2_Day1_Mon_NeonTokyo.mp4"),
    os.path.join(WEEK2_DIR, "Day2_Tue_DeepSpace", "Master_W2_Day2_Tue_DeepSpace.mp4"),
    os.path.join(WEEK2_DIR, "Day3_Wed_SynthHighway", "Master_W2_Day3_Wed_SynthHighway.mp4"),
    os.path.join(WEEK2_DIR, "Day4_Thu_OrbitalStation", "Master_W2_Day4_Thu_OrbitalStation.mp4"),
    os.path.join(WEEK2_DIR, "Day5_Fri_UnderwaterDome", "Master_W2_Day5_Fri_UnderwaterDome.mp4"),
    os.path.join(WEEK2_DIR, "Day6_Sat_CyberZen", "Master_W2_Day6_Sat_CyberZen.mp4"),
    os.path.join(WEEK2_DIR, "Day7_Sun_AstralHorizon", "Master_W2_Day7_Sun_AstralHorizon.mp4"),
]

def main():
    token = os.environ.get("GH_PAT", "").strip()
    if not token and len(sys.argv) > 1:
        token = sys.argv[1].strip()

    if not token:
        print("[!] ERROR: GH_PAT environment variable or token argument is required.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "CyberMokshaUploader"
    }

    # 1. Check or Create Release v2.0
    print(f"[*] Checking release {TAG} on {REPO}...")
    release_url = f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}"
    release = None
    try:
        req = urllib.request.Request(release_url, headers=headers)
        with urllib.request.urlopen(req) as res:
            release = json.loads(res.read().decode())
            print(f"[+] Found existing release {TAG} (ID: {release['id']})")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[*] Creating new release {TAG}...")
            create_url = f"https://api.github.com/repos/{REPO}/releases"
            payload = json.dumps({
                "tag_name": TAG,
                "name": "CYBERMOKSHA Week 2 - 24/7 Master Videos",
                "body": "Seamless 1080p Master Videos and 70-Minute Full Playlist for 24/7 Live Streaming",
                "draft": False,
                "prerelease": False
            }).encode()
            create_req = urllib.request.Request(create_url, data=payload, headers=headers)
            with urllib.request.urlopen(create_req) as res:
                release = json.loads(res.read().decode())
                print(f"[+] Created release {TAG} (ID: {release['id']})")
        else:
            raise

    upload_base = release["upload_url"].split("{")[0]
    existing_assets = {a["name"]: a["id"] for a in release.get("assets", [])}

    # 2. Upload assets
    for filepath in FILES_TO_UPLOAD:
        if not os.path.exists(filepath):
            print(f"[!] Warning: File not found: {filepath}")
            continue

        filename = os.path.basename(filepath)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)

        if filename in existing_assets:
            print(f"[*] Deleting existing asset {filename} (ID: {existing_assets[filename]})...")
            del_url = f"https://api.github.com/repos/{REPO}/releases/assets/{existing_assets[filename]}"
            del_req = urllib.request.Request(del_url, headers=headers, method="DELETE")
            try:
                with urllib.request.urlopen(del_req) as res:
                    pass
            except Exception as ex:
                print(f"[!] Failed to delete old asset: {ex}")

        print(f"[*] Uploading {filename} ({size_mb:.1f} MB)...")
        up_url = f"{upload_base}?name={filename}"
        with open(filepath, "rb") as f:
            data = f.read()

        up_headers = dict(headers)
        up_headers["Content-Type"] = "video/mp4"
        up_headers["Content-Length"] = str(len(data))

        up_req = urllib.request.Request(up_url, data=data, headers=up_headers)
        with urllib.request.urlopen(up_req) as res:
            res_data = json.loads(res.read().decode())
            print(f"[+] Uploaded {filename} successfully! (Asset ID: {res_data['id']})")

    print("\n[+] All Week 2 release assets deployed successfully!")

if __name__ == "__main__":
    main()
