def rps(p1, p2):

    if p1 == "scissors" and p2 == "paper":
        print("p1 wins")
    elif p1 == "paper" and p2 == "rock":
        print("p1 wins")
    elif p1 == "rock" and p2 == "scissors":
        print("p1 wins")
    else:
        print("p2 wins")

p1 = int(input("p1 scissor - paper - rock choose one of them"))
p2 = int(input("p2 scissor - paper - rock choose one of them"))







rps()