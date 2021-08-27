import click
from Local import basic,commiting,branching,additional
from Remote import basicRemote,connectRemote,transferRemote


@click.group(help="user the commands mentioned below")
def main():
	""" See below """

main.add_command(basic.init)
main.add_command(basic.track)
main.add_command(basic.ignore)
main.add_command(basic.status)

main.add_command(commiting.commit)
main.add_command(commiting.history)
main.add_command(commiting.getHash)
main.add_command(commiting.getTag)
main.add_command(commiting.revert)

main.add_command(branching.changeBranch)
main.add_command(branching.makeBranch)
main.add_command(branching.showBranches)

main.add_command(additional.diff)

main.add_command(basicRemote.createAccount)
main.add_command(basicRemote.makeRemoteRepo)

main.add_command(connectRemote.addDevs)
main.add_command(connectRemote.showDevs)

main.add_command(transferRemote.pushRepo)


if __name__=="__main__":
   main()	





















