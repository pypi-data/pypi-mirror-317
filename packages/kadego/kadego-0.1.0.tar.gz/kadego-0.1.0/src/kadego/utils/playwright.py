# Standard Library Imports
import asyncio
from typing import Sequence

# Third-Party Imports
from playwright.async_api import Page, async_playwright

GAME_VARIABLES = "window.$gameVariables"
KEY_PRESS_HOLD_DOWN = .1
TIMEOUT = 100000
URL = "https://html5.plicy.net/GamePlay/155561"


async def _launch_browser(headless: bool) -> Page:
    """Launches a Chromium browser instance using Playwright and returns a
    page.

    Args:
        headless (bool): Whether to launch the browser in headless mode (without UI).

    Returns:
        Page: A Playwright Page object representing the newly opened browser page.
    """
    browser = await async_playwright().start()
    context = await browser.chromium.launch(headless=headless)
    page = await context.new_page()
    page.set_default_timeout(TIMEOUT)
    return page


async def get_kadego(headless: bool = True) -> Page:
    """Opens 漢字でGO! in a new browser instance and returns the page.

    Args:
        headless (bool, optional): Whether to run the browser in headless mode (default is True).

    Returns:
        Page: A Playwright Page object representing the page after opening 漢字でGO!.
    """
    page = await _launch_browser(headless=headless)
    await page.goto(URL)
    return page


async def press_key(page: Page, key: str) -> None:
    """Simulates pressing a key on the keyboard.

    Args:
        page (Page): The Playwright Page object.
        key (str): The key to press.
    """
    await page.keyboard.down(key)
    await asyncio.sleep(KEY_PRESS_HOLD_DOWN)
    await page.keyboard.up(key)


async def press_key_sequence(page: Page, keys: Sequence[str], delay: float) -> None:
    """Simulates pressing a sequence of keys on the keyboard.

    Args:
        page (Page): The Playwright Page object.
        keys (Sequence[str]): The sequence of keys to press.
        delay (float): The delay (in seconds) between key presses
    """
    for i, key in enumerate(keys):
        await press_key(page, key)
        if i != len(keys) - 1:
            await asyncio.sleep(delay)


async def get_game_variables(page: Page) -> dict:
    """Retrieves the current game variables from a page.

    Args:
        page (Page): The Playwright Page object.

    Returns:
        game_variables (dict): The current game variables.
    """
    game_variables = await page.evaluate(GAME_VARIABLES)
    return game_variables
