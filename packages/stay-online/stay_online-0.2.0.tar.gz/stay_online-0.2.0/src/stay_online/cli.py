from stay_online.stay_online import stay_online
from stay_online.constants import HELP_MAX_DELAY_SECONDS, HELP_MAX_NUM_WORDS, HELP_MIN_DELAY_SECONDS, HELP_MIN_NUM_WORDS, HELP_SHOW_TIMESTAMP, HELP_STOP_HHMM


def cli_stay_online():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--stop', dest='stop_hhmm', type=str, help=HELP_STOP_HHMM)
    parser.add_argument('--min_delay', dest='min_delay_seconds', type=int, help=HELP_MIN_DELAY_SECONDS)
    parser.add_argument('--max_delay', dest='max_delay_seconds', type=int, help=HELP_MAX_DELAY_SECONDS)
    parser.add_argument('--min_words', dest='min_num_words', type=int, help=HELP_MIN_NUM_WORDS)
    parser.add_argument('--max_words', dest='max_num_words', type=int, help=HELP_MAX_NUM_WORDS)
    parser.add_argument('--timestamp', dest='show_timestamp', type=bool, help=HELP_SHOW_TIMESTAMP)
    args = parser.parse_args()

    stay_online_kwargs = {}
    
    if args.stop_hhmm:
        stay_online_kwargs['stop_hhmm'] = args.stop_hhmm
    if args.min_delay_seconds:
        stay_online_kwargs['min_delay_seconds'] = args.min_delay_seconds
    if args.max_delay_seconds:
        stay_online_kwargs['max_delay_seconds'] = args.max_delay_seconds
    if args.min_num_words:
        stay_online_kwargs['min_num_words'] = args.min_num_words
    if args.max_num_words:
        stay_online_kwargs['max_num_words'] = args.max_num_words
    if args.show_timestamp:
        stay_online_kwargs['show_timestamp'] = args.show_timestamp

    stay_online(**stay_online_kwargs)
    return
