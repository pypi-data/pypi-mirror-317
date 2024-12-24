#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#

import glob
import os
import shutil
from argparse import ArgumentParser

import requests
import wget
from bs4 import BeautifulSoup
from questionary import Separator, prompt

from brainframe_apps.capsule_control import (
    VISIONCAPSULES_EXT,
    find_localfiles,
    get_local_vcap_dir,
)


from visioncapsule_tools.command_utils import command, subcommand_parse_args, by_name

TBODY_PRODUCTION = "✨"
TBODY_REQUIRED_INPUT_TYPE = "Type:"
TBODY_REQUIRED_INPUT_DETECTIONS = "Detections:"
TBODY_REQUIRED_INPUT_TRACKED = "Tracked:"
TBODY_OUTPUT_TYPE = "Type:"
TBODY_OUTPUT_CLASSIFIES = "Classifies:"
TBODY_OUTPUT_DETECTIONS = "Detections:"
TBODY_OUTPUT_ENCODED = "Encoded:"
TBODY_OUTPUT_TRACKED = "Tracked:"
TBODY_OUTPUT_EXPAND = "Expand"

TBODY_DOWNLOAD_URL = "a"
TBODY_FILE_NAME = "FileName"


class Thead:
    thead_name: str
    thead_description: str
    thead_hardware: str
    thead_required_input: str
    thead_output: str


def connect_marketplace(marketplace_url, marketplace_path):
    # Retrieve table from remote website
    print("Connect to VisionCapsules Marketplace at " + marketplace_url)

    response = requests.get(marketplace_url + marketplace_path)
    html = response.content.decode("utf-8")  # text
    soup = BeautifulSoup(html, features="lxml")
    table = soup.find("table")

    # Parse the table
    thead = parse_thead(table)
    vcap_table = parse_table(marketplace_url, table, thead)

    return vcap_table, thead


def parse_thead(table):
    thead = Thead()

    # Parse table head
    rows = table.find("thead").find_all("tr")

    for row in rows:
        cols = row.find_all("th")
        thead.thead_name = cols[0].string.strip()
        thead.thead_description = cols[1].string.strip()
        thead.thead_hardware = cols[2].string.strip()
        thead.thead_required_input = cols[3].string.strip()
        thead.thead_output = cols[4].string.strip()

    return thead


