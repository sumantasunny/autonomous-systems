import argparse
import re
import os
from datetime import datetime


def str2bool(str):
    if str.lower() in ["false", "f", "0"]:
        return False
    return True


def collect():
    parser = argparse.ArgumentParser(description='Setup your Environment.')
    parser.add_argument("--domain", help="Enter 'wurmi', 'car', 'pendel' or 'lunar'. Wurmi is default", type=str)
    parser.add_argument("--checkpoint",
                        help="Enter the path to the checkpoint you want to start from. Make sure it fits your Environment!",
                        type=str)
    parser.add_argument("--learn", help="Enter True for Training mode", type=str2bool)
    parser.add_argument("--check_step", help="The amount of Episodes when a checkpoint will be created", type=int)
    parser.add_argument("--no_graphics", help="True or false", type=str2bool)
    parser.add_argument("--episodes", help="Set amnt. of Episodes", type=int)
    parser.add_argument('--file', help="Enter path to a file containing arguments.(--file args.txt)", type=open,
                        action=LoadFromFile)
    return parser.parse_args()
import argparse


def collect():
    parser = argparse.ArgumentParser(description='Define the parameter for Captain Wurmi')
    parser.add_argument("-e", "--episodes", default=5, metavar='N', type=int,
                        help='Define the number of episodes')

    parser.add_argument("-m", "--model", default="ppo.nn", metavar='S', type=str, help='Define the model to be used/overwritten')
    parser.add_argument("-g", "--graphics", default=False, metavar='B', type=str2bool, help="Define if graphics should be shown")



def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None


def get_domain():
    args = collect()
    if args.domain is None:
        return "wurmi"
    return args.domain


def get_checkpoint_dir(domain, dir=""):
    args = collect()
    if args.checkpoint:
        return os.path.dirname(args.checkpoint) + "\\"
    elif not dir:
        cur_time = datetime.now()
        checkpoint_dir = "models\\" + domain + "_" + str(cur_time.day) + str(cur_time.month) + str(cur_time.year)[:2] + \
                         "-" + str(cur_time.hour) + "_" + str(cur_time.minute) + "\\"
        if not os.path.isdir(checkpoint_dir):
            os.mkdir(checkpoint_dir)
        return checkpoint_dir
    else:
        return dir


def get_checkpoint_model(dir="", best=False):
    """
    :return: Path to checkpoint file, Path to checkpoint dir, Number of last Episode
    """
    args = collect()
    if args.checkpoint:
        checkpoint_path = args.checkpoint
        if os.path.isfile(checkpoint_path):
            if checkpoint_path.endswith("_best.nn"):
                start = get_trailing_number(checkpoint_path.replace("_best.nn", ""))
            else:
                start = get_trailing_number(checkpoint_path.replace(".nn", ""))
            checkpoint_dir = os.path.dirname(checkpoint_path) + "\\"
            return checkpoint_path, start, True
        else:
            print("Error reading Checkpoint-File '", checkpoint_path, "'")
            exit(-1)
    elif dir:
        domain = get_domain()
        checkpoint_dir = dir
        if not os.path.isdir(checkpoint_dir):
            os.mkdir(checkpoint_dir)
        if best:
            return checkpoint_dir + domain + "_best.nn", 0, False
        else:
            return checkpoint_dir + domain + ".nn", 0, False

    else:
        # Create new checkpoint file
        domain = get_domain()
        checkpoint_dir = get_checkpoint_dir(domain)
        if not os.path.isdir(checkpoint_dir):
            os.mkdir(checkpoint_dir)
        return checkpoint_dir + domain + ".nn", 0, False


def remove_best(checkpoint_dir):
    test = os.listdir(checkpoint_dir)
    for item in test:
        if item.endswith("_best.nn"):
            os.remove(os.path.join(checkpoint_dir, item))


def get_check_step():
    args = collect()
    if args.check_step is None:
        return 500
    return args.check_step


def get_learn():
    args = collect()
    if args.learn is None:
        return True
    return args.learn


def get_no_graphics():
    args = collect()
    if args.no_graphics is None:
        return True
    return args.no_graphics


def get_episodes():
    args = collect()
    if args.episodes is None:
        return 1000
    return args.episodes


def get_save_model(domain, last_episode, dir="", is_best=False):
    dir = get_checkpoint_dir(domain, dir)
    return dir + domain + "-" + str(last_episode) + ("_best.nn" if is_best else ".nn")


class LoadFromFile(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            # parse arguments in the file and store them in the target namespace
            parser.parse_args(f.read().split(), namespace)
