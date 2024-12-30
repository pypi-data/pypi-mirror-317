#!/usr/bin/env python

import sys
import requests
from pathlib import Path
import psutil
from tqdm import tqdm

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

class TipToiDL:
    def __init__(self):
        self.catalog_url = (
            "https://bouni.github.io/tiptoi-dl/products.json"
        )
        self.products = []
        self.download_catalog()
        self.main()

    def download_catalog(self):
        r = requests.get(self.catalog_url, timeout=10)
        self.products = r.json()

    def main(self):
        print("=" * 80)
        print("\nWelcome to TipToi-dl, a CLI TipToi audio file downloader.\n")
        print("=" * 80)
        while True:
            self.results = []
            s = input("\nEnter search term or 'q' to quit: ")
            if s == "q":
                break
            if s != "":
                self.search(s)
            if len(self.results) == 0:
                print("\n  No results found")
                continue
            print(f"\n  Found {len(self.results)} results!\n")
            for n, r in enumerate(self.results, 1):
                print(f"  [{n}] {r["title"]}")
            print("\n")
            s = input("Select item by entering number, q to quit: ")
            if s == "q":
                break
            try:
                n = int(s)
            except ValueError:
                print("\n  Not a vaild selection, quit ...")
                sys.exit(1)
            if n < 0 or n > len(self.results):
                print("\n  Not a valid selection, quit ...")
                break
            print(f"\n  Your selection: {self.results[n-1]['title']}")
            self.download(self.results[n-1]["gme"])


    def search(self, searchterm: str):
        for item in self.products:
            if searchterm.lower() in item["title"].lower():
                self.results.append(item)

    def download(self, url: str):
        print(f"\n  Download {url}")
        filename = url.split("/")[-1]
        disk = self.find_tiptoi_disk()
        if not disk:
            path = Path.home() / filename
        else:
            path = Path(disk) / filename
        print(f"  Download file to {path}")
        resp = requests.get(url, stream=True)
        total = int(resp.headers.get('content-length', 0))
        with open(path, 'wb') as file, tqdm(
            desc=filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

    def find_tiptoi_disk(self):
        disks = [
            p.mountpoint
            for p in psutil.disk_partitions(all=True)
            if "/dev/" in p.device.lower() and "toi" in p.mountpoint.lower()
        ]
        if len(disks) == 1:
            return disks[0]
        else:
            print("  Cannot find tiptoi disk ...")
            return None


def main():
    ttdl = TipToiDL()

if __name__ == "__main__":
    main()
