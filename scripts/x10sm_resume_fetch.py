"""Resume polling and fetch of the Sarvam-m X10 ITRANS kernel after the laptop reboot of 2026-11-09 02:31 killed the chain's poller (the Kaggle kernel itself kept running). Account 3."""
import os, sys
os.environ["KAGGLE_ACCOUNT"] = "3"
sys.path.insert(0, "scripts"); sys.path.insert(0, "src")
import kaggle_runner as k
k.fetch("kaggle_x10", wait=True)