def parse_table(marketplace_url, table, thead):
    HREF_STARTSWITH = "/release"

    # Parse table body

    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    vcap_table = []

    VisionCapsules_FullList = []
    for row in rows:
        tbody_production = ""
        tbody_required_input_type = ""
        tbody_required_input_detections = ""
        tbody_required_input_tracked = False
        tbody_output_type = ""
        tbody_output_classifies = ""
        tbody_output_detections = ""
        tbody_output_encoded = False
        tbody_output_tracked = False
        tbody_output_expand = False
        tbody_download_url = ""
        tbody_file_name = ""

        # Parse vcap download URL
        link = row.find("a")
        if link.has_attr("href"):
            linktext = link["href"]
            startswith = linktext.startswith(HREF_STARTSWITH)
            endswith = linktext.endswith(VISIONCAPSULES_EXT)
            if startswith and endswith:
                download_url = marketplace_url + linktext
                VisionCapsules_FullList.append(download_url)

                tbody_download_url = download_url
                tbody_file_name = download_url.split("/")[-1]

        cols = row.find_all("td")

        # Parse the text in the first 3 columns: Name, Description, Hardware
        tbody_name = cols[0].string
        tbody_description = cols[1].string
        if tbody_description.startswith(TBODY_PRODUCTION):
            tbody_description = tbody_description.replace(TBODY_PRODUCTION, "").strip()
            tbody_production = "Ready"

        tbody_hardware = cols[2].get_text(separator=" ").strip()

        # Parse the text in the Required Input column
        vcap_required_input = cols[3].find_all("strong")
        items = cols[3].find_all("strong")
        for item in vcap_required_input:
            item_name = item.contents[0]

            next_item = item.nextSibling
            item_value = next_item.string

            if item_name == TBODY_REQUIRED_INPUT_TYPE:
                tbody_required_input_type = item_value
            if item_name == TBODY_REQUIRED_INPUT_DETECTIONS:
                tbody_required_input_detections = str(item_value)
            if item_name == TBODY_REQUIRED_INPUT_TRACKED:
                tbody_required_input_tracked = item_value

        # Parse the text in the Output column
        vcap_output = cols[4].find("summary")
        if vcap_output:
            tbody_output_expand = True

        vcap_output = cols[4].find_all("strong")
        for item in vcap_output:

            item_name = item.contents[0]

            next_item = item.nextSibling
            item_value = next_item.string

            next_item = next_item.nextSibling
            item_detail = next_item

            if item_name == TBODY_OUTPUT_TYPE:
                tbody_output_type = item_value
            if item_name == TBODY_OUTPUT_DETECTIONS:
                tbody_output_detections = item_value
            if item_name == TBODY_OUTPUT_ENCODED:
                tbody_output_encoded = item_value
            if item_name == TBODY_OUTPUT_TRACKED:
                tbody_output_tracked = item_value
            if item_name == TBODY_OUTPUT_CLASSIFIES:
                if item_detail:
                    tbody_output_classifies = str(item_detail)
                    while next_item:
                        next_item = next_item.nextSibling  # skip a <br>
                        if next_item:
                            next_item = next_item.nextSibling
                            item_detail2 = next_item
                            tbody_output_classifies = (
                                tbody_output_classifies + ". " + str(item_detail2)
                            )

        vcap_item = {
            thead.thead_name: tbody_name,
            thead.thead_description: tbody_description,
            TBODY_PRODUCTION: tbody_production,
            thead.thead_hardware: tbody_hardware,
            # thead_required_input: vcap_required_input,
            TBODY_REQUIRED_INPUT_TYPE: tbody_required_input_type,
            TBODY_REQUIRED_INPUT_DETECTIONS: tbody_required_input_detections,
            TBODY_REQUIRED_INPUT_TRACKED: tbody_required_input_tracked,
            # thead_output:         vcap_output,
            TBODY_OUTPUT_TYPE: tbody_output_type,
            TBODY_OUTPUT_CLASSIFIES: tbody_output_classifies,
            TBODY_OUTPUT_DETECTIONS: tbody_output_detections,
            TBODY_OUTPUT_ENCODED: tbody_output_encoded,
            TBODY_OUTPUT_TRACKED: tbody_output_tracked,
            TBODY_OUTPUT_EXPAND: tbody_output_expand,
            TBODY_DOWNLOAD_URL: tbody_download_url,
            TBODY_FILE_NAME: tbody_file_name,
        }

        vcap_table.append(vcap_item)

    return vcap_table


def retrieve_vcap_url(vcap_table, vcap_file_name):
    for vcap_rol in vcap_table:
        vcap_remote_file_name = vcap_rol.get(TBODY_FILE_NAME)

        if vcap_file_name.strip() == vcap_remote_file_name.strip():
            vcap_url = vcap_rol.get(TBODY_DOWNLOAD_URL)
            return vcap_url
        else:
            pass

    print(f"Error: {vcap_file_name} not found on the VisionCapsule marketplace")


