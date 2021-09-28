#!/usr/bin/bash
set -e

case $1 in
	clean)
		find ./data/guilds/ -type f -name "invites.tmp*" -exec rm {} \;
		find ./data/guilds/ -type d -empty -delete;
		;;

	help)
		echo "Usage: $0 [COMMAND]"
		echo ""
		echo "Commands:"
		echo "  clean  Delete tmp files and empty dirs"
		echo "  help   Show this help and exit"
		exit 0
		;;

	*)
		echo "Unknown command '$1'"
		echo "Use '$0 help' for more information."
		exit 2
		;;
esac
