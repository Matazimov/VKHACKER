from rich import print
import random


phrases = [
    'Подпишись:',
    'Эй, подпишись:',
    'Будь в курсе, подпишись:',
]

links = [
    'https://www.youtube.com/channel/UC1-IbnSQyY7xzC3Troe8MTg',
    'https://t.me/matazimov_official',
    'https://www.instagram.com/mr_qpdb'
]


def support_us():
    if random.randint(1, 20) == 10:
        print(f'[cyan]{random.choice(phrases)} {random.choice(links)}[/cyan]')