# The vcap_table is from the market place; the vcap_local_list is used to mark the
# VisionCapsules to be Selected on the Choices list.
def build_vcap_list(vcap_local_list, vcap_table, thead):
    vcap_choices = []
    last_selection_name = ""
    for vcap_rol in vcap_table:

        vcap_url = vcap_rol.get(TBODY_DOWNLOAD_URL)

        # Use the first word of the vcap file name as the section name
        vcap_remote_file_name = vcap_rol.get(TBODY_FILE_NAME)
        selection_name = vcap_remote_file_name.split("_")[0]

        exists = False
        for vcap_local_file_path in vcap_local_list:

            vcap_local_file_name = vcap_local_file_path.split("/")[-1]
            if vcap_remote_file_name == vcap_local_file_name:
                exists = True
                break
            else:
                exists = False

        if selection_name != last_selection_name:
            SeparatorText = "======== " + selection_name + " ========"
            vcap_choices.append(Separator(SeparatorText))
            last_selection_name = selection_name

        # Add VisionCapsules download url line
        vcap_choices.append({"name": vcap_url, "checked": exists})

        # Add VisionCapsules Name, Description
        vcap_text = vcap_rol.get(thead.thead_name) + ": "
        if vcap_rol.get(TBODY_PRODUCTION):
            vcap_text = (
                vcap_text + "(Production " + vcap_rol.get(TBODY_PRODUCTION) + ") "
            )

        vcap_text = vcap_text + vcap_rol.get(thead.thead_description)

        vcap_choices.append(Separator("  " + vcap_text))

        # Add VisionCapsules Hardware, Required Input, Output
        vcap_text = thead.thead_hardware + ": " + vcap_rol.get(thead.thead_hardware)
        vcap_choices.append(Separator("  " + vcap_text))

        vcap_text = (
            thead.thead_required_input + ": " + vcap_rol.get(TBODY_REQUIRED_INPUT_TYPE)
        )
        if vcap_rol.get(TBODY_REQUIRED_INPUT_TRACKED):
            vcap_text = vcap_text + ". " + TBODY_REQUIRED_INPUT_TRACKED + "True "
        if vcap_rol.get(vcap_rol.get(TBODY_REQUIRED_INPUT_DETECTIONS)):
            vcap_text = vcap_text + ". " + vcap_rol.get(TBODY_REQUIRED_INPUT_DETECTIONS)
        vcap_choices.append(Separator("  " + vcap_text))

        vcap_text = thead.thead_output + ": " + vcap_rol.get(TBODY_OUTPUT_TYPE)
        if vcap_rol.get(TBODY_OUTPUT_ENCODED):
            vcap_text = vcap_text + ". " + TBODY_OUTPUT_ENCODED + "True "
        if vcap_rol.get(TBODY_OUTPUT_TRACKED):
            vcap_text = vcap_text + ". " + TBODY_OUTPUT_TRACKED + "True "
        if vcap_rol.get(TBODY_OUTPUT_CLASSIFIES):
            vcap_text = (
                vcap_text
                + ". "
                + TBODY_OUTPUT_CLASSIFIES
                + " "
                + vcap_rol.get(TBODY_OUTPUT_CLASSIFIES)
            )
        if vcap_rol.get(TBODY_OUTPUT_DETECTIONS):
            vcap_text = (
                vcap_text
                + ". "
                + TBODY_OUTPUT_DETECTIONS
                + " "
                + vcap_rol.get(TBODY_OUTPUT_DETECTIONS)
            )
        vcap_choices.append(Separator("  " + vcap_text))
    return vcap_choices


def prompt_questions(vcap_choices):
    questions = [
        {
            "type": "checkbox",
            "qmark": "[?]",
            "message": "Select VisionCapsules",
            "name": "vcap choices",
            "choices": vcap_choices,
            "validate": lambda answer: True,
            "instruction": "(Use arrow keys to move, <space> to select, <Enter> to accept and exit."
        }
    ]

    answers = prompt(questions)

    vcap_selected_list = answers.get("vcap choices")
    return vcap_selected_list


def download_capsules(vcap_url, capsules_path, vcap_local_frig):
    vcap_local_file_name_to_be_downloaded = (
        capsules_path + "/" + vcap_url.split("/")[-1]
    )

    if not os.path.exists(vcap_local_file_name_to_be_downloaded):
        vcap_local_frig_file_name = vcap_local_frig + "/" + vcap_url.split("/")[-1]

        if os.path.exists(vcap_local_frig_file_name):
            unfreeze_capsule(
                vcap_local_frig_file_name, vcap_local_file_name_to_be_downloaded
            )
        else:
            print("\nDownloading " + vcap_url)
            try:
                wget.download(vcap_url, out=capsules_path)
            except:
                print("Failed.")


