#!/usr/bin/bash
set -eu

case $1 in
	users)
		cat ./data/trusted_users
		;;

	useradd)
		if [ -f ./data/trusted_users ]; then
			cp ./data/trusted_users ./data/trusted_users.tmp
		fi
		echo "$2####$3####$4" >> ./data/trusted_users.tmp
		sort ./data/trusted_users.tmp > ./data/trusted_users
		rm ./data/trusted_users.tmp
		;;

	userdel)
		grep -v "$2" ./data/trusted_users > ./data/trusted_users.tmp
		cp ./data/trusted_users.tmp ./data/trusted_users
		;;

	clean)
		find ./data/guilds/ -type f -name "invites.tmp*" -exec rm {} \;
		find ./data/guilds/ -type d -empty -delete;
		;;

	help)
		echo "Usage: $0 [COMMAND]"
		echo ""
		echo "Commands:"
		echo " users"
		echo "    Shows a list of trusted users"
		echo ""
		echo " userdel [ID]"
		echo "    Delete a trusted user"
		echo ""
		echo " useradd [ID] [ROLE] [INTERNAL_NICK]"
		echo "    Add a new trusted user"
		echo ""
		echo " clean"
		echo "    Delete tmp files and empty dirs"
		echo ""
		echo " help"
		echo "    Show this help and exit"
		exit 0
		;;

	*)
		echo "Unknown command '$1'"
		echo "Use '$0 help' for more information."
		exit 2
		;;
esac
