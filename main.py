"""
L4D2 Mod Checker
"""

import os
import asyncio
import platform
import shutil
import aiohttp
from retrying_async import retry
from colorama import Fore
from colorama import Style


if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.system("")  # Makes ANSI colors work


def whichlarger(first_list, second_list):
    """Gets the larger list and returns that"""
    first_count = len(first_list)
    second_count = len(second_list)
    if first_count > second_count:
        return first_list
    if second_count > first_count:
        return second_list
    return first_list


def move():
    """Asks to move the missing mods to a subfolder called 'gone'"""
    print(
        f'Would you like to move these {len(results)} mod(s) to a subfolder called "gone"? (y/n)'
    )
    do_move = input()
    if do_move.lower() == "y":
        gone_path = os.path.join(addons_path, "gone")
        if not os.path.exists(gone_path):
            os.mkdir(gone_path)
        for i in results:
            source1 = os.path.join(addons_path, f"{i}.jpg")
            dest1 = os.path.join(addons_path, "gone", f"{i}.jpg")
            source2 = os.path.join(addons_path, f"{i}.vpk")
            dest2 = os.path.join(addons_path, "gone", f"{i}.vpk")
            shutil.move(source1, dest1)
            shutil.move(source2, dest2)
        print(f"Move complete! Files will be in {gone_path}")
    elif do_move.lower() == "n":
        print("K. byebye!")


async def run(statements):
    """Runs all mods on url_checker all at the same time"""
    print("Checking...")
    await asyncio.gather(*statements)
    print(f"\n{Fore.YELLOW}Check complete!{Style.RESET_ALL}")
    if not results:
        print("No missing mods found. Have a good day! :)")
    else:
        print("The following are gone from the workshop :(")
        print("\n".join(results))
        move()


@retry(attempts=10, delay=3)
async def url_checker(mod_id, results):
    """Checks if mod exists or not on workshop"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
        ) as resp:
            content = await resp.read()
    content = content.decode("utf-8")
    if "<title>Steam Community :: Error</title>" in content:
        results.append(mod_id)
        print(f"{Fore.RED}{mod_id} is dead.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}{mod_id} is alive!{Style.RESET_ALL}")


print("Paste your addons folder (...left4dead2/addons/workshop):")
addons_path = input()
files = os.listdir(addons_path)
jpg_list = []
vpk_list = []
other_list = []
for i in files:
    if i.endswith("jpg"):
        jpg_list.append(i)
    elif i.endswith("vpk"):
        vpk_list.append(i)
    else:
        other_list.append(i)
jpg_count = len(jpg_list)
vpk_count = len(vpk_list)
if jpg_count == vpk_count:
    print(f"{jpg_count} JPGs found and {vpk_count} VPKs found. ")

else:
    print(f"{jpg_count} JPGs found and {vpk_count} VPKs found. Sussy?")
larger_list = whichlarger(jpg_list, vpk_list)
id_list = [x[:-4] for x in larger_list]
results = []
statements = []
for i in id_list:
    statements.append(url_checker(i, results))
asyncio.run(run(statements))
