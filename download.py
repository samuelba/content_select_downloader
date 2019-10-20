#!/usr/bin/env python3

import argparse
import os
import re

from bs4 import BeautifulSoup
from requests_html import HTMLSession

from PyPDF2 import PdfFileMerger


class ContentSelectDownloader:
    def __init__(self):
        self.url = ''
        self.output = 'result.pdf'
        self.parse_arguments()

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--url", dest="url",
                            help="Url to the PDF on https://content-select.com/",
                            type=str, required=True)
        parser.add_argument("--output", dest="output",
                            help="Name of the resulting PDF.",
                            type=str)
        args = parser.parse_args()
        if args.url:
            self.url = args.url
        else:
            print("No url defined.")
            exit(0)
        if args.output:
            self.output = args.output
            if not self.output.endswith(".pdf"):
                self.output = self.output + '.pdf'
        print("Download from url: " + self.url)
        print("Resulting PDF name: " + self.output)

    @staticmethod
    def get_pdf_id(url):
        print("Get PDF id.")
        result = re.search(r"moz_viewer\/([a-z0-9\-]*)\/", url)
        pdf_id = ''
        if result:
            pdf_id = result.group(1)
            print("PDF id: " + pdf_id)
            return pdf_id
        else:
            print("Could not get PDF id from url: " + url)
            exit(0)

    @staticmethod
    def get_chapter_ids(url):
        print("Get chapter ids.")
        session = HTMLSession()
        resp = session.get(url)
        resp.html.render()

        soup = BeautifulSoup(resp.html.html, "lxml")
        # outlineItems = soup.select("div.outlineItem a")
        print_list_items = soup.select("#printList a")

        print("Chapter ids:")
        chapter_ids = list()
        for item in print_list_items:
            chapter_id = item["data-chapter-id"]
            chapter_ids.append(chapter_id)
            print(chapter_id)

        return chapter_ids

    @staticmethod
    def download_pdfs(pdf_id, chapter_ids):
        print("Download PDFs.")
        files = list()
        counter = 1
        for chapter_id in chapter_ids:
            file_name = 'tmp_' + str(counter) + '.pdf'
            url = 'https://content-select.com/media/display/' + pdf_id + '/' + chapter_id + '#pdfjs.action=download'
            print("Download PDF " + str(counter) + " of " + str(len(chapter_ids)) + " from: " + url)
            os.system('curl ' + url + ' --output ' + file_name)
            files.append(file_name)
            counter = counter + 1

        return files

    @staticmethod
    def merge_pdfs(files, output):
        print("Merge PDFs.")
        merger = PdfFileMerger()

        for pdf in files:
            merger.append(pdf)

        merger.write(output)
        merger.close()

    @staticmethod
    def clean_up(files):
        print("Clean up.")
        for pdf in files:
            os.system('rm ' + pdf)

    def run(self):
        pdf_id = self.get_pdf_id(self.url)
        chapter_ids = self.get_chapter_ids(self.url)
        files = self.download_pdfs(pdf_id, chapter_ids)
        self.merge_pdfs(files, self.output)
        self.clean_up(files)


if __name__ == '__main__':
    downloader = ContentSelectDownloader()
    downloader.run()
