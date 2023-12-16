from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def parse(user_input):
    command = user_input.split(':')[0]
    args = user_input.split(':')[1].split(',')
    return command, args


def main():
    while True:
        user_input = input('Enter command: ')
        if user_input.lower() == 'exit':
            exit()
        elif user_input.startswith('name:') or user_input.startswith('tag:') or user_input.startswith('tags:'):
            command, args = parse(user_input)
            if command == 'name':
                print(find_by_author(*args))
            elif command == 'tag':
                print(find_by_tag(*args))
            elif command == 'tags':
                for tag in args:
                    print(find_by_tag(tag))
        else:
            print("Unknown command. Please type one of the commands: 'name:', 'tag:', 'tags:', 'exit'.")


if __name__ == '__main__':
    main()
