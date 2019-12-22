# Youtube Terminal Viewer

YTV is an experimental Youtube feed fetcher for the terminal. This is aimed to help me choose videos from my Youtube feed faster and easier.

For now, the feed can be cached by using `get_youtube.py`, which uses a selenium controlled Firefox instance to fetch the contents. Then the feed is processed and watched by the `ytv.sh` script, which uses `fzf` as a simple interface, and contains an incomplete implementation of video queues and watch history.
