import json
import sys

import requests

import argparse

from bs4 import BeautifulSoup

LINK = 'https://coreyms.com/'


def parse_src():
    console_args = parse_console_arguments()
    file_name = console_args.file_name
    src_link = console_args.src_link

    soup = get_html_soup(src_link)
    images_links = parse_img_links_from_soup(soup)
    not_images_links = parse_a_href_links_from_soup(soup)
    data_for_json = {'images': images_links, 'links': not_images_links}

    create_json_file(file_name, data_for_json)

    sys.exit('Done!')


def create_json_file(file_name, data_for_json):
    with open(file_name, 'w') as json_file:
        json.dump(data_for_json, json_file)


def get_html_soup(link):
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        return soup
    except Exception as exc_err:
        print(f'\nFailed to access the source {link}. It may be unavailable or you don\'t have access\n')
        sys.exit('Error message:\n' + str(exc_err))


def parse_img_links_from_soup(soup) -> list:
    images_links = []
    for image in (soup.find_all('img')):
        image_link = image['src']
        if image_link.startswith('http'):
            images_links.append(image_link)
        elif image_link.startswith('//'):
            images_links.append('https:' + image_link)
    return images_links


def parse_a_href_links_from_soup(soup) -> list:
    a_links = []
    all_a_links = soup.find_all('a')
    for a_link in all_a_links:
        href_link = a_link['href']
        if href_link.startswith('http') and href_link not in a_links:
            a_links.append(a_link['href'])
    return a_links


def parse_console_arguments():
    parser = argparse.ArgumentParser(description='Getting image links and other links to JSON file.')

    parser.add_argument('-src', '--src_link', help='URL for parsing', required=True)
    parser.add_argument('-n', '--file_name', help='Name of saved data in JSON', default='links.json')

    return parser.parse_args()


if __name__ == "__main__":
    parse_src()

