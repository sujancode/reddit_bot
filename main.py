from bots.account_create import run as account_create
from bots.poster import run as poster
from bots.post_creator import run as post_creator
from bots.commenter import run as commentor
import sys

def main():
    args=sys.argv
    print(args)
    if args[1]=="account":
        account_create()
    elif args[1]=="poster":
        poster()
    elif args[1]=="post_creator":
        post_creator()
    elif args[1]=="commentor":
        commentor()
    else:
        print("Will do Nothing")

    
main()


