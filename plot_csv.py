import matplotlib.legend
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np
import pandas as pd
from scipy.ndimage.filters import gaussian_filter1d

"""
Use this class to create plots from csv files from tensorboard

"""
parser = argparse.ArgumentParser(description='Setup your Environment.')
parser.add_argument("-f", "--folder", help="Enter folder, where plots are", type=str)
parser.add_argument("-s", "--sigma", help="Enter smoothing factor sigma. Default 1 not smooth. 2 smoother", default=1, type=int)
parser.add_argument("-n", "--name", help="Name the plot.", default="plot", type=str)
args = parser.parse_args()

plt.figure(figsize=(19,10))
folder = args.folder
if os.path.isdir(folder):
    files = os.listdir(folder)
    max_y = 0
    min_y = 1000
    for file in files:
        if "Value Loss" in file:
            value_loss = pd.read_csv(folder + "\\" + file, index_col=1)
            vals = [i[1] for i in value_loss.values]
            vals = gaussian_filter1d(vals, sigma=args.sigma)
            if max(vals) > max_y: max_y = max(vals) + 1
            if min(vals) < min_y: min_y = min(vals) - 1
            index = value_loss.index
            value_loss = pd.DataFrame(data=vals, index=index)
            plt.plot(value_loss, label="Value_Loss")
        elif "Entropy Loss" in file:
            entropy_loss = pd.read_csv(folder + "\\" + file, index_col=1)
            vals = [i[1] for i in entropy_loss.values]
            vals = gaussian_filter1d(vals, sigma=args.sigma)
            if max(vals) > max_y: max_y = max(vals) + 1
            if min(vals) < min_y: min_y = min(vals) - 1
            index = entropy_loss.index
            entropy_loss = pd.DataFrame(data=vals, index=index)
            plt.plot(entropy_loss, label="Entropy_Loss")
        elif "Policy Loss" in file:
            policy_loss = pd.read_csv(folder + "\\" + file, index_col=1)
            vals = [i[1] for i in policy_loss.values]
            vals = gaussian_filter1d(vals, sigma=args.sigma)
            if max(vals) > max_y: max_y = max(vals) + 1
            if min(vals) < min_y: min_y = min(vals) - 1
            index = policy_loss.index
            policy_loss = pd.DataFrame(data=vals, index=index)
            plt.plot(policy_loss, label="Policy_Loss")
        else:
            if not "loss" in file:
                continue
            episode_loss = pd.read_csv(folder + "\\" + file, index_col=1)
            vals = [i[1] for i in episode_loss.values]
            vals = gaussian_filter1d(vals, sigma=args.sigma)
            if max(vals) > max_y: max_y = max(vals) + 1
            if min(vals) < min_y: min_y = min(vals) - 1
            index = episode_loss.index
            episode_loss = pd.DataFrame(data=vals, index=index)
            plt.plot(episode_loss, label="Episode_Loss")
    plt.legend(loc="upper left")
    axes = plt.gca()
    axes.set_ylim([min_y, max_y])
    plt.xlabel("Episodes")
    plt.ylabel("Loss")
    plt.savefig("plots\\" + args.name + "_losses.png")
    plt.show()
    plt.close()
    for file in files:
        if not "loss" in file:
            if "Entropy" in file:
                plt.figure(figsize=(19,10))
                entropy = pd.read_csv(folder + "\\" + file, index_col=1)
                vals = [i[1] for i in entropy.values]
                vals = gaussian_filter1d(vals, sigma=args.sigma)
                index = entropy.index
                entropy = pd.DataFrame(data=vals, index=index)
                plt.plot(entropy, label="Entropy")
                plt.legend(loc="upper left")
                axes = plt.gca()
                axes.set_ylim([min(vals)-0.1, max(vals)+0.1])
                plt.xlabel("Episodes")
                plt.ylabel("Entropy")
                plt.savefig("plots\\" + args.name + "_entropy.png")
                plt.show()
                plt.close()
            if "Discounted Return" in file:
                plt.figure(figsize=(19,10))
                disc_return = pd.read_csv(folder + "\\" + file, index_col=1)
                vals = [i[1] for i in disc_return.values]
                vals = gaussian_filter1d(vals, sigma=args.sigma)
                index = disc_return.index
                disc_return = pd.DataFrame(data=vals, index=index)
                plt.plot(disc_return, label="Discounted Return")
                plt.legend(loc="upper left")
                axes = plt.gca()
                axes.set_ylim([min(vals)-10, max(vals)+10])
                plt.xlabel("Episodes")
                plt.ylabel("Value")
                plt.savefig("plots\\" + args.name + "_discReturn.png")
                plt.show()
                plt.close()

