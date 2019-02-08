import math
import discord
import central
from handlers.logic.commands.settings import versions
from bible_modules import biblehub, bibleserver, biblesorg, biblegateway, rev


def search(version, query, lang):
    biblehub_versions = ["BSB", "NHEB", "WBT"]
    bibleserver_versions = ["LUT", "LXX", "SLT"]
    biblesorg_versions = ["KJVA"]
    other_versions = ["REV"]
    non_bible_gateway = other_versions + biblehub_versions + biblesorg_versions + bibleserver_versions

    if version not in non_bible_gateway:
        results = biblegateway.search(version, query)

        if results is not None:
            query.replace("\"", "")

            pages = []
            max_results_per_page = 6
            total_pages = int(math.ceil(len(results.keys()) / max_results_per_page))

            if total_pages == 0:
                total_pages += 1
            elif total_pages > 100:
                total_pages = 100

            for i in range(total_pages):
                embed = discord.Embed()

                embed.title = lang["searchResults"] + " \"" + query + "\""

                page_counter = lang["pageOf"].replace("<num>", str(i + 1)).replace("<total>", str(total_pages))
                embed.description = page_counter

                embed.color = 303102
                embed.set_footer(text=f"BibleBot {central.version}", icon_url=central.icon)

                if len(results.keys()) > 0:
                    count = 0

                    for key in list(results.keys()):
                        if len(results[key]["text"]) < 700:
                            if count < max_results_per_page:
                                title = results[key]["title"]
                                text = results[key]["text"]

                                embed.add_field(name=title, value=text, inline=False)

                                del results[key]
                                count += 1
                else:
                    embed.title = lang["nothingFound"].replace("<query>", query)
                    embed.description = ""

                pages.append(embed)

            if len(pages) > 1:
                return {
                    "level": "info",
                    "paged": True,
                    "pages": pages
                }
            else:
                return {
                    "level": "info",
                    "message": pages[0]
                }
    else:
        return {
            "level": "err",
            "message": lang["searchNotSupported"].replace("<search>", lang["commands"]["search"])
        }


def get_versions(lang):
    pages = []
    available_versions = versions.get_versions()
    max_results_per_page = 25

    total_pages = int(math.ceil(len(available_versions) / max_results_per_page))

    if total_pages == 0:
        total_pages += 1

    for i in range(total_pages):
        embed = discord.Embed()

        embed.color = 303102
        embed.set_footer(text=f"BibleBot {central.version}", icon_url=central.icon)

        if len(available_versions) > 0:
            count = 0
            version_list = ""

            available_versions_copy = available_versions[:]
            for item in available_versions_copy:
                if count < max_results_per_page:
                    version_list += item + "\n"
                    count += 1

                    available_versions.remove(item)
                else:
                    break

            page_counter = lang["pageOf"].replace("<num>", str(i + 1)).replace("<total>", str(total_pages))

            embed.title = central.cmd_prefix + lang["commands"]["versions"] + " - " + page_counter
            embed.description = version_list

            pages.append(embed)

    return {
        "level": "info",
        "paged": True,
        "pages": pages
    }
