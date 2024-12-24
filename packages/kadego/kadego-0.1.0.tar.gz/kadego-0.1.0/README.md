# kadego

`kadego` is a python package for running bots to play the browser game [漢字でGO!](https://plicy.net/GamePlay/155561).

This package allows you to automate gameplay, collect data (like readings and meanings), and customize game-playing strategies.

## 📦 Structure

This package provides five main objects to work with: `Bot`, `Logger`, `Observer`, `Strategy` and `Runner`.

### 🦾 Bot

The `Bot` is the one actually playing the game.

When calling its `launch` method it navigates to the provided `mode` and `level`, sets the provided number of `lives` and `questions` and finally enters into the `level`. Calling the `run` method will then make the bot play a full game answering questions according to the specified `strategy` and logging answers with the specified `logger`.

### 📜 Logger

A `Logger` logs data from the game.

Its `log` method is called each time an answer is presented to the associated `Bot` and provided with the current `gameVariables`. An example use case would be storing readings and meanings to a JSON file.

### 👀 Observer

An `Observer` runs in parallel to a `Bot`.

Its `observe` method runs continuously and can perform actions depending on the state of the `Bot` or any outside factors. One of these actions can be stopping the `Runner` from continuing to run the `Bot`. An example use case would be stopping the `Bot` after a certain amount of time or when the intended task has been completed.

### 🧠 Strategy

A `Strategy` returns an answer and the corresponding outcome when presented with a question.

Its `solve` method is called each time the associated `Bot` is presented with a question. The `Strategy` will then depending on the `gameVariables` and the current `GameStatus` choose a `Solver` to provide an answer and the associated outcome. An example use case would be acing the game by always choosing the right answer.

### 🚀 Runner

A `Runner` is responsible for concurrently running a `Bot` together with an `Observer`.

Its `run` method runs the specified `Bot` by first calling its `launch` method and the repeatedly calling its `run` method until a signal to stop is sent. Additionally, it also runs the specified `Observer` by calling its `observe` method.

## 🗺️ Map

The different game modes are conceptualized as a `WorldMap` which the `Bot` uses to navigate namely the `KanjiDeGoMap`.

### ⚙️ Main

The main (メイン) `mode` has `levels`:
- easy (ノーマル)
- hard (ハード)
- very_hard (ゲキムズ)
- hell (ヘル)

### 🔄 Casual

The casual (カジュアル) `mode` has `levels`:
- basic (ベーシック)
- variety (バラエティ)
- variety_hard (鬼・バラエティ)
- one_character (一文字)
- four_characters (四字熟語)
- places (国・都市の名前)
- bugs (虫の名前)
- mammals (哺乳類の名前)
- birds (鳥の名前)
- aquatic (水性物の名前)
- plants (植物の名前)
- food (グルメ・調味料)

### ⏱️ Rush

The rush (ラッシュ) `mode` has `levels`:
- level_1 (１ラッシュ)
- level_2 (２ラッシュ)
- level_3 (３ラッシュ)
- level_4 (４ラッシュ)
- level_5 (５ラッシュ)
- level_6 (６ラッシュ)

### 🌟 Extra
extra (エクストラ) `mode` has `levels`:
- math (数学アタック)
- math_hard (鬼・数学アタック)
- english (英語・アタック)
- elements (元素記号)

## ⚙️ Installation

To install kadego, run
```bash
pip install kadego
```

## 📚 Example Usage

To run a bot that scrapes all the readings and meanings for words from a single level, you can run the following.
````python
import asyncio
from kadego import get_kadego
from kadego.runners import SingleLevelScraper


async def run(level: int, log_path: str) -> None:
    kadego = await get_kadego()
    runner = SingleLevelScraper(kadego, level, log_path)

    await runner.run()


if __name__ == "__main__":
    example_level = 1
    exampe_log_path = "/path/to/store/data/to"
    asyncio.run(run(example_level, exampe_log_path))
````
The bot will then run until the data for all words has been collected.

## 🛠️ Troubleshooting

`漢字でGO!` might crash or time out from time to time. This will in turn crash the `Bot` meaning you wil need to rerun your script.

## 📝 Changelog

v0.1.0 — Initial release (based on 漢字でGO! v1.1.2.2b).