def update_capsules(vcap_local_list, vcap_url_list, capsules_path, vcap_local_frig):
    # Download selected VisionCapsules
    if vcap_url_list is not None:
        for vcap_url in vcap_url_list:
            # This function will download a capsule if it is not available on local; or unfreeze a capsule if
            # the capsule is available from vcap_local_frig
            download_capsules(vcap_url, capsules_path, vcap_local_frig)

    # Freeze unselected VisionCapsules
    for vcap_local_file in vcap_local_list:

        # Is this a developer capsule? If yes, then we don't freeze it; developer needs to manually change it
        # If there is a folder there, then it is a developer capsule
        developer_vcap_dir = os.path.splitext(vcap_local_file)[0]
        if os.path.isdir(developer_vcap_dir):
            continue

        # Is this capsule on the vcap_url_list? If yes, then we don't freeze it.
        vcap_local_file_name = vcap_local_file.split("/")[-1]
        freeze_me = True
        if vcap_url_list is not None:
            for vcap_url in vcap_url_list:
                if vcap_local_file_name in vcap_url:
                    freeze_me = False
                    break

        # Now we freeze unselected capsules
        if freeze_me:
            freeze_capsule(vcap_local_file, vcap_local_frig)


def freeze_capsule(vcap_local_file, vcap_local_frig):
    try:
        os.makedirs(vcap_local_frig, exist_ok=True)
        vcap_local_frig_file_name = (
            vcap_local_frig + "/" + vcap_local_file.split("/")[-1]
        )

        shutil.move(vcap_local_file, vcap_local_frig_file_name)
        print(f"{vcap_local_file} has frozen: {vcap_local_frig_file_name}")

    except OSError as e:
        print(
            "381 Error: %s : %s : %s" % (vcap_local_file, vcap_local_frig, e.strerror)
        )


def unfreeze_capsule(vcap_local_frig_file_name, vcap_local_file):
    try:
        shutil.move(vcap_local_frig_file_name, vcap_local_file)
        print(f"{vcap_local_file} has frozen.")

    except OSError as e:
        print(
            "Error: %s : %s : %s"
            % (vcap_local_file, vcap_local_frig_file_name, e.strerror)
        )


def remove_capsules(vcap_local_file):
    try:
        os.remove(vcap_local_file)
        print(f"{vcap_local_file} has been removed.")

    except OSError as e:
        print("Error: %s : %s" % (vcap_local_file, e.strerror))


def remove_all_capsules(vcap_local_file):
    files = glob.glob(vcap_local_file + "/*")
    for f in files:
        try:
            os.remove(f)
            print(f"{f} has been removed.")

        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def delete_capsules(vcap_files, vcap_dir):
    if vcap_files:
        for file_name in vcap_files:
            remove_capsules(vcap_dir + "/" + file_name)
    else:
        remove_all_capsules(vcap_dir)


def freeze_all_capsules(vcap_local_file, vcap_local_frig):
    files = glob.glob(vcap_local_file + "/*")
    for f in files:
        try:
            freeze_capsule(f, vcap_local_frig)

        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def freeze_capsules(vcap_local_files, vcap_local_dir, vcap_local_frig):
    if vcap_local_files:
        for file_name in vcap_local_files:
            file_path = vcap_local_dir + "/" + file_name
            freeze_capsule(file_path, vcap_local_frig)
    else:
        freeze_all_capsules(vcap_local_dir, vcap_local_frig)


def list_local_capsules(vcap_dir, vcap_frig):
    print("Current VisionCapsules:")

    vcap_files = [f for f in os.listdir(vcap_dir) if f.endswith(VISIONCAPSULES_EXT)]
    if vcap_files is not None:
        print("\n    + " + "\n    + ".join(vcap_files) + "\n")
    else:
        print("    empty\n")

    if vcap_dir != vcap_frig:
        print("Current frozen VisionCapsules:")

        vcap_frig_files = [
            f for f in os.listdir(vcap_frig) if f.endswith(VISIONCAPSULES_EXT)
        ]
        if vcap_frig_files is not None:
            print("\n    + " + "\n    + ".join(vcap_frig_files) + "\n")
        else:
            print("    empty\n")

    return


def capsule_downloader_load_capsules(prompt, vcap_files, vcap_dir, vcap_frig):
    WEBSITE_URL = "https://aotu.ai"
    WEBSITE_PATH = "/docs/downloads/"

    # Download table from VisionCapsules marketplace
    vcap_table, thead = connect_marketplace(WEBSITE_URL, WEBSITE_PATH)

    # Build VisionCapsules lists from local path. We only care about capsule files.
    vcap_local_list = find_localfiles("*" + VISIONCAPSULES_EXT, vcap_dir)

    # Here we build up the final capsule list based on the input from prompt question or command line input.
    vcap_url_list = []
    if prompt:
        # Build VisionCapsules question list
        vcap_choices = build_vcap_list(vcap_local_list, vcap_table, thead)

        # The prompt is a concept of the marketplace. A list of capsules downloaded from the website live
        # will show up as prompt questions for user to select. If a capsule has been downloaded, the item
        # will be marked as selected.
        vcap_url_list = prompt_questions(vcap_choices)

    if vcap_files:
        # If user specify a capsule filename from the command line, we first check if the capsule filename
        # is available from the marketplace. If yes, we will append to the url list.
        for file_name in vcap_files:
            vcap_url = retrieve_vcap_url(vcap_table, file_name)
            if vcap_url:
                # download_capsules(vcap_url, args.vcap_dir)
                vcap_url_list.append(vcap_url)
            else:
                # This might be a capsule in capsule_frig?
                vcap_url_list.append(file_name)

    # Now we know what are the capsules user wants to use (vcap_url_list); and what are the capsules on
    # the local storage (vcap_local_list), it is the time to download the VisionCapsules that is not local.
    update_capsules(vcap_local_list, vcap_url_list, vcap_dir, vcap_frig)


def __parse_args__(default_vcap_local_dir, default_vcap_local_frig):
    parser = ArgumentParser(
        description="A helper utility for downloading BrainFrame capsules."
    )

    parser.add_argument(
        "--vcap-dir",
        default=default_vcap_local_dir,
        help=f"The path to the BrainFrame capsule directory. default is {default_vcap_local_dir}",
    )

    parser.add_argument(
        "--vcap-frig",
        default=default_vcap_local_frig,
        help=f"The path to the BrainFrame capsule frig. default is {default_vcap_local_frig}",
    )

    parser.add_argument(
        "--vcap-files",
        nargs="+",
        help="The capsule files to be downloaded. A selection list will be prompt if the argument is not provided",
    )

    parser.add_argument(
        "--delete",
        action="store_true",
        help="The capsule file to be removed. default is all local capsules will be deleted",
    )

    parser.add_argument(
        "--freeze",
        action="store_true",
        help="Freeze the capsules",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List the local capsules",
    )

    parser.add_argument(
        "--download",
        action="store_true",
        default=True,
        help="Download capsules",
    )

    args = subcommand_parse_args(parser)
    return args


@command("capsule_downloader")
def capsule_downloader_main():
    default_vcap_local_dir, _ = get_local_vcap_dir()
    if not os.path.isdir(default_vcap_local_dir):
        default_vcap_local_dir = "./"
    args = __parse_args__(default_vcap_local_dir, "./")

    if args.delete:
        delete_capsules(args.vcap_files, args.vcap_dir)
    elif args.freeze:
        freeze_capsules(args.vcap_files, args.vcap_dir, args.vcap_frig)
    elif args.list:
        list_local_capsules(args.vcap_dir, args.vcap_frig)
    elif args.download:
        capsule_downloader_load_capsules(
            args.download, args.vcap_files, args.vcap_dir, args.vcap_frig
        )

    list_local_capsules(args.vcap_dir, args.vcap_frig)


if __name__ == "__main__":
    by_name["capsule_downloader"]()
